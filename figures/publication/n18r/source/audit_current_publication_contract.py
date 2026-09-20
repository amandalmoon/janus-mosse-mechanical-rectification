from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ROOT / "manifests"
VALID_ROLES = {"hero", "validation", "control", "robustness", "mechanism", "context"}
REQUIRED_TOP = {
    "figure_id", "manuscript_role", "core_conclusion", "claim_ids", "archetype",
    "final_size", "design_system", "provenance", "panels", "exports",
    "caption", "visual_qa", "qa", "publication_gate",
}
REQUIRED_PANEL = {
    "id", "question", "role", "visual_type", "evidence_ids", "source_paths",
    "uncertainty_shown", "uncertainty_definition", "processing_notes", "scale",
}
REQUIRED_VISUAL_QA_TRUE = {
    "render_opened", "final_size_inspected", "no_overlap_or_clipping",
    "panel_hierarchy_clear", "theory_data_semantics_clear",
    "redundant_series_encoding", "caption_parameter_complete",
    "not_default_matplotlib",
}


def check_source(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    compact = re.sub(r"\s+", " ", text.lower())
    errors: list[str] = []
    if re.search(r"style\.use\(\s*['\"]default['\"]", compact):
        errors.append("default matplotlib style")
    rc_keys = [
        "font.family", "font.size", "axes.labelsize", "xtick.labelsize",
        "ytick.labelsize", "axes.linewidth", "lines.linewidth",
        "lines.markersize", "pdf.fonttype", "svg.fonttype",
    ]
    explicit_style = bool(re.search(r"(?:plt|mpl|matplotlib)\.style\.use\(", text)) or sum(k in text for k in rc_keys) >= 6
    if not explicit_style:
        errors.append("no explicit publication style")
    if "figsize=" not in compact and "set_size_inches" not in compact:
        errors.append("no explicit final figure size")
    if "savefig" not in compact:
        errors.append("no savefig/export contract")
    if not any(ext in compact for ext in [".pdf", ".svg"]):
        errors.append("no vector export contract")
    return errors


def main() -> int:
    errors: list[str] = []
    for manifest_path in sorted(MANIFESTS.glob("FIG-*.json")):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_TOP - data.keys())
        if missing:
            errors.append(f"{manifest_path.name}: missing top-level {missing}")
            continue

        if data["publication_gate"] != "PUBLICATION_READY":
            errors.append(f"{manifest_path.name}: publication_gate is not PUBLICATION_READY")
        if data.get("qa", {}).get("scientific") != "PASS":
            errors.append(f"{manifest_path.name}: scientific QA is not PASS")
        if data.get("qa", {}).get("visual") != "PASS":
            errors.append(f"{manifest_path.name}: visual QA is not PASS")
        if data.get("qa", {}).get("venue") != "PASS":
            errors.append(f"{manifest_path.name}: venue QA is not PASS")
        if data.get("provenance", {}).get("class") in {"ILLUSTRATIVE", "PLACEHOLDER"}:
            errors.append(f"{manifest_path.name}: ineligible evidence provenance")

        for panel in data["panels"]:
            pmissing = sorted(REQUIRED_PANEL - panel.keys())
            if pmissing:
                errors.append(f"{manifest_path.name}/{panel.get('id')}: missing {pmissing}")
            if panel.get("role") not in VALID_ROLES:
                errors.append(f"{manifest_path.name}/{panel.get('id')}: invalid role {panel.get('role')!r}")
            if panel.get("uncertainty_shown") and not panel.get("uncertainty_definition"):
                errors.append(f"{manifest_path.name}/{panel.get('id')}: uncertainty definition missing")

        visual = data["visual_qa"]
        for key in REQUIRED_VISUAL_QA_TRUE:
            if visual.get(key) is not True:
                errors.append(f"{manifest_path.name}: visual_qa.{key} is not true")

        exports = data["exports"]
        for key in ["pdf", "svg", "png_preview", "source"]:
            if not exports.get(key):
                errors.append(f"{manifest_path.name}: exports.{key} missing")
                continue
            p = (manifest_path.parent / exports[key]).resolve()
            if key != "source" and not p.exists():
                # Rendered binaries are CI products and can be absent in git checkout.
                continue
            if key == "source":
                if not p.exists():
                    errors.append(f"{manifest_path.name}: source does not exist: {p}")
                elif p.suffix.lower() == ".py":
                    for issue in check_source(p):
                        errors.append(f"{manifest_path.name}: {issue}: {p.name}")

        final_size = data["final_size"]
        if float(final_size.get("min_text_pt", 0)) < 7.0:
            errors.append(f"{manifest_path.name}: min_text_pt below N18R benchmark")
        if float(final_size.get("min_line_pt", 0)) < 0.55:
            errors.append(f"{manifest_path.name}: min_line_pt below N18R benchmark")

    if errors:
        print("CURRENT STRICT FIGURE CONTRACT: FAIL")
        for item in errors:
            print("ERROR:", item)
        return 1

    print("CURRENT STRICT FIGURE CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
