# Design Lifecycle Scripts

## Table of Contents

- Script Reference

## Script Reference

All scripts are located at `../../scripts/` relative to this skill.

| Script | Purpose | Usage |
|--------|---------|-------|
| `amaa_design_lifecycle.py` | Manage design document state transitions | `python scripts/amaa_design_lifecycle.py --uuid <UUID> --transition <STATE>` |
| `amaa_design_transition.py` | Validate and execute state transitions | `python scripts/amaa_design_transition.py --from <STATE> --to <STATE>` |
| `amaa_design_uuid.py` | Generate UUIDs for new design documents | `python scripts/amaa_design_uuid.py --type <DOC_TYPE>` |
| `amaa_design_version.py` | Track document versions | `python scripts/amaa_design_version.py --uuid <UUID> --bump` |
| `amaa_design_export.py` | Export design documents to various formats | `python scripts/amaa_design_export.py --uuid <UUID> --format <FORMAT>` |
| `amaa_design_handoff.py` | Generate handoff documents for AMOA | `python scripts/amaa_design_handoff.py --design <UUID> --target eoa` |
| `amaa_init_design_folders.py` | Initialize design folder structure | `python scripts/amaa_init_design_folders.py --project-root <PATH>` |
