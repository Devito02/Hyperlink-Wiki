#!/usr/bin/env python3
"""Convert Dataview query blocks to static markdown tables.

Runs locally, no API calls. Handles the Dataview patterns used in this project:
- TABLE field, field FROM "dir" SORT ... ASC/DESC
- LIST FROM "dir"
- TABLE ... GROUP BY field
- FROM "dir" WHERE expression
"""

import re
import yaml
from pathlib import Path


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                return {}
    return {}


def find_files(directory, where_expr=None):
    """Find all markdown files in directory, optionally filtered."""
    files = sorted(directory.glob("*.md"))
    results = []
    for f in files:
        content = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        fm["_file"] = f
        fm["_name"] = f.stem
        results.append((f, fm))

    if where_expr:
        # Simple WHERE: field name exists (truthy check)
        field = where_expr.strip()
        results = [(f, fm) for f, fm in results if fm.get(field)]

    return results


def resolve_link(name, page_index):
    """Convert a page name to a GitHub markdown link."""
    if name in page_index:
        return f"[{name}]({page_index[name]})"
    # Try alias resolution
    for sep_from, sep_to in [("_", " "), (" ", "_"), ("-", " "), (" ", "-")]:
        alt = name.replace(sep_from, sep_to)
        if alt in page_index:
            return f"[{alt}]({page_index[alt]})"
    return name


def build_page_index(root):
    """Build page-name -> relative URL mapping."""
    index = {}
    for base_dir in ["wiki", "raw"]:
        for md_file in (root / base_dir).rglob("*.md"):
            index[md_file.stem] = md_file.relative_to(root).as_posix()
    return index


def replace_dataview_block(match, root, page_index):
    """Replace a dataview code block with a static markdown table."""
    query = match.group(1).strip()

    # Parse FROM
    from_match = re.search(r'FROM\s+"([^"]+)"', query)
    if not from_match:
        return match.group(0)  # Can't parse, leave as-is
    directory = root / from_match.group(1)

    if not directory.exists():
        return match.group(0)

    # Parse WHERE
    where_match = re.search(r'WHERE\s+(\S+)', query)
    where_expr = where_match.group(1) if where_match else None

    # LIST query
    if re.search(r'^LIST', query):
        files_data = find_files(directory, where_expr)
        lines = []
        for f, fm in files_data:
            link = resolve_link(f.stem, page_index)
            lines.append(f"- {link}")
        return "\n".join(lines) if lines else "_Nessuna pagina_"

    # TABLE query
    table_match = re.search(r'TABLE\s+(.+?)(?:\s+FROM|\s+SORT|\s+WHERE|\s+GROUP|\s*$)', query)
    if not table_match:
        return match.group(0)

    fields = [f.strip() for f in table_match.group(1).split(",")]
    files_data = find_files(directory, where_expr)

    if not files_data:
        return "_Nessuna pagina_"

    # Parse SORT
    sort_match = re.search(r'SORT\s+(\S+)\s*(ASC|DESC)?', query)
    if sort_match:
        sort_field = sort_match.group(1)
        reverse = sort_match.group(2) == "DESC"
        if sort_field == "file.name":
            files_data.sort(key=lambda x: x[0].stem.lower(), reverse=reverse)
        elif sort_field == "rows.length":
            pass  # GROUP BY sorting handled elsewhere
        else:
            files_data.sort(
                key=lambda x: str(x[1].get(sort_field, "")).lower(),
                reverse=reverse,
            )

    # GROUP BY
    group_match = re.search(r'GROUP BY\s+(\S+)', query)
    if group_match:
        group_field = group_match.group(1)
        groups = {}
        for f, fm in files_data:
            key = str(fm.get(group_field, "_non specificato"))
            groups.setdefault(key, []).append((f, fm))

        lines = []
        for group_key in sorted(groups.keys()):
            lines.append(f"\n### {group_key}\n")
            lines.append(f"| Pagina | {' | '.join(fields)} |")
            lines.append(f"|{'---|' * (len(fields) + 1)}")
            for f, fm in groups[group_key]:
                link = resolve_link(f.stem, page_index)
                values = [str(fm.get(field, "-")) for field in fields]
                lines.append(f"| {link} | {' | '.join(values)} |")
        return "\n".join(lines)

    # Simple TABLE
    lines = []
    header_parts = ["Pagina"] + fields
    lines.append(f"| {' | '.join(header_parts)} |")
    lines.append(f"|{'---|' * len(header_parts)}")

    for f, fm in files_data:
        link = resolve_link(f.stem, page_index)
        values = [str(fm.get(field, "-")) for field in fields]
        lines.append(f"| {link} | {' | '.join(values)} |")

    return "\n".join(lines)


def process_file(filepath, root, page_index):
    """Convert all dataview blocks in a file to static tables."""
    content = filepath.read_text(encoding="utf-8")
    pattern = r"```dataview\n(.*?)```"
    new_content = re.sub(
        pattern,
        lambda m: replace_dataview_block(m, root, page_index),
        content,
        flags=re.DOTALL,
    )
    filepath.write_text(new_content, encoding="utf-8")


def main():
    root = Path(__file__).resolve().parent.parent
    output_dir = root / "_github-output"

    if not output_dir.exists():
        print(f"Error: {output_dir} not found. Run convert-links.py first.")
        return

    print("Building page index...")
    page_index = build_page_index(output_dir)
    print(f"  {len(page_index)} pages indexed")

    index_md = output_dir / "wiki" / "index.md"
    if index_md.exists():
        print(f"Processing {index_md}...")
        process_file(index_md, output_dir, page_index)
        print("  Done!")
    else:
        print(f"Warning: {index_md} not found")


if __name__ == "__main__":
    main()
