#!/usr/bin/env python3
"""Structural validator for the G4-SWE Elite submission directory."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submission"
REQUIRED = [
    SUB / "agent.yaml",
    SUB / "prompts/system.md",
    SUB / "configs/sampling.yaml",
    SUB / "sub_agents/repo_analyst.yaml",
    SUB / "sub_agents/analyzer.md",
    SUB / "skills/repo_navigation/SKILL.md",
    SUB / "skills/repair_protocol/SKILL.md",
]
MODELS = {
    "gemma-4-31b-it-qat-w4a16-ct",
    "gemma-4-12b-it-qat-w4a16-ct",
    "gemma-4-e4b-it-qat-w4a16-ct",
    "gemma-4-e2b-it-qat-w4a16-ct",
}


def main() -> int:
    errors = []
    for path in REQUIRED:
        if not path.is_file():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1

    root_yaml = (SUB / "agent.yaml").read_text(encoding="utf-8")
    sub_yaml = (SUB / "sub_agents/repo_analyst.yaml").read_text(encoding="utf-8")
    root_model = re.search(r"(?m)^model:\s*(\S+)\s*$", root_yaml)
    sub_model = re.search(r"(?m)^model:\s*(\S+)\s*$", sub_yaml)
    if not root_model or root_model.group(1) not in MODELS:
        errors.append("Root agent model is missing or not in the currently published allowlist.")
    if not sub_model or sub_model.group(1) not in MODELS:
        errors.append("Sub-agent model is missing or not in the currently published allowlist.")
    if root_model and sub_model and root_model.group(1) != sub_model.group(1):
        errors.append("Root agent and sub-agent must use the same base model.")

    # Reject symlinks and path traversal in submission assets.
    for path in SUB.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink is not allowed in submission: {path.relative_to(SUB)}")
        if ".." in path.relative_to(SUB).parts:
            errors.append(f"Path traversal component found: {path}")

    try:
        import yaml  # type: ignore
        for path in [SUB / "agent.yaml", SUB / "configs/sampling.yaml", SUB / "sub_agents/repo_analyst.yaml"]:
            # !include is a custom tag, so register a harmless constructor.
            class IncludeLoader(yaml.SafeLoader):
                pass
            IncludeLoader.add_constructor("!include", lambda loader, node: loader.construct_scalar(node))
            yaml.load(path.read_text(encoding="utf-8"), Loader=IncludeLoader)
        print("YAML syntax: parsed (PyYAML)")
    except ImportError:
        print("YAML syntax: skipped (PyYAML not installed; official validator remains required)")
    except Exception as exc:
        errors.append(f"YAML parse error: {exc}")

    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print("PASS: required files, model consistency, and path checks passed.")
    print("NOTE: this is not a substitute for the official Kaggle harness validator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
