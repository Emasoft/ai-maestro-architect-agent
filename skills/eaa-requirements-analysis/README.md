# Planning Commands Skill

This skill documents all planning phase commands for the Architect Agent plugin.

## Overview

The planning phase is the first stage of the Two-Phase workflow where:
- Requirements are gathered and documented
- Implementation modules are defined
- Acceptance criteria are specified
- The plan is approved before implementation begins

## Directory Structure

```
planning-commands/
├── SKILL.md                 # Main skill documentation (entry point)
├── README.md                # This file
├── references/              # Detailed reference documents
│   ├── start-planning-procedure.md    # /start-planning workflow
│   ├── requirement-management.md      # Add/modify/remove operations
│   ├── plan-approval-transition.md    # /approve-plan + transition
│   ├── state-file-format.md           # State file schema
│   └── troubleshooting.md             # Common issues and solutions
└── scripts/                 # Utility scripts
    ├── check_plan_prerequisites.py    # Verify prerequisites
    ├── export_plan_summary.py         # Export plan as markdown
    └── reset_plan_phase.py            # Reset plan phase
```

## Commands Documented

| Command | Description |
|---------|-------------|
| `/start-planning` | Enter Plan Phase Mode |
| `/planning-status` | View requirements progress |
| `/add-requirement` | Add requirement or module |
| `/modify-requirement` | Change requirement specs |
| `/remove-requirement` | Remove pending requirement |
| `/approve-plan` | Transition to Orchestration Phase |

## Usage

1. Read `SKILL.md` for an overview and quick reference
2. Follow TOC links to reference documents for detailed procedures
3. Use utility scripts for common operations

## Scripts

### check_plan_prerequisites.py
Verifies all prerequisites are met before running `/approve-plan`.
```bash
python3 scripts/check_plan_prerequisites.py --fix-suggestions
```

### export_plan_summary.py
Exports the current plan as a formatted markdown summary.
```bash
python3 scripts/export_plan_summary.py --output plan-summary.md
```

### reset_plan_phase.py
Safely resets the plan phase with automatic backup.
```bash
python3 scripts/reset_plan_phase.py --confirm
```

## Dependencies

- Python 3.10+
- PyYAML (`pip install pyyaml`)
- GitHub CLI (`gh`) for issue creation

## Related

- Main plugin: `architect-agent`
- Parent scripts: `${CLAUDE_PLUGIN_ROOT}/scripts/eaa_*.py`
- Next phase: Use `orchestration-commands` skill after plan approval
