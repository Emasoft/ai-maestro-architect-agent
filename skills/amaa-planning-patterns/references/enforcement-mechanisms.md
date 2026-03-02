# Enforcement Mechanisms

## Table of Contents

- 1. Overview of Enforcement
  - 1.1 Why enforcement matters
  - 1.2 Three enforcement mechanisms
- 2. Plan Validation Script (validate_plan.py)
  - 2.1 What it validates
  - 2.2 When to use it
  - 2.3 Usage examples
- 3. Shared Thresholds Module (thresholds.py)
  - 3.1 Task complexity thresholds
  - 3.2 Plan quality thresholds
  - 3.3 When to reference thresholds
- 4. Handoff Protocols
  - 4.1 Required deliverables
  - 4.2 Minimum information requirements
  - 4.3 When to use the checklist
- 5. Integration Workflow
  - 5.1 Recommended validation sequence
  - 5.2 Addressing validation failures

---

## 1. Overview of Enforcement

### 1.1 Why Enforcement Matters

Planning patterns become effective when they are validated and enforced. Without enforcement, plans may:
- Miss required sections
- Contain overly complex tasks
- Have circular dependencies
- Lack clear ownership

### 1.2 Three Enforcement Mechanisms

| Mechanism | Purpose | Location |
|-----------|---------|----------|
| validate_plan.py | Automated quality validation | `scripts/validate_plan.py` |
| thresholds.py | Objective quality criteria | `../shared/thresholds.py` |
| handoff-protocols.md | Deliverable requirements | `../shared/references/handoff-protocols.md` |

---

## 2. Plan Validation Script (validate_plan.py)

**Location**: `scripts/validate_plan.py`

**Usage**:
```bash
python scripts/validate_plan.py --plan plan.md --output validation-report.md
```

**Purpose**: Automated plan quality validation before submission to stakeholders or execution teams.

### 2.1 What It Validates

- All required sections are present (architecture, risks, roadmap, tasks)
- Task complexity stays within defined thresholds
- Dependencies form valid DAG (no circular dependencies)
- Each task has clear owner and success criteria
- Milestones have measurable deliverables
- Risk mitigations are scheduled in roadmap

### 2.2 When to Use It

Before submitting any planning document for approval or before starting execution phase.

### 2.3 Usage Examples

```bash
# Validate a plan and generate report
python scripts/validate_plan.py --plan project-plan.md --output validation.md

# Validate with strict mode (fail on warnings)
python scripts/validate_plan.py --plan project-plan.md --strict

# Validate specific sections only
python scripts/validate_plan.py --plan project-plan.md --sections architecture,tasks
```

---

## 3. Shared Thresholds Module (thresholds.py)

**Location**: `../shared/thresholds.py`

**Purpose**: Standardized, objective criteria for plan quality across all projects.

### 3.1 Task Complexity Thresholds

| Scope Classification | Files Affected | Components Affected |
|---------------------|----------------|---------------------|
| Trivial | 1-2 | 1 |
| Small | 3-5 | 1-2 |
| Medium | 6-10 | 2-3 |
| Large | 11-20 | 4-6 |
| Epic | 21+ | 7+ |

### 3.2 Plan Quality Thresholds

- Maximum dependencies per task
- Minimum buffer capacity percentage
- Risk threshold values (impact x probability scores)
- Team capacity limits (tasks per person)

### 3.3 When to Reference Thresholds

Reference these thresholds when breaking down tasks in implementation planning. The validate_plan.py script automatically checks against these thresholds.

---

## 4. Handoff Protocols

**Location**: `../shared/references/handoff-protocols.md`

**Purpose**: Ensures plans contain everything execution teams need to proceed without blocking on missing information.

### 4.1 Required Deliverables

- Planning document structure requirements
- Minimum information needed for task execution
- Verification evidence format
- Communication requirements
- Acceptance criteria for plan approval

### 4.2 Minimum Information Requirements

For each task handoff, the following must be present:
- Clear task description
- Owner assignment
- Success criteria
- Dependencies
- Estimated effort

### 4.3 When to Use the Checklist

Before declaring planning phase complete. Use the checklist in handoff-protocols.md to verify all required deliverables are ready.

---

## 5. Integration Workflow

### 5.1 Recommended Validation Sequence

1. Complete all four planning phases (architecture, risks, roadmap, tasks)
2. Run `validate_plan.py` on the final plan document
3. Address any validation failures (missing sections, threshold violations)
4. Review against handoff-protocols.md checklist
5. Submit for stakeholder approval only after validation passes

### 5.2 Addressing Validation Failures

| Failure Type | Resolution |
|--------------|------------|
| Missing section | Add the required section content |
| Task too complex | Break into smaller tasks |
| Circular dependency | Remove or restructure dependencies |
| Missing owner | Assign task owner |
| Threshold exceeded | Reduce scope or add resources |

This ensures every plan meets minimum quality standards before execution begins.
