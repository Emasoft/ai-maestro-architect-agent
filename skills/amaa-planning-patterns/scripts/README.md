# Planning Patterns Scripts

This directory contains Python scripts to automate the generation of planning documents and templates.

## Scripts Overview

All scripts are Python 3.8+ compatible and have no external dependencies (use standard library only).

### 1. generate_planning_checklist.py

Generates a customized planning checklist for your project.

**Usage**:
```bash
python scripts/generate_planning_checklist.py \
  --project "ProjectName" \
  --phases 4 \
  --output checklist.md
```

**Arguments**:
- `--project` (required): Name of your project
- `--phases` (optional): Number of phases (default: 4)
- `--output` (optional): Output file path (default: checklist-{date}.md)

**Output**: Markdown file with customized planning checklist

**Example**:
```bash
python scripts/generate_planning_checklist.py \
  --project "UserAuthSystem" \
  --phases 3 \
  --output planning-checklist.md
```

### 2. generate_risk_register.py

Generates an empty risk register template in multiple formats.

**Usage**:
```bash
python scripts/generate_risk_register.py \
  --template excel \
  --risks 20 \
  --output risks.xlsx
```

**Arguments**:
- `--template` (optional): Format (excel, csv, json, markdown) (default: markdown)
- `--risks` (optional): Number of risk rows to pre-allocate (default: 20)
- `--output` (optional): Output file path (default: risk-register.{ext})

**Output**: Empty risk register ready to fill in

**Example**:
```bash
# Create Excel template
python scripts/generate_risk_register.py \
  --template excel \
  --risks 25 \
  --output project-risks.xlsx

# Create markdown template
python scripts/generate_risk_register.py \
  --template markdown \
  --output risk-register.md
```

### 3. generate_roadmap_template.py

Generates a milestone-based roadmap template (NO TIME ESTIMATIONS).

**Usage**:
```bash
python scripts/generate_roadmap_template.py \
  --phases 5 \
  --output roadmap.md
```

**Arguments**:
- `--phases` (optional): Number of phases (default: 4)
- `--output` (optional): Output file path (default: roadmap.md)

**Output**: Milestone-based roadmap template with phases (no time estimations)

**Example**:
```bash
python scripts/generate_roadmap_template.py \
  --phases 4 \
  --output project-roadmap.md
```

### 4. generate_task_tracker.py

Generates a task tracking spreadsheet template.

**Usage**:
```bash
python scripts/generate_task_tracker.py \
  --phases 4 \
  --tasks-per-phase 8 \
  --output task-tracker.csv
```

**Arguments**:
- `--phases` (optional): Number of phases (default: 4)
- `--tasks-per-phase` (optional): Tasks per phase for pre-allocation (default: 8)
- `--output` (optional): Output file path (default: task-tracker.csv)
- `--format` (optional): Format (csv, json, markdown) (default: csv)

**Output**: Task tracking spreadsheet with columns for ID, name, owner, dates, status

**Example**:
```bash
python scripts/generate_task_tracker.py \
  --phases 5 \
  --tasks-per-phase 10 \
  --output my-tasks.csv
```

### 5. generate_status_report.py

Generates a weekly status report template.

**Usage**:
```bash
python scripts/generate_status_report.py \
  --project "ProjectName" \
  --output status-report.md
```

**Arguments**:
- `--project` (optional): Project name (default: "Project")
- `--output` (optional): Output file path (default: status-report-{date}.md)
- `--team-size` (optional): Number of team members (default: 1)

**Output**: Status report template ready to fill in weekly

**Example**:
```bash
python scripts/generate_status_report.py \
  --project "UserAuthSystem" \
  --team-size 5 \
  --output weekly-status.md
```

## Running the Scripts

### Prerequisites

- Python 3.8 or higher
- No external packages required (uses standard library only)

### Command Line Usage

Each script has help available:
```bash
python scripts/generate_planning_checklist.py --help
python scripts/generate_risk_register.py --help
python scripts/generate_roadmap_template.py --help
python scripts/generate_task_tracker.py --help
python scripts/generate_status_report.py --help
```

### Batch Generation

Generate all templates at once for a new project:
```bash
#!/bin/bash

PROJECT_NAME="MyProject"

python scripts/generate_planning_checklist.py --project "$PROJECT_NAME" --output checklist.md
python scripts/generate_risk_register.py --template markdown --output risks.md
python scripts/generate_roadmap_template.py --phases 4 --output roadmap.md
python scripts/generate_task_tracker.py --phases 4 --output tasks.csv
python scripts/generate_status_report.py --project "$PROJECT_NAME" --output status-template.md

echo "All planning templates generated successfully!"
```

## Output Files

Scripts generate plain text files (markdown, CSV, JSON) that are:
- Easy to version control (git friendly)
- Easy to edit in any text editor
- Easy to convert to other formats
- Printable for stakeholder review

### File Naming Conventions

Scripts follow naming convention: `{template}-{date}.{extension}`

Examples:
- `checklist-2025-12-29.md`
- `risk-register-2025-12-29.xlsx`
- `roadmap.md`
- `task-tracker-phase1.csv`

You can override with `--output` argument.

## Integration with Planning Workflow

### Typical workflow:

1. **Create base templates** (initial phase):
   ```bash
   python scripts/generate_planning_checklist.py --project "MyProject"
   python scripts/generate_risk_register.py --template markdown
   python scripts/generate_roadmap_template.py --phases 4
   python scripts/generate_task_tracker.py --phases 4
   ```

2. **Fill in templates** (planning phase):
   - Architecture Design: Use architecture template from `references/architecture-design.md`
   - Risk Identification: Fill in `risk-register.md`
   - Roadmap Creation: Fill in `roadmap.md`
   - Implementation Planning: Fill in `task-tracker.csv`

3. **Monitor progress** (execution phase):
   - Generate fresh status reports as needed: `generate_status_report.py`
   - Update task tracker with actual progress
   - Update risk register with new risks

## Troubleshooting

### Script not found

```bash
# Make sure you are in the scripts directory
cd /path/to/planning-patterns/scripts

# Or use full path
python /path/to/planning-patterns/scripts/generate_planning_checklist.py
```

### Python version error

Scripts require Python 3.8+. Check your Python version:
```bash
python --version
# or
python3 --version
```

### File permission denied

Make scripts executable:
```bash
chmod +x generate-*.py
```

### Cannot write to output file

Check directory exists and is writable:
```bash
# Create output directory if needed
mkdir -p output/planning

# Run script with output in that directory
python scripts/generate_planning_checklist.py --output output/planning/checklist.md
```

## Script Documentation

Each script has inline documentation and can be read to understand:
- Exact template structure it generates
- All available options
- Usage examples

```bash
# View script source
cat scripts/generate_planning_checklist.py
```

## Contributing

To add new scripts or modify existing ones:
1. Keep scripts simple (no external dependencies)
2. Support `--help` flag
3. Support `--output` flag for file location
4. Generate plain text files (markdown, CSV, JSON)
5. Include usage examples in this README

## Version Information

- Script compatibility: Python 3.8+
- Last updated: 2025-12-29
- All scripts tested with Python 3.12

---

For questions about planning patterns, see the skill references in the `references/` folder.
