#!/usr/bin/env python3
"""Convert Obsidian [[wiki]] links to GitHub markdown links for web publishing."""

import os
import re
import shutil
import sys
from pathlib import Path

# Configuration
GITHUB_USER = "Devito02"
GITHUB_REPO = "Hyperlink-Wiki"
GITHUB_BRANCH = "main"
BASE_URL = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/blob/{GITHUB_BRANCH}"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_github-output"
WIKI_DIR = ROOT / "wiki"
RAW_DIR = ROOT / "raw"
TEMPLATES_DIR = ROOT / "_templates"

DIRS_TO_COPY = ["wiki", "raw"]


def build_page_index():
    """Scan wiki/ and raw/ to build page-name -> relative-path mapping.

    Adds aliases for common naming mismatches:
    - underscore <-> space (Trascritto_1 <-> Trascritto 1)
    - hyphen <-> underscore (trascritto-1 <-> Trascritto_1)
    """
    index = {}
    for base_dir in DIRS_TO_COPY:
        base_path = ROOT / base_dir
        for md_file in base_path.rglob("*.md"):
            page_name = md_file.stem
            rel_path = md_file.relative_to(ROOT).as_posix()
            index[page_name] = rel_path

    # Build aliases for common mismatches
    aliases = {}
    for key, val in index.items():
        aliases[key.replace("_", " ")] = val
        aliases[key.replace("_", "-")] = val
        aliases[key.replace(" ", "_")] = val
        aliases[key.replace(" ", "-")] = val
        aliases[key.replace("-", "_")] = val
        aliases[key.replace("-", " ")] = val
    index.update(aliases)
    return index


def convert_links(text, page_index):
    """Replace all [[link]] and [[link|display]] with GitHub markdown links."""
    def replace_match(match):
        inner = match.group(1).strip()
        display = inner
        anchor = ""

        # Handle [[link#anchor]] or [[link#anchor|display]]
        if "#" in inner:
            parts = inner.split("#", 1)
            inner = parts[0]
            anchor = "#" + parts[1].split("|")[0] if "|" in parts[1] else "#" + parts[1]
            display = parts[1].split("|")[-1] if "|" in parts[1] else inner + anchor

        # Handle [[link|display]]
        if "|" in inner:
            inner, display = inner.split("|", 1)

        # Resolve page name to file path
        if inner in page_index:
            url = f"{BASE_URL}/{page_index[inner]}{anchor}"
            return f"[{display}]({url})"
        else:
            # Page doesn't exist — keep as plain text
            return display

    # Pattern: [[ ... ]]  (non-greedy, skips escaped)
    pattern = r"\[\[([^\]]+)\]\]"
    return re.sub(pattern, replace_match, text)


def process_file(src_path, dst_path, page_index):
    """Copy a file, converting Obsidian links to GitHub links."""
    content = src_path.read_text(encoding="utf-8")
    converted = convert_links(content, page_index)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(converted, encoding="utf-8")


def main():
    print(f"Building page index...")
    page_index = build_page_index()
    print(f"  Found {len(page_index)} pages")

    # Clean output
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)

    # Copy and convert wiki/
    wiki_files = list((ROOT / "wiki").rglob("*.md"))
    print(f"\nConverting {len(wiki_files)} wiki files...")
    for src in wiki_files:
        rel = src.relative_to(ROOT)
        dst = OUTPUT / rel
        process_file(src, dst, page_index)

    # Copy raw/ (no link conversion needed, but do it anyway for consistency)
    raw_files = list((ROOT / "raw").rglob("*.md"))
    print(f"Copying {len(raw_files)} raw files...")
    for src in raw_files:
        rel = src.relative_to(ROOT)
        dst = OUTPUT / rel
        process_file(src, dst, page_index)

    # Copy top-level files
    for fname in ["README.md", "CLAUDE.md"]:
        fpath = ROOT / fname
        if fpath.exists():
            dst = OUTPUT / fname
            if fname.endswith(".md"):
                process_file(fpath, dst, page_index)
            else:
                shutil.copy2(fpath, dst)

    print(f"\nDone! Output in {OUTPUT}")
    print(f"Total files converted: {len(wiki_files) + len(raw_files)}")
    print(f"\nNext steps:")
    print(f"  cd {OUTPUT}")
    print(f"  git init")
    print(f"  git add -A")
    print(f'  git commit -m "Initial publish with GitHub links"')
    print(f"  git remote add origin https://github.com/{GITHUB_USER}/{GITHUB_REPO}.git")
    print(f"  git push -u origin main")


if __name__ == "__main__":
    main()
