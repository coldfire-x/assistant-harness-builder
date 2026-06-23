---
name: assistant-harness-builder
description: "Create a personal AI assistant harness: a durable folder structure, startup/init prompt, identity and preference docs, project index, areas, people, resources, memory, sync/mirror workflow, and guided interview questions. Use when someone asks to set up, design, scaffold, improve, or standardize an AI-powered personal/work assistant context folder for themselves or a team."
---

# Assistant Harness Builder

## Overview

Build a durable assistant harness that lets future assistants quickly understand a person, their preferences, active work, tools, projects, relationships, and safety constraints.

Use this skill as an interview-and-scaffold workflow. Keep the user's harness small enough for assistants to read, but structured enough to preserve useful context across sessions.

## Workflow

1. Confirm the target source-of-truth folder and any mirror folder.
2. Scaffold the baseline structure with `scripts/create_assistant_harness.py` when useful.
3. Guide the user through the setup one file at a time.
4. Update files after each answer and sync/mirror if configured.
5. Add an `INIT_PROMPT.md` that future agents can use as startup instruction.
6. Record decisions and lessons as durable memory.

If the user wants the full architecture, questions, or file definitions, read `references/harness-blueprint.md`.

## Default Structure

Use this structure unless the user has a strong reason to change it:

```text
assistant-harness/
  README.md
  INIT_PROMPT.md
  who-am-i.md
  preferences.md
  current-focus.md
  principles.md
  projects/index.md
  areas/index.md
  people/index.md
  people/_template.md
  resources/tools.md
  resources/references.md
  resources/prompts.md
  memory/lessons.md
  memory/decisions.md
  memory/daily/YYYY-MM-DD.md
  archive/README.md
```

Add project or area files only when they are useful. Do not force personal files such as health or finance if the user wants a work-focused harness.

## Interview Order

Ask for rough bullets, then convert them into assistant-readable text.

1. `who-am-i.md`: identity, background, current context, long-term direction, strengths, constraints, non-negotiables.
2. `preferences.md`: communication style, detail level, language, ask-vs-assume policy, work style, engineering/research/data defaults.
3. `current-focus.md`: top priorities, this week, active projects, waiting-on items, constraints, avoid list, review cadence.
4. `principles.md`: decision, work, learning, relationship, and assistant-collaboration principles.
5. `projects/index.md`: active project map, repo paths, or goal/status table.
6. `areas/`: long-running responsibilities such as engineering leadership, security, learning, compliance, AI agents.
7. `people/`: keep minimal unless durable person-specific context is useful.
8. `resources/`: tools, references, bookmark classifications, prompts.
9. `memory/`: lessons and cross-project decisions.
10. `INIT_PROMPT.md`: the startup prompt for future assistants.

## File Rules

- Prefer markdown.
- Keep top-level files concise and high-signal.
- Separate stable identity from current priorities.
- Separate projects with deadlines from areas with no end date.
- Treat internal links as pointers. Do not reproduce sensitive data.
- For sensitive info, store policy and location pointers, not secrets.
- Add examples or generated samples when the user is unsure, then ask whether to keep or edit.

## Scaffold Command

Run this to create the baseline files:

```bash
python3 scripts/create_assistant_harness.py --target /path/to/assistant-harness
```

Optional mirror/sync script:

```bash
python3 scripts/create_assistant_harness.py \
  --target /path/to/source/assistant-harness \
  --mirror /path/to/mirror/assistant-harness \
  --sync-script /path/to/sync_assistant_harness.sh
```

The script will not overwrite existing files unless `--overwrite` is passed.

## Init Prompt Pattern

Create `INIT_PROMPT.md` with:

```text
You are <name>'s personal work assistant.

Before helping, load the personal assistant harness from:
<source-of-truth-path>

Read README.md, who-am-i.md, preferences.md, current-focus.md, principles.md,
projects/index.md, areas/index.md, resources/tools.md, resources/references.md,
memory/lessons.md, and memory/decisions.md.

Then load any additional project, area, people, resource, or bookmark files
that are relevant to the user's current request.
```

Add the user's core operating rules: ask-vs-assume policy, security rules, communication style, documentation defaults, and confirmation gates.

## Delivery

After setup, report:

- Source-of-truth path.
- Mirror path, if any.
- Sync command, if any.
- Files completed.
- Files intentionally skipped.
- Next recommended file to refine.
