# Hypothesis Verification Skill

Verify claims through controlled Docker experimentation using the TBV (To Be Verified) principle. Never trust documentation or claims without experimental confirmation.

## When to Use

- Validating claims from documentation, researchers, or developers
- Reproducing bugs in isolated environments
- Comparing multiple implementation approaches
- Testing architectural decisions before committing
- Fact-checking performance or behavior claims

## Key Concepts

| Concept | Description |
|---------|-------------|
| **TBV Principle** | Everything is "To Be Verified" until personally tested |
| **Multiplicity Rule** | Always test 3+ approaches before selecting |
| **Ephemeral Code** | Experimental code is deleted after findings documented |
| **Docker Isolation** | ALL experiments run in containers |
| **Documentation** | 50% of output is the experiment report |

## Status Classifications

| Status | Meaning | Safe to Rely On? |
|--------|---------|------------------|
| **VERIFIED** | Experimentally confirmed | YES |
| **UNVERIFIED** | Tested but failed to match claim | NO (dangerous) |
| **PARTIALLY VERIFIED** | True under specific conditions | YES (with conditions) |
| **TBV** | Not yet tested | NO (unknown risk) |

## Reference Documents

- `references/docker-experimentation.md` - Container setup templates
- `references/researcher-vs-experimenter.md` - Role distinction and workflow
- `references/experiment-scenarios.md` - When to invoke experiments
- `references/multiplicity-rule.md` - Evidence-based selection process
- `references/output-templates.md` - Report and archive formats

## Quick Start

1. Read the claim to verify
2. Set up Docker container from template
3. Implement 3+ approaches (Multiplicity Rule)
4. Run experiments and collect evidence
5. Document findings in experiment report
6. Archive or delete experimental code
7. Report verification status

See [SKILL.md](SKILL.md) for complete instructions.
