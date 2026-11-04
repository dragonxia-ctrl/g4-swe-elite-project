#!/usr/bin/env python3
"""Build a Kaggle-ready submission.zip with agent.yaml at archive root."""
from pathlib import Path
import argparse
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submission"
OUT = ROOT / "submission.zip"
MODELS = {
    "gemma-4-31b-it-qat-w4a16-ct",
    "gemma-4-12b-it-qat-w4a16-ct",
    "gemma-4-e4b-it-qat-w4a16-ct",
    "gemma-4-e2b-it-qat-w4a16-ct",
}


def set_model(path: Path, model: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^model:\s*\S+\s*$", f"model: {model}", text, count=1)
    if count != 1:
        raise RuntimeError(f"Could not update model field in {path}")
    path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemma-4-31b-it-qat-w4a16-ct", choices=sorted(MODELS))
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()

    # Keep every agent on the same permitted base model.
    set_model(SUB / "agent.yaml", args.model)
    set_model(SUB / "sub_agents/repo_analyst.yaml", args.model)

    # Run structural validation before packaging.
    import subprocess
    result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_submission.py")])
    if result.returncode:
        return result.returncode

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(SUB.rglob("*")):
            if path.is_file() and not path.is_symlink():
                arcname = path.relative_to(SUB).as_posix()
                zf.write(path, arcname)
    with zipfile.ZipFile(output) as zf:
        names = set(zf.namelist())
        if "agent.yaml" not in names:
            raise RuntimeError("agent.yaml is not at archive root")
    print(f"Built: {output}")
    print(f"Files: {len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
