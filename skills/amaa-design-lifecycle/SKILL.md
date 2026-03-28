---
name: amaa-design-lifecycle
description: Use when managing design document states or lifecycle transitions, including project repo setup and inter-agent handoff. Trigger with design lifecycle or state transition request.
context: fork
agent: ai-maestro-architect-agent-main-agent
user-invocable: false
---

# Design Lifecycle Skill

## Overview

Manages the complete lifecycle of design documents: creation, review, approval, implementation tracking, and archival. Enforces valid state transitions (DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED) and generates handoff documents for implementers.

## Checklist

Copy this checklist and track your progress:
- [ ] Receive project requirements from COS or MANAGER
- [ ] Discover existing repos: `amp-project-repos.sh --team <teamId>`
- [ ] Clone main repo: `amp-clone-repo.sh <url>`
- [ ] Research APIs/technologies
- [ ] Create design documents in `docs_dev/design/`
- [ ] Generate design UUID and register in index with state DRAFT
- [ ] Write design document (architecture, components, interfaces)
- [ ] Complete design and validate checklist
- [ ] Push design doc to the repo
- [ ] Submit for review (state: REVIEW)
- [ ] Address review comments
- [ ] Update state to APPROVED
- [ ] Create GitHub issues for each component
- [ ] Create handoff document for AMOA
- [ ] Notify orchestrator: `amp-send.sh <orchestrator> "Design Complete"` with repo URL, doc path, N components, M tasks
- [ ] Report completion to AMCOS
- [ ] Track implementation progress
- [ ] Archive when complete (state: ARCHIVED)
- [ ] (If needed) Create new repo: `amp-create-repo.sh <name> [--org <org>]`

## Prerequisites

- Write access to `docs_dev/design/` directory for design documents
- Design scripts available at `${CLAUDE_PLUGIN_ROOT}/scripts/amaa_design_*.py`

## Instructions

1. Receive project requirements from COS or MANAGER
2. Discover existing repos: `amp-project-repos.sh --team <teamId>` to understand the project landscape
3. Clone the main repo: `amp-clone-repo.sh <url>` (or create a new one: `amp-create-repo.sh <name> [--org <org>] [--private] [--description "..."]`)
4. Research APIs/technologies and create design documents in `docs_dev/design/`
5. Generate design UUID and register in index with state DRAFT
6. Write design document covering architecture, components, and interfaces
7. Push design doc to the repo
8. Complete design, validate checklist, submit for review (state: REVIEW)
9. Address review comments, update state to APPROVED
10. Create GitHub issues for each component (one issue per module/service/interface)
11. Create handoff document for AMOA
12. Notify the orchestrator of design completion:
    ```bash
    amp-send.sh <orchestrator> "Design Complete" \
      "Repo: <repo-url>, Doc: <doc-path>, Components: N, Tasks: M"
    ```
13. Report completion to AMCOS
14. Track implementation progress, archive when complete (state: ARCHIVED)

## AI Maestro Project Scripts

These scripts are available from the AI Maestro `scripts/` directory (installed to `~/.local/bin/` on setup):

| Script | Purpose | Usage |
|--------|---------|-------|
| `amp-project-repos.sh` | List repositories for the team's project | `amp-project-repos.sh --team <teamId>` |
| `amp-clone-repo.sh` | Clone a repo into the agent's working directory | `amp-clone-repo.sh <url> [<localName>]` |
| `amp-create-repo.sh` | Create a new GitHub repo and register it with the team | `amp-create-repo.sh <name> [--org <org>] [--private]` |
| `amp-send.sh` | Send inter-agent messages (design handoff notifications) | `amp-send.sh <agent> <subject> <message>` |

## Reference Documents

| Reference | Description |
|-----------|-------------|
| [procedures.md](references/procedures.md) | PROCEDURE 1: Create New Design, PROCEDURE 2: Submit for Review, PROCEDURE 3: Approve Design, PROCEDURE 4: Track Implementation, PROCEDURE 5: Complete and Archive |
| [design-states.md](references/design-states.md) | State Definitions |
| [examples.md](references/examples.md) | Example 1: Design Real-Time Collaborative Editor, Example 2: Design Stripe Payment Integration, Example 3: Create and Submit Design for Review (Lifecycle), Example 4: Approve and Track Implementation (Lifecycle) |
| [scripts.md](references/scripts.md) | Script Reference |
| [rule-14-enforcement.md](references/rule-14-enforcement.md) | 1 When handling user requirements in any workflow, 2 When detecting potential requirement deviations, 3 When a technical constraint conflicts with a requirement, 4 When documenting requirement compliance |

## Examples

```
User: Design architecture for a real-time collaborative editor.
AMAA: Research (OT vs CRDT) -> Requirements -> Architecture (Y.js + Socket.io)
      -> Module breakdown (5 modules) -> Handoff document for AMOA
Output: docs_dev/design/{requirements,architecture,handoff-<uuid>}.md
```

## Error Handling

| Error | Solution |
|-------|----------|
| Invalid state transition | Follow valid path: DRAFT->REVIEW->APPROVED->IMPLEMENTING->COMPLETED->ARCHIVED |
| Missing UUID | Generate UUID before registration |
| Index conflict | Use unique timestamp-based UUIDs |
| Unresolved review comments | Resolve all comments before approval |

## Output

| Output Type | Location |
|-------------|----------|
| Design documents | `docs_dev/design/` |
| Handoff documents | `docs_dev/design/handoff-{uuid}.md` |
| Design index entry | `design/requirements/index.json` |

## Resources

- `templates/design-template.md` - Design document template
- amaa-requirements-analysis - Requirements input skill
- amaa-planning-patterns - Planning integration skill
