# RULE 14: User Requirements Are Immutable

## Table of Contents

- 1. Planning Phase Requirement Check
  - 1.1 Loading USER_REQUIREMENTS.md
  - 1.2 Requirement Feasibility Analysis
  - 1.3 Handling Issues Found
- 2. Plan Structure Requirements
  - 2.1 Requirement Compliance Table
- 3. Forbidden Planning Actions
  - 3.1 Actions that violate requirement immutability
- 4. Correct Planning Approach
  - 4.1 Actions that respect requirement immutability

---

## 1. Planning Phase Requirement Check

BEFORE creating any implementation plan, complete these steps:

### 1.1 Loading USER_REQUIREMENTS.md

1. Parse all user requirements
2. Note exact user quotes
3. Identify technology constraints

### 1.2 Requirement Feasibility Analysis

Answer these questions:
- Can requirements be implemented as specified?
- Any conflicts between requirements?
- Any ambiguities needing clarification?

### 1.3 Handling Issues Found

If issues are found:
1. **STOP** planning
2. Generate Requirement Issue Report
3. Present alternatives to user
4. **WAIT** for user decision
5. Resume planning only after user decides

---

## 2. Plan Structure Requirements

Every implementation plan MUST include a Requirement Compliance section.

### 2.1 Requirement Compliance Table

```markdown
## Requirement Compliance
| Requirement | User Statement | Plan Addresses | Status |
|-------------|----------------|----------------|--------|
| REQ-001 | "[exact quote from user]" | [how plan addresses it] | ✅/❌ |
| REQ-002 | "[exact quote from user]" | [how plan addresses it] | ✅/❌ |
```

This table traces every plan element back to a user requirement.

---

## 3. Forbidden Planning Actions

### 3.1 Actions That Violate Requirement Immutability

These actions are forbidden during planning:

| Forbidden Action | Why It Is Forbidden |
|-----------------|---------------------|
| Planning for different technology than user specified | User requirements are immutable |
| Reducing scope in the plan | Changes must be approved by user first |
| Adding features user did not request | Scope creep without approval |
| Assuming user would approve changes | Only explicit approval counts |

---

## 4. Correct Planning Approach

### 4.1 Actions That Respect Requirement Immutability

| Correct Action | Description |
|---------------|-------------|
| Plan implements exactly what user specified | No deviations from requirements |
| Plan flags requirement issues BEFORE implementation | Early warning, not silent changes |
| Plan traces every step to a user requirement | Full traceability |
| Plan waits for user decision on conflicts | No assumptions about user preferences |
