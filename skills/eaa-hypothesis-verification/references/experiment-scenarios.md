# Experiment Scenarios

When to invoke hypothesis verification.

---

## Table of Contents

- 1. Case 1: Post-Research Validation
- 2. Case 2: Issue Reproduction in Isolation
- 3. Case 3: Architectural Bug Investigation
- 4. Case 4: New API/Tool Evaluation
- 5. Case 5: Fact-Checking Claims (Quick Verification)

---

## 1. Case 1: Post-Research Validation

**Trigger**: Research agent completed a report with findings that need experimental validation before integration into architecture specs.

**Example**:
```
Research agent reports: "Redis Streams vs Kafka for event sourcing"
→ Experimenter builds testbeds for both
→ Measures throughput, latency, resource usage
→ Documents which performs better for our use case
→ Orchestrator decides based on evidence
```

---

## 2. Case 2: Issue Reproduction in Isolation

**Trigger**: Remote agents or developers report unforeseen limitations, issues, vulnerabilities, conflicts, incompatibilities, or algorithm limits that need isolated reproduction.

**Example**:
```
Remote agent reports: "WebSocket connections drop after 2 hours"
→ Experimenter creates minimal reproduction testbed
→ Isolates the issue from application complexity
→ Tests multiple hypotheses (timeout, memory leak, protocol issue)
→ Documents root cause with evidence
→ Orchestrator sends fix instructions to remote agents
```

---

## 3. Case 3: Architectural Bug Investigation

**Trigger**: Complex bugs that no implementer could fix, mysterious test failures, non-deterministic issues, architectural problems requiring pattern experimentation.

**Example**:
```
Multiple agents failed to fix: "Race condition in payment processing"
→ Experimenter reproduces in minimal testbed
→ Tests multiple architectural patterns:
  - Saga pattern
  - Two-phase commit
  - Event sourcing with compensation
→ Documents which pattern eliminates the race condition
→ Orchestrator updates architecture specs
```

---

## 4. Case 4: New API/Tool Evaluation

**Trigger**: New API released or new tool adoption requires evaluation against existing stack.

**Example**:
```
New tool: "Anthropic Claude Agent SDK released"
→ Experimenter builds testbeds for basic functions
→ Measures complexity, usage difficulty
→ Tests conflicts with existing frameworks
→ Compares with current solution (direct API calls)
→ Documents findings with benchmarks
→ Orchestrator decides whether to adopt
```

---

## 5. Case 5: Fact-Checking Claims (Quick Verification)

**Trigger**: Orchestrator needs to verify data, claims, hypotheses, or statements reported by implementers, researchers, or external sources before planning changes based on them.

**Example**:
```
Researcher reports: "Library X handles 10K req/s according to benchmarks"
→ Experimenter creates minimal load test
→ Runs actual benchmark in controlled environment
→ Verifies: actual throughput is 6.5K req/s (35% below claimed)
→ Reports: "Claim UNVERIFIED - actual measured: 6.5K req/s"
→ Orchestrator adjusts capacity planning accordingly
```

**Quick verification checklist**:
- Can this claim be tested in under 30 minutes?
- Is this claim critical to an architectural decision?
- Does the source provide reproducible test conditions?
- What would be the cost of acting on a false claim?

**Status classifications**:
| Status | Meaning |
|--------|---------|
| **VERIFIED** | Experimentally confirmed, safe to rely on |
| **UNVERIFIED** | Tested but failed to match claim |
| **PARTIALLY VERIFIED** | True under specific conditions only |
| **TBV** | To Be Verified - not yet tested, treat as unknown |
