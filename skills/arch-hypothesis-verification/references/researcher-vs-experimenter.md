# Researcher vs Experimenter

These are OPPOSITE roles with fundamentally different epistemologies.

---

## Table of Contents

- 1. The Researcher (What OTHERS say is true)
- 2. The Experimenter (What I can PROVE is true)
- 3. The TBV Principle (To Be Verified)
- 4. Workflow Integration: Researcher → Experimenter

---

## 1. The Researcher

**Philosophy**: "What do OTHERS say is true?"

| Characteristic | Description |
|----------------|-------------|
| **Source of truth** | External sources (docs, papers, forums, issues, threads) |
| **Method** | Collect, cross-reference, evaluate source credibility |
| **Output** | Curated findings with citations and source ratings |
| **Verification** | None - reports what sources claim, not personal validation |
| **Trust model** | Trusts credible sources (official docs, reputable authors, consensus) |

**What Researcher DOES:**
- Reads API documentation, papers, tutorials
- Searches Reddit threads, GitHub issues, Twitter discussions
- Cross-checks claims across multiple sources
- Evaluates source credibility (official vs community vs anonymous)
- Reports consensus and dissenting views
- Cites ALL sources - nothing reported without traceable reference

**What Researcher DOES NOT:**
- Write code to test claims
- Run benchmarks or experiments
- Personally verify performance numbers
- Generate original data
- Trust claims without external validation

**Researcher output example:**
```markdown
## Finding: Redis Streams Throughput

**Claim**: Redis Streams handles 100K messages/second
**Sources**:
- Official Redis docs (https://redis.io/docs/data-types/streams/): Claims 100K+ msg/s (HIGH credibility)
- StackOverflow answer (https://stackoverflow.com/q/example): User reports 85K msg/s (MEDIUM credibility)
- GitHub issue redis/redis#1234: Bug report showing 50K limit (HIGH credibility)

**Consensus**: 50K-100K msg/s depending on configuration
**Confidence**: MEDIUM (conflicting sources)
**Recommendation**: Needs experimental verification
```

---

## 2. The Experimenter

**Philosophy**: "What can I PROVE is true?"

| Characteristic | Description |
|----------------|-------------|
| **Source of truth** | Personal experimental results only |
| **Method** | Build testbeds, run experiments, measure outcomes |
| **Output** | Evidence-based conclusions with raw data |
| **Verification** | ALL claims verified through controlled experiments |
| **Trust model** | Trusts NOTHING - everything is TBV (To Be Verified) |

**What Experimenter DOES:**
- Questions ALL claims regardless of source
- Builds Docker containers to test hypotheses
- Runs controlled experiments with measurable outcomes
- Compares multiple approaches (minimum 3)
- Produces raw data, benchmarks, measurements
- Classifies claims as VERIFIED, UNVERIFIED, or TBV

**What Experimenter DOES NOT:**
- Accept claims based on source credibility
- Report findings without personal verification
- Trust official documentation without testing
- Assume consensus equals truth
- Skip verification because "everyone knows" something

**Experimenter output example:**
```markdown
## Verification: Redis Streams Throughput

**Claim tested**: "Redis Streams handles 100K messages/second"
**Source of claim**: Researcher report (citing official docs)

**Experimental setup**:
- Docker container: redis:7.2-alpine
- Test harness: custom Python with redis-py
- Message size: 1KB
- Duration: 60 seconds
- Iterations: 5 runs

**Results**:
| Run | Messages/sec | Latency P99 |
|-----|--------------|-------------|
| 1 | 67,234 | 12ms |
| 2 | 68,891 | 11ms |
| 3 | 66,102 | 13ms |
| 4 | 69,445 | 11ms |
| 5 | 67,890 | 12ms |

**Average**: 67,912 msg/s (32% below claimed 100K)
**Status**: PARTIALLY VERIFIED
**Conditions**: True only with sub-100 byte messages; 1KB messages hit ~68K

**Conclusion**: Researcher's claim was based on optimistic official numbers.
Actual measured throughput is 68K msg/s for realistic payloads.
```

---

## 3. The TBV Principle (To Be Verified)

**Everything not personally verified is marked TBV.**

```
┌─────────────────────────────────────────────────────────────────┐
│  VERIFIED (green)     - Tested personally, confirmed true       │
│  UNVERIFIED (red)     - Tested personally, failed to confirm    │
│  PARTIALLY (yellow)   - True under specific conditions only     │
│  TBV (gray)           - Not yet tested, treat as UNKNOWN        │
└─────────────────────────────────────────────────────────────────┘
```

**IRON RULE**: When the Orchestrator must make a decision, only VERIFIED facts are safe to rely on. TBV facts introduce risk. UNVERIFIED facts are dangerous assumptions.

---

## 4. Workflow Integration: Researcher → Experimenter

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Orchestrator needs information                               │
│    ↓                                                            │
│ 2. RESEARCHER collects from external sources                    │
│    - Produces report with citations                             │
│    - Flags claims needing verification                          │
│    ↓                                                            │
│ 3. EXPERIMENTER verifies critical claims                        │
│    - Tests in Docker containers                                 │
│    - Produces VERIFIED/UNVERIFIED status                        │
│    ↓                                                            │
│ 4. Orchestrator makes decision based on VERIFIED facts only     │
└─────────────────────────────────────────────────────────────────┘
```

**The Researcher saves time by filtering the universe of information.**
**The Experimenter ensures decisions are based on proven facts.**
