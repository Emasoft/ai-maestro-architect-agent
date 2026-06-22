# Design Lifecycle Procedures


## Table of Contents

- PROCEDURE 1: Create New Design
- PROCEDURE 2: Submit for Review
- PROCEDURE 3: Approve Design
- PROCEDURE 4: Track Implementation
- PROCEDURE 5: Complete and Archive

## PROCEDURE 1: Create New Design

1. Generate design UUID
2. Create design document from template
3. Set state to DRAFT
4. Register in design index
5. Notify stakeholders

## PROCEDURE 2: Submit for Review

1. Validate completeness checklist
2. Update state to REVIEW
3. Create review request
4. Assign reviewers
5. Track review comments

## PROCEDURE 3: Approve Design

1. Verify all review comments resolved
2. Update state to APPROVED
3. Create implementation tasks — incl. the AI-Maestro kanban `epic` + first-level children (see op-create-kanban-epic); capture the epic id
4. Notify implementers — the design-handoff message carries the epic id as `aimaestro_task_id` (see op-send-ai-maestro-message / ai-maestro-message-templates §1.3–1.4)
5. Link to GitHub Issues

## PROCEDURE 4: Track Implementation

1. Monitor implementation progress — query the epic's child tasks across the 14-stage pipeline (see op-query-kanban-progress)
2. Update design if changes needed
3. Maintain requirements traceability
4. Document deviations

## PROCEDURE 5: Complete and Archive

1. Verify all requirements implemented
2. Update state to COMPLETED
3. Archive to historical folder
4. Update design index
5. Create completion report
