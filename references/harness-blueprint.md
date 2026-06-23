# Assistant Harness Blueprint

## Purpose

An assistant harness is a durable folder that gives AI assistants enough context to help a person consistently across sessions. It should answer:

- Who is this person?
- How should assistants work with them?
- What are they focused on now?
- What projects, tools, people, and references matter?
- What safety/security rules must be followed?
- What lessons and decisions should persist?

## Architecture

```text
assistant-harness/
  README.md                 # How to use the harness
  INIT_PROMPT.md            # Startup prompt for future assistants
  who-am-i.md               # Stable identity and context
  preferences.md            # Communication, work, tool, output defaults
  current-focus.md          # Current priorities and constraints
  principles.md             # Decision/work/learning/team principles
  projects/
    index.md                # Active project map
    <project-name>/         # Optional per-project context
      summary.md
      notes.md
      decisions.md
  areas/
    index.md                # Long-running responsibilities
    <area>.md
  people/
    index.md                # Relationship map
    _template.md
  resources/
    tools.md
    references.md
    prompts.md
    bookmarks-classified.md # Optional
  memory/
    lessons.md
    decisions.md
    daily/
      YYYY-MM-DD.md
  archive/
    README.md
```

## Setup Questions

### who-am-i.md

Ask:

1. What name should assistants use for you?
2. Where are you based, and what timezone should be assumed?
3. What languages do you use or prefer?
4. What are your primary roles right now?
5. What is your professional/personal background?
6. What current life or work context should assistants know?
7. What are you trying to build, become, or optimize for long term?
8. What strengths should assistants lean into?
9. What constraints should assistants respect?
10. What are your non-negotiables?
11. Any sensitive topics requiring extra care?

### preferences.md

Ask:

1. Preferred communication tone?
2. Preferred detail level?
3. Language preference?
4. When should assistants ask questions vs make assumptions?
5. What styles do you dislike?
6. Engineering/work priority order?
7. Research and learning preferences?
8. Tooling defaults?
9. Documentation, file, date, and data-analysis defaults?

### current-focus.md

Ask:

1. Top 3 priorities right now?
2. What should be done this week?
3. Active projects or systems?
4. Waiting on whom or what?
5. Active constraints?
6. What should assistants avoid spending time on?
7. Review cadence?

### principles.md

Ask:

1. Decision rules for important decisions?
2. Execution/work principles?
3. Learning principles?
4. Relationship/team principles?
5. Assistant collaboration principles?

### projects/index.md

Choose one:

- Project goal/status table.
- Repo/path map.
- Hybrid: area/system + path + goal + status.

Ask for project name, path, goal, current status, next action, priority, owner/stakeholders.

### areas/

Common work areas:

- engineering-leadership.md
- security.md
- learning.md
- compliance-systems.md
- ai-agents.md
- career.md

Ask only for areas the user wants to keep.

### people/

Default to minimal. Store person files only when durable context is useful:

- communication preferences
- decision authority
- recurring responsibilities
- open loops
- collaboration history

### resources/

Ask for:

- daily tools
- internal systems
- vendor systems
- documentation defaults
- data-analysis tools
- important links/bookmarks

Classify large bookmark exports by category. Sanitize auth/token-style query parameters.

### memory/

Use `lessons.md` for durable collaboration lessons.
Use `decisions.md` for cross-project harness decisions.
Use `daily/YYYY-MM-DD.md` for raw timeline notes.

## Recommended Categories For Bookmarks

- Production And Internal Systems
- Sandbox Dev And Test
- Observability Incident And Logs
- Compliance KYT And Screening
- Travel Rule
- AI Agents Automation And MCP
- Internal Operations
- Customer Support And Tickets
- Product Requirements And Design
- People HR OKR And Recruiting
- Security And Permission
- Engineering And Technical References
- Learning
- Project Management
- Other Tools And References

## Security Defaults

Capture:

- sensitive information types
- actions requiring confirmation
- whether assistants may read logs/code/configs
- how to handle sensitive findings
- organization-specific risks

Good defaults:

- Do not store secrets, private keys, API tokens, recovery phrases, credentials, or customer-sensitive data.
- Confirm before production writes, permission changes, outbound messages, database changes, deployments, or customer/compliance-impacting actions.
- If sensitive information is found, point to where it exists instead of reproducing it.

## Sync/Mirror Pattern

Use a single source of truth and optional mirror.

Example:

```bash
SOURCE_ROOT="/home/user/assistant-harness"
TARGET_ROOT="/some/local/mirror/assistant-harness"
rsync -a --delete "$SOURCE_ROOT"/ "$TARGET_ROOT"/
```

Make clear that the mirror is not the editable source unless the user decides otherwise.
