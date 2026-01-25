# Documentation Writing Workflow

Step-by-step procedure for creating documentation.

---

## Table of Contents

- 1. Step 1: Receive and Parse Assignment
- 2. Step 2: Gather Context
- 3. Step 3: Create Document Structure
- 4. Step 4: Write Core Content
- 5. Step 5: Add Cross-References
- 6. Step 6: Quality Check
- 7. Step 7: Commit and Report

---

## 1. Step 1: Receive and Parse Assignment

**Action**: Read the orchestrator's task assignment and identify:
- Document type (spec, ADR, API contract, workflow, etc.)
- Input sources (files, meeting notes, requirements)
- Output location and file name
- Stakeholders who will use this document

**Verification Step 1**: Confirm that:
- [ ] You can access all input files
- [ ] You understand the deliverable format

---

## 2. Step 2: Gather Context

**Action**: Read all referenced input documents, prior decisions, and related specifications
- Review existing documentation for terminology consistency
- Check glossary for standard terms
- Identify dependencies and integration points

**Verification Step 2**: Confirm that:
- [ ] All key concepts have been identified
- [ ] Standard terms have been catalogued
- [ ] Dependencies are documented

---

## 3. Step 3: Create Document Structure

**Action**: Set up the document skeleton using appropriate template
- Add frontmatter (title, date, version, status)
- Create section headers per template
- Add placeholder text for each section

**Verification Step 3**: Confirm that:
- [ ] Structure matches the appropriate template
- [ ] All required sections are included
- [ ] Placeholder text is in place for each section

---

## 4. Step 4: Write Core Content

**Action**: Fill in each section with detailed, actionable content
- Write clear, unambiguous prose
- Add concrete examples for abstract concepts
- Include diagrams where relationships are complex
- Document edge cases and error scenarios

**Verification Step 4**: Confirm that:
- [ ] Each section has concrete examples
- [ ] No undefined terms exist
- [ ] No ambiguous statements remain
- [ ] Edge cases are documented

---

## 5. Step 5: Add Cross-References

**Action**: Link related documents and update navigation
- Add links to dependencies, related specs, ADRs
- Update parent README with link to new document
- Update glossary if new terms introduced
- Check all links are valid

**Verification Step 5**: Confirm that:
- [ ] All links are valid and working
- [ ] Document is discoverable from main index
- [ ] Glossary has been updated if needed
- [ ] Parent README contains link to new document

---

## 6. Step 6: Quality Check

**Action**: Review against quality standards
- Run through self-check checklist
- Verify all required sections present
- Check terminology consistency with glossary
- Ensure examples are complete and correct
- Add "Last Updated" timestamp

**Verification Step 6**: Confirm that:
- [ ] All quality checklist items pass
- [ ] No TBD/TODO markers remain
- [ ] Terminology is consistent with glossary
- [ ] "Last Updated" timestamp is added

---

## 7. Step 7: Commit and Report

**Action**: Save file to specified location and notify orchestrator
- Commit file to repository with descriptive message
- Generate minimal completion report
- Send report to orchestrator

**Verification Step 7**: Confirm that:
- [ ] File is committed to correct path
- [ ] Commit message is descriptive
- [ ] Completion report is generated
- [ ] Orchestrator has received the report

---

## Output Format

**Success Report:**
```
[DONE] documentation-writer - <document-type> created
Files: <filepath1>, <filepath2>
Word count: <total-words> | Examples: <count> | Cross-refs: <count>
```

**Failure Report:**
```
[FAILED] documentation-writer - <reason>
Issue: <specific-problem>
Requires: <what-is-needed-to-proceed>
```

**CRITICAL**: Do NOT return verbose output or full document content to orchestrator.
