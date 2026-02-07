---
operation: parse-requirements
procedure: proc-route-requirements
workflow-instruction: Step 6 - Requirements to Architect
parent-skill: eaa-requirements-analysis
parent-plugin: emasoft-architect-agent
version: 1.0.0
---

# Parse Requirements Operation

## When to Use

Use this operation when:
- Receiving requirements from user in unstructured text format
- Extracting and categorizing requirements from documentation
- Converting natural language requirements into structured format
- Preparing requirements for tracking in USER_REQUIREMENTS.md

This operation supports RULE 14 (User Requirements Are Immutable) by capturing exact user intent.

## Prerequisites

- [ ] Have user-provided requirements text or file
- [ ] Python 3.8+ available
- [ ] Plugin scripts accessible

## Procedure

### Step 1: Gather Requirements Text

Collect the requirements from:
- User conversation/messages
- Existing documentation
- Meeting notes
- Specification files

### Step 2: Execute Parse Command

From text:
```bash
python3 scripts/eaa_requirement_analysis.py parse --input "The system must support user login with email and password. It should handle session management with JWT tokens."
```

From file:
```bash
python3 scripts/eaa_requirement_analysis.py parse --input path/to/requirements.txt
```

### Step 3: Review Parsed Output

The script outputs structured requirements:
- Functional requirements
- Non-functional requirements
- Constraints
- Assumptions

### Step 4: Document in USER_REQUIREMENTS.md

Transfer parsed requirements to USER_REQUIREMENTS.md, preserving original wording per RULE 14.

## Checklist

Copy this checklist and track your progress:

- [ ] Gather all requirements text from user
- [ ] Execute parse command on requirements
- [ ] Review extracted requirements
- [ ] Verify categorization is correct
- [ ] Document in USER_REQUIREMENTS.md
- [ ] Preserve original user wording (RULE 14)

## Examples

### Example: Parsing User Text

```bash
python3 scripts/eaa_requirement_analysis.py parse --input "The application needs to:
1. Allow users to register with email
2. Support password reset via email link
3. Handle 1000 concurrent users
4. Respond within 200ms for API calls"

# Expected output:
# Parsed Requirements:
#
# FUNCTIONAL:
#   - REQ-F001: Allow users to register with email
#   - REQ-F002: Support password reset via email link
#
# NON-FUNCTIONAL:
#   - REQ-NF001: Handle 1000 concurrent users (Performance)
#   - REQ-NF002: Respond within 200ms for API calls (Performance)
#
# Total: 4 requirements extracted
```

### Example: Parsing from File

```bash
# Create requirements file
cat > /tmp/user_reqs.txt << 'EOF'
The system should authenticate users via OAuth2.
Data must be encrypted at rest using AES-256.
The API should follow REST conventions.
Deployment should be containerized with Docker.
EOF

# Parse the file
python3 scripts/eaa_requirement_analysis.py parse --input /tmp/user_reqs.txt

# Expected output:
# Parsed Requirements:
#
# FUNCTIONAL:
#   - REQ-F001: Authenticate users via OAuth2
#
# NON-FUNCTIONAL:
#   - REQ-NF001: Data encrypted at rest using AES-256 (Security)
#   - REQ-NF002: API follows REST conventions (Architectural)
#   - REQ-NF003: Deployment containerized with Docker (Infrastructure)
```

### Example: Documenting in USER_REQUIREMENTS.md

After parsing, create USER_REQUIREMENTS.md:

```markdown
# User Requirements

## Functional Requirements

### REQ-F001: User Registration
- **Original**: "Allow users to register with email"
- **Category**: Authentication
- **Priority**: High

### REQ-F002: Password Reset
- **Original**: "Support password reset via email link"
- **Category**: Authentication
- **Priority**: Medium

## Non-Functional Requirements

### REQ-NF001: Concurrent Users
- **Original**: "Handle 1000 concurrent users"
- **Category**: Performance
- **Metric**: 1000 concurrent users minimum
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| File not found | Invalid input path | Verify file path exists |
| Empty input | No text provided | Provide requirements text or file |
| Parse error | Malformed text | Simplify input format |
| Script not found | Plugin not loaded | Verify plugin is enabled |

## Related Operations

- [op-init-requirements-tracking.md](op-init-requirements-tracking.md) - Initialize tracking structure
- [op-report-requirement-issue.md](op-report-requirement-issue.md) - Report issues with requirements
- [op-start-planning.md](op-start-planning.md) - Start planning after parsing
