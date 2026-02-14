---
procedure: support-skill
workflow-instruction: support
---

# Operation: Write Process Documentation


## Contents

- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Inputs](#inputs)
- [Procedure](#procedure)
  - [Step 1: Gather Process Information](#step-1-gather-process-information)
  - [Step 2: Create Process Documentation](#step-2-create-process-documentation)
- [Overview](#overview)
  - [Purpose](#purpose)
  - [Scope](#scope)
  - [Trigger Events](#trigger-events)
- [Roles and Responsibilities](#roles-and-responsibilities)
  - [RACI Matrix](#raci-matrix)
- [Process Flow](#process-flow)
  - [Diagram](#diagram)
  - [Detailed Steps](#detailed-steps)
- [Tools and Systems](#tools-and-systems)
- [Inputs and Outputs](#inputs-and-outputs)
  - [Process Inputs](#process-inputs)
  - [Process Outputs](#process-outputs)
- [Service Level Agreements](#service-level-agreements)
- [Exception Handling](#exception-handling)
  - [Exception 1: <Exception Type>](#exception-1-exception-type)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [Related Processes](#related-processes)
- [Revision History](#revision-history)
  - [Step 3: Apply Quality Check (6 C's)](#step-3-apply-quality-check-6-cs)
  - [Step 4: Save Document](#step-4-save-document)
- [Output](#output)
- [Verification Checklist](#verification-checklist)
- [Error Handling](#error-handling)

## Purpose

Write process documentation that describes workflow steps, responsibilities, tools, and best practices for a technical or organizational process.

## When to Use

- Documenting a new workflow or process
- Standardizing an existing process
- Onboarding documentation

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Process name | Assignment | Yes |
| Process steps | Analysis | Yes |
| Roles involved | Analysis | Yes |

## Procedure

### Step 1: Gather Process Information

Collect:
- Process name and purpose
- Trigger events (what starts the process)
- Steps and sequence
- Roles and responsibilities
- Tools used
- Inputs and outputs
- Exceptions and edge cases

### Step 2: Create Process Documentation

Use this template:

```markdown
# Process: <Process Name>

**Version:** 1.0
**Owner:** <Role/Name>
**Last Updated:** YYYY-MM-DD
**Review Cycle:** Quarterly

---

## Overview

### Purpose

<Why does this process exist? What problem does it solve?>

### Scope

**In Scope:**
- <What this process covers>

**Out of Scope:**
- <What this process does NOT cover>

### Trigger Events

This process is initiated when:
- <Trigger event 1>
- <Trigger event 2>

---

## Roles and Responsibilities

| Role | Responsibilities |
|------|-----------------|
| <Role 1> | <What they do in this process> |
| <Role 2> | <What they do in this process> |

### RACI Matrix

| Step | <Role 1> | <Role 2> | <Role 3> |
|------|----------|----------|----------|
| Step 1 | R | A | C |
| Step 2 | A | R | I |

**R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

---

## Process Flow

### Diagram

```
[Start] → [Step 1] → [Decision?]
                          ↓ Yes
                     [Step 2] → [Step 3] → [End]
                          ↓ No
                     [Alternative] → [End]
```

### Detailed Steps

#### Step 1: <Step Name>

**Responsible:** <Role>
**Duration:** <Estimated time>

**Description:**
<What happens in this step>

**Inputs:**
- <Input required for this step>

**Actions:**
1. <Action 1>
2. <Action 2>
3. <Action 3>

**Outputs:**
- <Output produced by this step>

**Tools:**
- <Tool used>

**Decision Point:** <If applicable, what decision is made?>

---

#### Step 2: <Step Name>

<Same structure as above>

---

## Tools and Systems

| Tool | Purpose | Access |
|------|---------|--------|
| <Tool 1> | <What it's used for> | <How to get access> |
| <Tool 2> | <What it's used for> | <How to get access> |

---

## Inputs and Outputs

### Process Inputs

| Input | Source | Format |
|-------|--------|--------|
| <Input 1> | <Where it comes from> | <Format> |

### Process Outputs

| Output | Destination | Format |
|--------|-------------|--------|
| <Output 1> | <Where it goes> | <Format> |

---

## Service Level Agreements

| Metric | Target |
|--------|--------|
| Process completion time | < X hours |
| Quality threshold | > Y% |

---

## Exception Handling

### Exception 1: <Exception Type>

**Situation:** <When this exception occurs>

**Resolution:**
1. <Step to resolve>
2. <Step to resolve>

**Escalation:** <Who to escalate to>

---

## Best Practices

- <Best practice 1>
- <Best practice 2>
- <Best practice 3>

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| <Common mistake> | <How to avoid it> |

---

## Related Processes

- [Related Process 1](link)
- [Related Process 2](link)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial version |
```

### Step 3: Apply Quality Check (6 C's)

- [ ] **Complete**: All steps documented
- [ ] **Correct**: Steps match actual process
- [ ] **Clear**: No ambiguous instructions
- [ ] **Consistent**: Same terminology throughout
- [ ] **Current**: Reflects current process
- [ ] **Connected**: Links to related docs

### Step 4: Save Document

Save to: `/docs/workflows/<process-name>.md`

## Output

| File | Location |
|------|----------|
| Process documentation | `/docs/workflows/<process-name>.md` |

## Verification Checklist

- [ ] Purpose clearly stated
- [ ] Roles and responsibilities defined
- [ ] All steps documented with actions
- [ ] Tools listed
- [ ] Inputs and outputs specified
- [ ] Exceptions handled
- [ ] 6 C's quality check passed

## Error Handling

| Error | Solution |
|-------|----------|
| Process owner unclear | Escalate to management |
| Steps missing | Interview process participants |
| Conflicting information | Validate with multiple sources |
