#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
ALLOWED_PROVENANCE={"MEASURED","SIMULATION_EXECUTED","SYNTHETIC_TEST","ILLUSTRATIVE","PLACEHOLDER"}
EVIDENCE_ELIGIBLE_DEFAULT={"MEASURED","SIMULATION_EXECUTED"}
def nonempty(value: Any)->bool: return isinstance(value,str) and bool(value.strip())
def audit(data):
    errors=[]; warnings=[]
    for key in ["figure_id","core_conclusion","archetype","caption"]:
        if not nonempty(data.get(key)): errors.append(f"missing/empty required field: {key}")
    claim_ids=data.get("claim_ids")
    if not isinstance(claim_ids,list): errors.append("claim_ids must be a list")
    elif not claim_ids: warnings.append("claim_ids is empty; figure may be explanatory rather than evidentiary")
    prov=data.get("provenance")
    if not isinstance(prov,dict): errors.append("provenance must be an object")
    else:
        pclass=prov.get("class"); eligible=prov.get("manuscript_evidence_eligible")
        if pclass not in ALLOWED_PROVENANCE: errors.append(f"invalid provenance.class: {pclass!r}")
        if not isinstance(eligible,bool): errors.append("provenance.manuscript_evidence_eligible must be boolean")
        if pclass in {"ILLUSTRATIVE","PLACEHOLDER"} and eligible is True: errors.append(f"{pclass} cannot be marked manuscript_evidence_eligible=true")
        if pclass=="SYNTHETIC_TEST" and eligible is True: warnings.append("SYNTHETIC_TEST evidence is only eligible when the manuscript claim explicitly concerns synthetic testing")
        if pclass in EVIDENCE_ELIGIBLE_DEFAULT and eligible is False: warnings.append(f"{pclass} is usually evidence-eligible; confirm why it is disabled")
    panels=data.get("panels")
    if not isinstance(panels,list) or not panels: errors.append("panels must be a non-empty list")
    else:
        ids=set(); questions=set()
        for i,panel in enumerate(panels):
            label=f"panels[{i}]"
            if not isinstance(panel,dict): errors.append(f"{label} must be an object"); continue
            pid=panel.get("id")
            if not nonempty(pid): errors.append(f"{label}.id missing/empty")
            elif pid in ids: errors.append(f"duplicate panel id: {pid}")
            else: ids.add(pid)
            q=panel.get("question")
            if not nonempty(q): errors.append(f"{label}.question missing/empty")
            elif q.strip() in questions: warnings.append(f"duplicate panel question: {q.strip()}")
            else: questions.add(q.strip())
            if not nonempty(panel.get("visual_type")): errors.append(f"{label}.visual_type missing/empty")
            evidence_ids=panel.get("evidence_ids"); source_paths=panel.get("source_paths")
            if not isinstance(evidence_ids,list): errors.append(f"{label}.evidence_ids must be a list")
            if not isinstance(source_paths,list): errors.append(f"{label}.source_paths must be a list")
            if prov and prov.get("manuscript_evidence_eligible") is True:
                if isinstance(evidence_ids,list) and not evidence_ids: warnings.append(f"{label} is evidence-eligible but has no evidence_ids")
                if isinstance(source_paths,list) and not source_paths: warnings.append(f"{label} is evidence-eligible but has no source_paths")
            if panel.get("uncertainty_shown") is True and not nonempty(panel.get("uncertainty_definition")): errors.append(f"{label} shows uncertainty but uncertainty_definition is empty")
    exports=data.get("exports")
    if not isinstance(exports,dict): errors.append("exports must be an object")
    else:
        rendered=[exports.get(k) for k in ("pdf","svg","tiff","png_preview") if nonempty(exports.get(k))]
        if not rendered: warnings.append("no rendered export path is recorded")
        if not nonempty(exports.get("source")): warnings.append("no plotting/design source file is recorded")
        archetype=str(data.get("archetype","")).lower(); vector_preferred=not any(x in archetype for x in ("image","microscopy","photo"))
        if vector_preferred and not (nonempty(exports.get("pdf")) or nonempty(exports.get("svg"))): warnings.append("vector-friendly figure has no PDF/SVG export recorded")
    size=data.get("final_size")
    if isinstance(size,dict):
        text_pt=size.get("min_text_pt"); line_pt=size.get("min_line_pt")
        if isinstance(text_pt,(int,float)) and text_pt<7: warnings.append("min_text_pt < 7 pt; verify venue requirement and final-size readability")
        if isinstance(line_pt,(int,float)) and line_pt<0.5: warnings.append("min_line_pt < 0.5 pt; verify print readability and venue requirement")
        if size.get("width_mm") is None: warnings.append("final_size.width_mm is not recorded")
    else: warnings.append("final_size is not recorded")
    qa=data.get("qa")
    if isinstance(qa,dict):
        if qa.get("scientific")=="FAIL" or qa.get("visual")=="FAIL" or qa.get("venue")=="FAIL": errors.append("one or more QA gates are marked FAIL")
        if qa.get("visual")=="NOT_RUN": warnings.append("final-size visual QA has not been run")
    else: warnings.append("qa status is not recorded")
    return errors,warnings

def main():
    p=argparse.ArgumentParser(); p.add_argument("manifest"); args=p.parse_args(); path=Path(args.manifest)
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: print(f"FAIL: cannot read JSON: {exc}"); return 2
    if not isinstance(data,dict): print("FAIL: root must be a JSON object"); return 2
    errors,warnings=audit(data)
    for item in errors: print(f"ERROR: {item}")
    for item in warnings: print(f"WARN: {item}")
    if errors: print(f"RESULT: FAIL ({len(errors)} errors, {len(warnings)} warnings)"); return 1
    if warnings: print(f"RESULT: PASS_WITH_WARNINGS (0 errors, {len(warnings)} warnings)"); return 0
    print("RESULT: PASS"); return 0
if __name__=='__main__': raise SystemExit(main())
