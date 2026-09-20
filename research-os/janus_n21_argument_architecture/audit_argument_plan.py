#!/usr/bin/env python3
# Local frozen copy of the scientific-argument-architect deterministic contract used at N21.
import json, sys
from collections import defaultdict, deque
from pathlib import Path
ALLOWED_STATUS={"VERIFIED","SUPPORTED","TENTATIVE","PENDING","REJECTED"}
def nonempty(x): return isinstance(x,str) and bool(x.strip()) and x.strip()!="REPLACE_ME"
def main():
    p=Path(sys.argv[1]); d=json.loads(p.read_text(encoding="utf-8")); errors=[]; warnings=[]
    for k in ["paper_id","target_venue","research_question","central_thesis"]:
        if not nonempty(d.get(k)): errors.append(f"missing {k}")
    pam=d.get("paper_argument_map",{})
    for k in ["problem","gap","approach","main_finding","mechanism","implication","scope_boundary"]:
        if not nonempty(pam.get(k)): errors.append(f"missing paper_argument_map.{k}")
    claims=d.get("claim_order",[]); ids=[c.get("claim_id") for c in claims]; known=set(ids)
    if not claims or len(ids)!=len(known): errors.append("missing/duplicate claims")
    graph=defaultdict(list); indeg={i:0 for i in known if i}
    for c in claims:
        cid=c.get("claim_id")
        if not nonempty(cid) or not nonempty(c.get("claim")): errors.append("claim id/text missing"); continue
        if c.get("status") not in ALLOWED_STATUS: errors.append(f"{cid}: invalid status")
        if not c.get("evidence_ids"): errors.append(f"{cid}: no evidence")
        for dep in c.get("depends_on",[]):
            if dep not in known: errors.append(f"{cid}: unknown dependency {dep}")
            else: graph[dep].append(cid); indeg[cid]=indeg.get(cid,0)+1
    q=deque([n for n,v in indeg.items() if v==0]); seen=0
    while q:
        n=q.popleft(); seen+=1
        for m in graph[n]:
            indeg[m]-=1
            if indeg[m]==0:q.append(m)
    if indeg and seen!=len(indeg): errors.append("claim dependency cycle")
    figs=d.get("figure_storyboard",[])
    for f in figs:
        if not all(nonempty(f.get(k)) for k in ["figure_id","question","role","answer"]): errors.append("figure field missing")
        if not f.get("claim_ids") or not f.get("evidence_ids") or not f.get("panels"): errors.append(f"{f.get('figure_id')}: incomplete")
        for c in f.get("claim_ids",[]):
            if c not in known: errors.append(f"{f.get('figure_id')}: unknown claim {c}")
        for p in f.get("panels",[]):
            if not nonempty(p.get("panel_id")) or not nonempty(p.get("job")): errors.append(f"{f.get('figure_id')}: bad panel")
    for s in d.get("section_logic",[]):
        for k in ["section","question","why_now","operation","answer","boundary","bridge"]:
            if not nonempty(s.get(k)): errors.append(f"section missing {k}")
        if not s.get("evidence_ids"): errors.append(f"{s.get('section')}: no evidence")
    for k in ["argument_map","figure_storyboard","section_logic"]:
        if d.get("gates",{}).get(k)!="PASS": errors.append(f"gate {k} not PASS")
    if d.get("handoff",{}).get("writer_ready") is not True: errors.append("writer_ready false")
    print(f"AUDIT: {p}")
    for e in errors: print("ERROR:",e)
    if errors: print(f"RESULT: FAIL ({len(errors)} errors)"); return 1
    print("RESULT: PASS (0 warnings)"); return 0
if __name__=="__main__": raise SystemExit(main())
