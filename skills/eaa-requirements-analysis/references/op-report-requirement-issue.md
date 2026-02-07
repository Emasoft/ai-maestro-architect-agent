---
operation: report-requirement-issue
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Report Requirement Issue Operation

## When to Use

Use this operation when:
- Identifying potential issues with requirements before implementation
- Discovering feasibility problems with a requirement
- Finding ambiguity that needs user clarification
- Detecting conflicts between requirements
- Scope concerns that need user decision

This operation enforces RULE 14 (User Requirements Are Immutable): requirements cannot be modified without explicit user approval.

## Prerequisites

- [ ] Requirements tracking initialized (`docs_dev/requirements/` exists)
- [ ] Requirement ID identified
- [ ] Issue type categorized
- [ ] Issue description prepared

## Procedure

### Step 1: Identify Issue Type

| Issue Type | When to Use |
|------------|-------------|
| Feasibility | Technical or resource constraints make requirement difficult |
| Ambiguity | Requirement text is unclear or open to interpretation |
| Conflict | Requirement contradicts another requirement |
| Scope | Requirement may be out of scope or too broad |

### Step 2: Execute Report Command

```bash
python3 scripts/eaa_requirement_analysis.py report \
  --project-root . \
  --requirement-id REQ-001 \
  --requirement-text "Original requirement text" \
  --issue-type Feasibility \
  --description "Description of the issue"
```

### Step 3: Review Generated Report

```bash
cat docs_dev/requirements/issues/REQ-001-issue.md
```

### Step 4: Present to User

Present the issue report to the user with alternatives. Wait for explicit user decision before proceeding.

## Checklist

Copy this checklist and track your progress:

- [ ] Identify requirement with issue
- [ ] Categorize issue type
- [ ] Document issue description
- [ ] Execute report command
- [ ] Review generated issue report
- [ ] Present alternatives to user
- [ ] Record user decision in report
- [ ] Only modify requirement after user approval

## Examples

### Example: Reporting Feasibility Issue

```bash
python3 scripts/eaa_requirement_analysis.py report \
  --project-root . \
  --requirement-id REQ-F003 \
  --requirement-text "System must support real-time video processing for 10000 concurrent streams" \
  --issue-type Feasibility \
  --description "Current infrastructure cannot support 10000 concurrent video streams. Maximum feasible with available resources is approximately 500 streams."

# Expected output:
# Requirement Issue Report created: docs_dev/requirements/issues/REQ-F003-issue.md
#
# Issue Summary:
#   Requirement: REQ-F003
#   Type: Feasibility
#   Status: Pending User Decision
#
# RULE 14 REMINDER: User requirements are immutable.
# Present this report to the user and await explicit decision.
```

### Example: Generated Issue Report

```markdown
# Requirement Issue Report

## Issue Details
- **Requirement ID**: REQ-F003
- **Requirement Text**: System must support real-time video processing for 10000 concurrent streams
- **Issue Type**: Feasibility
- **Reported Date**: 2026-01-15

## Issue Description
Current infrastructure cannot support 10000 concurrent video streams. Maximum feasible with available resources is approximately 500 streams.

## Proposed Alternatives
1. Reduce concurrent stream requirement to 500
2. Scale infrastructure (cost estimate: $X/month)
3. Implement queue-based processing for overflow
4. No change - accept as-is (will require significant infrastructure investment)

## User Decision
- **Decision**: [PENDING]
- **Rationale**:
- **Decided Date**:

## Impact
- Affects: video-processing module
- Related requirements: REQ-NF001 (performance)
```

### Example: Reporting Ambiguity Issue

```bash
python3 scripts/eaa_requirement_analysis.py report \
  --project-root . \
  --requirement-id REQ-F007 \
  --requirement-text "Users should be able to export data easily" \
  --issue-type Ambiguity \
  --description "Requirement does not specify: what data, what formats, what 'easily' means, or performance expectations."
```

### Example: Reporting Conflict

```bash
python3 scripts/eaa_requirement_analysis.py report \
  --project-root . \
  --requirement-id REQ-NF002 \
  --requirement-text "All API responses must be under 50ms" \
  --issue-type Conflict \
  --description "Conflicts with REQ-F010 which requires complex data aggregation. Aggregation query alone takes 200ms minimum."
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Issues folder not found | Tracking not initialized | Run init operation first |
| Invalid issue type | Unknown type | Use: Feasibility, Ambiguity, Conflict, or Scope |
| Missing required field | Incomplete command | Provide all required arguments |
| Script not found | Plugin not loaded | Verify plugin is enabled |

## Related Operations

- [op-init-requirements-tracking.md](op-init-requirements-tracking.md) - Initialize tracking first
- [op-parse-requirements.md](op-parse-requirements.md) - Parse requirements to identify issues
- [op-validate-implementation.md](op-validate-implementation.md) - Validate after user decision
