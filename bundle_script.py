#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

REQUIRED_VARS = ("DBX_CATALOG", "DBX_SCHEMA", "DBX_USERNAME")

def load_env_from_repo_root(repo_root: Path) -> dict:
    """Load .env from the repo root (same directory as this script)."""
    env_file = repo_root / ".env"
    if not env_file.is_file():
        raise SystemExit(f"Missing .env at {env_file}. Place .env in the repo root.")
    load_dotenv(dotenv_path=env_file, override=False)

    env = {k: os.getenv(k) for k in REQUIRED_VARS}
    missing = [k for k, v in env.items() if not v]
    if missing:
        raise SystemExit(
            f"Missing required variables in .env: {', '.join(missing)}. "
            f"Set DBX_CATALOG, DBX_SCHEMA, DBX_USERNAME."
        )
    return env

def replace_placeholders(text: str, env: dict) -> str:
    for token, value in {
        "{catalog}": env["DBX_CATALOG"],
        "{schema}": env["DBX_SCHEMA"],
        "{username}": env["DBX_USERNAME"],
    }.items():
        text = text.replace(token, value)
    return text

def derive_output_path(input_path: Path) -> Path:
    name = input_path.name
    if name.endswith(".json.template"):
        return input_path.with_name(name[:-len(".json.template")] + ".json")
    if name.endswith(".template"):
        base = input_path.with_suffix("")  # strip ".template"
        return base if base.suffix == ".json" else base.with_suffix(base.suffix + ".json")
    return input_path.with_suffix(".json")

def process_file(path: Path, env: dict) -> Path:
    out_text = replace_placeholders(path.read_text(), env)
    out_path = derive_output_path(path)
    out_path.write_text(out_text)
    return out_path

def collect_files(root: Path, recursive: bool):
    if root.is_file():
        return [root]
    pattern = "**/*.json.template" if recursive else "*.json.template"
    return [p for p in root.glob(pattern) if p.is_file()]

def main():
    parser = argparse.ArgumentParser(
        description="Convert *.json.template to *.json by replacing {catalog}, {schema}, {username} using repo-root .env."
    )
    parser.add_argument("path", help="Path to a template file or a directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    env = load_env_from_repo_root(repo_root)

    root = Path(args.path)
    files = collect_files(root, args.recursive)
    if not files:
        if not root.exists():
            print(f"Path not found: {root}", file=sys.stderr)
            sys.exit(1)
        files = [root]

    for f in files:
        out = process_file(f, env)
        print(f"Wrote: {out}")

if __name__ == "__main__":
    main()