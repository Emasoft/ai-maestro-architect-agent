---
procedure: support-skill
workflow-instruction: support
---

# Operation: Perform 6 C's Quality Check

## Purpose

Verify documentation quality against the 6 C's framework: Complete, Correct, Clear, Consistent, Current, and Connected.

## When to Use

- Before finalizing any documentation
- During documentation review
- When updating existing documentation

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Document to review | File path | Yes |
| Document type | Assignment | Yes |
| Related docs | Context | Helpful |

## Procedure

### Step 1: Complete Check

Verify the document covers all required aspects.

**Checklist by Document Type:**

**Module Specification:**
- [ ] Purpose stated
- [ ] All public interfaces documented
- [ ] Dependencies listed
- [ ] Configuration documented
- [ ] Error handling explained
- [ ] Usage examples provided

**API Contract:**
- [ ] All endpoints documented
- [ ] Request/response schemas complete
- [ ] Authentication explained
- [ ] Error codes listed
- [ ] Rate limits documented

**ADR:**
- [ ] Context provided
- [ ] Decision clearly stated
- [ ] Alternatives documented (at least 2)
- [ ] Consequences listed (positive and negative)
- [ ] Status set

**Feature Specification:**
- [ ] User stories with acceptance criteria
- [ ] Functional requirements
- [ ] Non-functional requirements
- [ ] Technical considerations

### Step 2: Correct Check

Verify technical accuracy.

**Verification Actions:**
- [ ] Code examples compile/run correctly
- [ ] API endpoints match implementation
- [ ] Configuration values are valid
- [ ] File paths exist
- [ ] Version numbers are accurate
- [ ] Links are not broken

```bash
# Verify links in markdown file
grep -oE '\[.*\]\(.*\)' document.md | while read link; do
  url=$(echo "$link" | sed 's/.*(\(.*\))/\1/')
  if [[ $url == http* ]]; then
    curl -s -o /dev/null -w "%{http_code}" "$url"
  elif [[ -f "$url" ]]; then
    echo "OK: $url"
  else
    echo "BROKEN: $url"
  fi
done
```

### Step 3: Clear Check

Verify unambiguous language.

**Look for:**
- [ ] No vague terms ("might", "could", "possibly")
- [ ] No undefined acronyms
- [ ] No jargon without explanation
- [ ] Active voice used
- [ ] One idea per sentence
- [ ] Short paragraphs

**Ambiguous Language to Flag:**
| Avoid | Replace With |
|-------|--------------|
| "It" (unclear referent) | Specific noun |
| "This" (without noun) | "This configuration" |
| "Some" | Specific number or "at least X" |
| "Usually" | "In 90% of cases" or "By default" |
| "Should" (ambiguous) | "Must" or "May" |

### Step 4: Consistent Check

Verify uniform terminology and formatting.

**Terminology Consistency:**
- [ ] Same terms used for same concepts
- [ ] Consistent capitalization
- [ ] Consistent punctuation in lists
- [ ] Consistent heading levels

**Format Consistency:**
- [ ] Code blocks use consistent syntax highlighting
- [ ] Tables have consistent structure
- [ ] Dates in consistent format (ISO 8601 preferred)
- [ ] Version numbers in consistent format

**Create Terminology Table:**
```markdown
| Term | Meaning | DO NOT USE |
|------|---------|------------|
| User | End user | Customer, Client |
| Admin | Administrator | Super user |
| API Key | Authentication credential | Token, Secret |
```

### Step 5: Current Check

Verify document reflects current state.

**Verification Actions:**
- [ ] Last updated date is recent
- [ ] Version numbers match current releases
- [ ] Deprecated features are marked
- [ ] Future features are marked as "planned"
- [ ] No references to removed functionality

**Freshness Indicators:**
- Check `Last Updated` date
- Compare with recent commits to related code
- Verify against changelog

### Step 6: Connected Check

Verify proper cross-references.

**Link Verification:**
- [ ] All related documents linked
- [ ] Links use relative paths where possible
- [ ] No orphan documents (unlinked)
- [ ] Bidirectional links where appropriate

**Cross-Reference Checklist:**
- [ ] Links to related modules
- [ ] Links to relevant ADRs
- [ ] Links to API contracts
- [ ] Links to external resources
- [ ] See Also section complete

### Step 7: Document Results

Create quality report:

```markdown
# Quality Check Report: <Document Name>

**Reviewer:** <Name>
**Date:** <Date>
**Document Version:** <Version>

## Summary

| Criterion | Status | Issues |
|-----------|--------|--------|
| Complete | PASS/FAIL | <count> issues |
| Correct | PASS/FAIL | <count> issues |
| Clear | PASS/FAIL | <count> issues |
| Consistent | PASS/FAIL | <count> issues |
| Current | PASS/FAIL | <count> issues |
| Connected | PASS/FAIL | <count> issues |

## Issues Found

### Critical (Must Fix)
1. <Issue description>

### Minor (Should Fix)
1. <Issue description>

## Recommendation

[ ] APPROVED - Ready for publication
[ ] REVISE - Address critical issues
[ ] REJECT - Major rewrite needed
```

## Output

| Artifact | Content |
|----------|---------|
| Quality report | Review results and recommendations |
| Updated document | If corrections made inline |

## Verification Checklist

- [ ] All 6 C's evaluated
- [ ] Issues documented
- [ ] Severity assigned
- [ ] Recommendation made
- [ ] Report created

## Quality Thresholds

| Rating | Criteria |
|--------|----------|
| APPROVED | All 6 C's pass, no critical issues |
| REVISE | 1-2 C's fail or 1-3 critical issues |
| REJECT | 3+ C's fail or 4+ critical issues |

## Error Handling

| Error | Solution |
|-------|----------|
| Cannot verify correctness | Request access to source code |
| Multiple terminology conflicts | Create project glossary |
| Broken external links | Replace with archived version or remove |
