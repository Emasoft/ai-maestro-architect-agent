---
name: amaa-design-management-ops
description: "Use when validating design documents or troubleshooting issues. Trigger with design management ops request. Loaded by ai-maestro-architect-agent-main-agent"
context: fork
user-invocable: false
agent: ai-maestro-architect-agent-main-agent
---

# Design Document Management (Operations)

## Overview

Covers validation, troubleshooting, and quick reference for design document management. Use after documents are created to ensure compliance and resolve issues.

## Prerequisites

- Python 3.10+ and the `design/` directory structure exists

## Instructions

1. Validate documents using `amaa_design_validate.py`
2. Review errors/warnings and resolve using troubleshooting guide
3. Use quick reference for common command patterns

## Checklist

Copy this checklist and track your progress:

- [ ] Validate single file or all files with `amaa_design_validate.py`
- [ ] Review and fix any validation errors or warnings
- [ ] Consult troubleshooting guide for persistent issues
- [ ] Use quick reference for command syntax

## Reference Documents

| Document | Content |
|----------|---------|
| [validating-documents.md](references/validating-documents.md) | Single File Validation, Bulk Validation, Understanding Errors, Understanding Warnings, Error Resolution, Required Frontmatter Fields, Script Reference |
| [troubleshooting.md](references/troubleshooting.md) | UUID Generation Issues, Creation Failures, Search Issues, Frontmatter Parsing Issues, Directory Structure Issues, Permission Issues, Encoding Issues |
| [quick-reference.md](references/quick-reference.md) | Quick Reference Commands, Document Status Workflow, Frontmatter Reference, Directory Structure, Extended Examples |

## Examples

Example: `python scripts/amaa_design_validate.py --all` validates all design documents and reports errors.

## Error Handling

| Issue | Fix |
|-------|-----|
| Validation: malformed frontmatter | Fix YAML delimiters and field formatting |
| Files in wrong directory | Move to correct `design/<type>/` subdirectory |
| Encoding errors | Ensure files are UTF-8 encoded |

## Output

| Type | Description |
|------|-------------|
| Validation Report | Error list with file paths and line numbers |
| Quick Reference | Command patterns for common operations |

## Resources

See Reference Documents table above.
