#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

REQUIRED_VARS = ("DBX_CATALOG", "DBX_SCHEMA", "DBX_USERNAME")

def find_root_env(start_path: Path) -> Path | None:
    """
    Walk up from start_path to the filesystem root and return the top-most .env found.
    """
    start_path = start_path.resolve()
    candidates = []
    search_dir = start_path if start_path.is_dir() else start_path.parent
    for p in [search_dir, *search_dir.parents]:
        env_path = p / ".env"
        if env_path.is_file():
            candidates.append(env_path)
    return candidates[-1] if candidates else None

def load_env_from_root(start_path: Path) -> dict:
    """
    Use python-dotenv to load .env from repo root (top-most) without overriding OS env.
    Validate required variables exist after load.
    """
    env_file = find_root_env(start_path)
    if env_file:
        # OS env keeps precedence (override=False)
        load_dotenv(dotenv_path=env_file, override=False)

    env = {k: os.getenv(k) for k in REQUIRED_VARS}
    missing = [k for k, v in env.items() if not v]
    if missing:
        hint = f"No .env found above {start_path.resolve()}" if not env_file else f"Loaded .env from {env_file}"
        raise SystemExit(
            f"{hint}. Missing required variables: {', '.join(missing)}. "
            f"Set them in the root .env or export them in your shell."
        )
    return env

def replace_placeholders(text: str, env: dict) -> str:
    mapping = {
        "{catalog}": env["DBX_CATALOG"],
        "{schema}": env["DBX_SCHEMA"],
        "{username}": env["DBX_USERNAME"],
    }
    for token, value in mapping.items():
        text = text.replace(token, value)
    return text

def derive_output_path(input_path: Path) -> Path:
    name = input_path.name
    if name.endswith(".json.template"):
        return input_path.with_name(name[: -len(".json.template")] + ".json")
    if name.endswith(".template"):
        base = input_path.with_suffix("")
        if base.suffix != ".json":
            return base.with_suffix(base.suffix + ".json")
        return base
    return input_path.with_suffix(".json")

def process_file(path: Path, env: dict) -> Path:
    out_text = replace_placeholders(path.read_text(), env)
    out_path = derive_output_path(path)
    out_path.write_text(out_text)
    return out_path

def find_files(root: Path, recursive: bool):
    if root.is_file():
        yield root
        return
    pattern = "**/*.json.template" if recursive else "*.json.template"
    for f in root.glob(pattern):
        if f.is_file():
            yield f

def main():
    parser = argparse.ArgumentParser(
        description="Replace {catalog}, {schema}, {username} in *.json.template files using root .env and write *.json."
    )
    parser.add_argument("path", help="Path to a template file or a directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories")
    args = parser.parse_args()

    root = Path(args.path)
    env = load_env_from_root(root)

    files = list(find_files(root, args.recursive))
    if not files:
        if not root.exists():
            print(f"Path not found: {root}", file=sys.stderr)
            sys.exit(1)
        files = [root]

    written = [process_file(f, env) for f in files]

    for p in written:
        print(f"  {p}")

if __name__ == "__main__":
    main()