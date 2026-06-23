#!/usr/bin/env python3
"""Scaffold a personal AI assistant harness."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


def write_file(path: Path, content: str, overwrite: bool) -> bool:
    if path.exists() and not overwrite:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def templates(today: str, target: Path, mirror: Path | None, sync_script: Path | None) -> dict[str, str]:
    mirror_line = f"- Mirror: `{mirror}`\n" if mirror else ""
    sync_line = f"- Sync script: `{sync_script}`\n" if sync_script else ""
    location_lines = f"- Source of truth: `{target}`\n{mirror_line}{sync_line}".rstrip()
    return {
        "README.md": f"""# Personal Assistant Harness

This folder is the source of truth for durable personal context an assistant should load before helping.

## Locations

{location_lines}

## Read Order

For assistant startup, use `INIT_PROMPT.md`.

1. `who-am-i.md`
2. `preferences.md`
3. `current-focus.md`
4. `principles.md`
5. `projects/index.md`
6. Relevant `areas/`, `people/`, and `resources/` files
7. `memory/lessons.md` and `memory/decisions.md`

## Rules

- Prefer current files over older notes.
- Do not store secrets, credentials, private keys, recovery phrases, or sensitive data.
- If new durable context is learned, update the relevant file.
- If context is temporary or uncertain, add it to today's daily note first.
""",
        "INIT_PROMPT.md": f"""# Assistant Init Prompt

You are this user's personal assistant.

Before helping, load the personal assistant harness from:

```text
{target}
```

Read `README.md`, `who-am-i.md`, `preferences.md`, `current-focus.md`, `principles.md`, `projects/index.md`, `areas/index.md`, `resources/tools.md`, `resources/references.md`, `memory/lessons.md`, and `memory/decisions.md`.

Then load any additional project, area, people, resource, or bookmark files relevant to the current request.

Ask clarifying questions unless the background/context is already known and confidence is high. Treat security as a primary constraint.
""",
        "who-am-i.md": f"""# Who Am I

Last updated: {today}

## Identity

- Name:
- Preferred name:
- Location:
- Timezone:
- Languages:
- Primary roles:

## Background


## Current Context


## Long-Term Direction


## Strengths

- 

## Constraints

- 

## Non-Negotiables

- 

## Sensitive Topics

- 
""",
        "preferences.md": f"""# Preferences

Last updated: {today}

## Communication

- Preferred tone:
- Preferred detail level:
- Preferred language:
- Ask vs assume policy:
- Things to avoid:

## Work Style

- I prefer:
- I dislike:
- Decision style:
- Planning style:

## Tools

- Editor:
- Shell:
- Notes:
- Task manager:
- Browser:
- Coding environment:

## Output Preferences

- For code:
- For writing:
- For planning:
- For research:
- For summaries:
- For data analysis:
""",
        "current-focus.md": f"""# Current Focus

Last updated: {today}

## Top Priorities

1.
2.
3.

## This Week

- 

## Active Projects

- See `projects/index.md`.

## Waiting On

- 

## Constraints Right Now

- 

## Things To Avoid

- 

## Review Cadence

- 
""",
        "principles.md": f"""# Principles

Last updated: {today}

## Decision Principles

- 

## Work Principles

- 

## Learning Principles

- 

## Relationship Principles

- 

## Assistant Collaboration Principles

- 
""",
        "projects/index.md": f"""# Projects

Last updated: {today}

## Active Projects

| Project | Path / Link | Goal | Status | Next Action |
| --- | --- | --- | --- | --- |

## Project Rules

- Use this index to locate the relevant project before answering project-specific questions.
- Read project docs before assuming behavior.
- When coding changes behavior, update relevant documentation.
""",
        "areas/index.md": f"""# Areas

Last updated: {today}

Areas are ongoing responsibilities without a fixed end date.

## Active Areas

- `security.md`
- `learning.md`

## Area Rules

- Use area files for long-running responsibilities and standards.
- Use project files for specific deliverables and deadlines.
""",
        "areas/security.md": f"""# Security

Last updated: {today}

## Sensitive Information

- 

## Actions Requiring Confirmation

- 

## Operating Principles

- Do not expose secrets, credentials, private keys, recovery phrases, tokens, or sensitive data.
- If sensitive information is found, point to where it exists instead of reproducing it.
""",
        "areas/learning.md": f"""# Learning

Last updated: {today}

## Topics

- 

## Learning Preferences

- 

## Resources

- 
""",
        "people/index.md": f"""# People

Last updated: {today}

Create individual person files only when durable person-specific context is useful.

| Person | Relationship | Context File |
| --- | --- | --- |
""",
        "people/_template.md": f"""# Person Name

Last updated: {today}

## Relationship


## Context


## Preferences

- 

## Open Loops

- 
""",
        "resources/tools.md": f"""# Tools

Last updated: {today}

## Daily Tools

| Tool | Purpose | Notes |
| --- | --- | --- |

## Internal Systems

- 

## Vendor And External Systems

- 

## Documentation Defaults

- Use markdown by default unless another format is better for the task.
""",
        "resources/references.md": f"""# References

Last updated: {today}

## Links

- 

## Documents

- 

## Security Notes

- Treat internal links as pointers only.
- Do not reproduce sensitive page contents.
""",
        "resources/prompts.md": f"""# Prompts

Last updated: {today}

## Personal Assistant Startup

Read `assistant-harness/README.md`, then load the files listed in its read order. Summarize the relevant context before starting if it would help avoid misunderstanding.
""",
        "memory/lessons.md": f"""# Lessons

Last updated: {today}

Durable lessons about how to work with this user.

## Lessons

- 
""",
        "memory/decisions.md": f"""# Cross-Project Decisions

Last updated: {today}

| Date | Decision | Reason | Status |
| --- | --- | --- | --- |
""",
        f"memory/daily/{today}.md": f"""# {today}

## Timeline

- Created initial assistant harness structure.

## Raw Notes

- 

## Facts To Promote

- 
""",
        "archive/README.md": """# Archive

Inactive or superseded context lives here.
""",
    }


def create_sync_script(script_path: Path, target: Path, mirror: Path, overwrite: bool) -> bool:
    content = f"""#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="{target}"
TARGET_ROOT="{mirror}"

if [[ ! -d "$SOURCE_ROOT" ]]; then
  echo "Source harness not found: $SOURCE_ROOT" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"
rsync -a --delete "$SOURCE_ROOT"/ "$TARGET_ROOT"/

echo "Synced assistant harness:"
echo "  from: $SOURCE_ROOT"
echo "  to:   $TARGET_ROOT"
"""
    wrote = write_file(script_path, content, overwrite)
    if wrote:
        script_path.chmod(0o755)
    return wrote


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a personal AI assistant harness.")
    parser.add_argument("--target", required=True, type=Path, help="Source-of-truth harness directory")
    parser.add_argument("--mirror", type=Path, help="Optional mirror directory")
    parser.add_argument("--sync-script", type=Path, help="Optional sync script path")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    target = args.target.expanduser().resolve()
    mirror = args.mirror.expanduser().resolve() if args.mirror else None
    sync_script = args.sync_script.expanduser().resolve() if args.sync_script else None

    written = []
    skipped = []
    for rel_path, content in templates(today, target, mirror, sync_script).items():
        path = target / rel_path
        if write_file(path, content, args.overwrite):
            written.append(path)
        else:
            skipped.append(path)

    if mirror:
        mirror.mkdir(parents=True, exist_ok=True)
    if sync_script:
        if not mirror:
            raise SystemExit("--sync-script requires --mirror")
        if create_sync_script(sync_script, target, mirror, args.overwrite):
            written.append(sync_script)
        else:
            skipped.append(sync_script)

    print(f"Assistant harness scaffolded at: {target}")
    print(f"Files written: {len(written)}")
    print(f"Files skipped: {len(skipped)}")
    if mirror:
        print(f"Mirror directory prepared at: {mirror}")
    if sync_script:
        print(f"Sync script: {sync_script}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
