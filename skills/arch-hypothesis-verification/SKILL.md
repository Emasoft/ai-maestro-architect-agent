---
name: ao-hypothesis-verification
description: Verify claims through controlled Docker experimentation using the TBV (To Be Verified) principle.
agent: test-engineer
context: fork
---

# Hypothesis Verification Skill

Patterns for **personally verifying claims** through controlled Docker experimentation. Use this skill when you need to test whether a claim (from docs, researchers, or developers) is actually true.

**TBV Principle**: Everything is "To Be Verified" until you personally test it. Claims from any source require experimental confirmation before relying on them for decisions.

---

## Table of Contents

### Docker Experimentation
For Docker container setup and experiment infrastructure, see [docker-experimentation.md](references/docker-experimentation.md):
- 1. Why Docker is Required
- 2. Container Structure Template
- 3. docker-compose.yml Template
- 4. Container Cleanup Procedure

### Researcher vs Experimenter
For understanding the critical distinction between roles, see [researcher-vs-experimenter.md](references/researcher-vs-experimenter.md):
- 1. The Researcher (What OTHERS say is true)
- 2. The Experimenter (What I can PROVE is true)
- 3. The TBV Principle (To Be Verified)
- 4. Workflow Integration: Researcher → Experimenter

### Experiment Scenarios
For when to invoke the experimenter, see [experiment-scenarios.md](references/experiment-scenarios.md):
- 1. Case 1: Post-Research Validation
- 2. Case 2: Issue Reproduction in Isolation
- 3. Case 3: Architectural Bug Investigation
- 4. Case 4: New API/Tool Evaluation
- 5. Case 5: Fact-Checking Claims (Quick Verification)

### Multiplicity Rule
For the evidence-based selection process, see [multiplicity-rule.md](references/multiplicity-rule.md):
- 1. The Multiplicity Process
- 2. Example: Implementing a Paper Algorithm
- 3. Iterative Selection Workflow

### Output Templates
For experiment documentation and prototype archiving, see [output-templates.md](references/output-templates.md):
- 1. Experiment Directory Structure
- 2. Experimentation Report Template
- 3. Prototype Archive Policy
- 4. Archive README Template

---

## Quick Reference

### Status Classifications

| Status | Meaning | Safe to Rely On? |
|--------|---------|------------------|
| **VERIFIED** | Experimentally confirmed | YES |
| **UNVERIFIED** | Tested but failed to match claim | NO (dangerous) |
| **PARTIALLY VERIFIED** | True under specific conditions | YES (with conditions) |
| **TBV** | Not yet tested | NO (unknown risk) |

### Implementation vs Experimental Code

| Implementation Code | Experimental Code |
|--------------------|-------------------|
| Permanent (committed) | Ephemeral (deleted after) |
| Production-ready | Throwaway testbed |
| Follows specifications | Generates specifications |
| One chosen solution | Multiple solutions compared |
| Part of delivery | Part of decision-making |

### Workflow Integration Points

| Workflow | Trigger | Experimenter Action |
|----------|---------|---------------------|
| BUILD | Architecture decision needs validation | Validates with testbeds |
| DEBUG | Root cause unclear or fix uncertain | Reproduces in isolation, tests fixes |
| REVIEW | Performance concerns or architectural questions | Benchmarks alternatives |

### IRON RULES Summary

1. **Multiplicity**: Always test 3+ approaches
2. **Ephemeral code**: Delete after findings documented
3. **Evidence-based**: Conclusions backed by measurements
4. **Docker isolation**: ALL experiments in containers
5. **Documentation**: 50% output is the report
6. **TBV by default**: Everything unverified until tested
