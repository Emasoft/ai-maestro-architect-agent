# Scripts Reference

## Table of Contents

- 1. Universal Analysis Scripts
  - 1.1 dependency_resolver.py - Resolving task dependencies and detecting cycles
  - 1.2 project_detector.py - Detecting project types and toolchains
  - 1.3 health_auditor.py - Running project health checks
  - 1.4 evidence_store.py - Storing and retrieving verification evidence
  - 1.5 analyzer_scaffold.py - Generating custom analyzer scaffolds
- 2. Core Planning Scripts
  - 2.1 planner.py - Step-based planning workflow with decision classification
  - 2.2 executor.py - 7-phase execution orchestration with JIT prompt injection
- 3. Template Generation Scripts
  - 3.1 generate_planning_checklist.py - Creating customized planning checklists
  - 3.2 generate_risk_register.py - Creating risk register templates
  - 3.3 generate_roadmap_template.py - Creating milestone-based roadmap templates
- 4. Analysis Scripts
  - 4.1 consistency_verifier.py - Verifying plan internal consistency
  - 4.2 quality_pattern_detector.py - Detecting code quality patterns
  - 4.3 scoring_framework.py - Multi-criteria scoring system
  - 4.4 comparison_analyzer.py - Comparing multiple options
  - 4.5 ab_test_calculator.py - A/B test statistical analysis
  - 4.6 checklist_validator.py - Validating checklist completion
- 5. Task Tracker Scripts
  - 5.1 generate_task_tracker.py - Generating task trackers from plans
  - 5.2 generate_status_report.py - Generating markdown status reports

---

## 1. Universal Analysis Scripts

### 1.1 dependency_resolver.py

**Purpose**: Universal dependency resolution using topological sort (Kahn's algorithm)

**Usage**:
```bash
# Resolve task dependencies and output execution order
python scripts/dependency_resolver.py --input tasks.json --output order.json

# Detect circular dependencies
python scripts/dependency_resolver.py --input tasks.json --detect-cycles

# Extract subgraph for a specific task
python scripts/dependency_resolver.py --input tasks.json --subgraph "deploy"
```

**Features**:
- Supports JSON/YAML input formats
- Cycle detection with cycle path reporting
- Subgraph extraction for focused analysis
- Task filtering by status or custom criteria
- Critical path identification

### 1.2 project_detector.py

**Purpose**: Automatic project type detection and capability inference

**Usage**:
```bash
# Detect project types in current directory
python scripts/project_detector.py --path .

# Output as JSON for automation
python scripts/project_detector.py --path /path/to/project --format json

# Include inferred capabilities
python scripts/project_detector.py --path . --capabilities
```

**Detects**:
- Python (pip, poetry, uv, conda)
- Node.js (npm, yarn, pnpm)
- Rust (cargo)
- Go (go.mod)
- Swift (Package.swift, Xcode)
- CMake
- Java (Maven, Gradle)
- .NET (MSBuild)

**Infers**: Package manager, test framework, linter, formatter, CI system

### 1.3 health_auditor.py

**Purpose**: Modular project health auditing with pluggable checks

**Usage**:
```bash
# Run all health checks
python scripts/health_auditor.py --path /path/to/project

# Run specific checks only
python scripts/health_auditor.py --path . --checks git,deps,tests

# Output as JSON for CI integration
python scripts/health_auditor.py --path . --format json --output health-report.json
```

**Check Categories**:
- `git`: Repository status, uncommitted changes, branch state
- `deps`: Dependency health, outdated packages, security issues
- `tests`: Test presence, coverage, test health
- `docs`: Documentation completeness, README, API docs
- `ci`: CI/CD configuration, workflow health

**Severity Levels**: CRITICAL, WARNING, INFO

### 1.4 evidence_store.py

**Purpose**: Store and retrieve verification evidence for plan validation

**Usage**:
```bash
python scripts/evidence_store.py --store evidence.json --key "test-results" --value "all-pass"
python scripts/evidence_store.py --retrieve evidence.json --key "test-results"
```

### 1.5 analyzer_scaffold.py

**Purpose**: Generate analyzer tool scaffolds by category

**Usage**:
```bash
# Generate a dependency analyzer scaffold
python scripts/analyzer_scaffold.py --category dependency --name my_dep_analyzer --output analyzers/

# Generate a security analyzer with all hooks
python scripts/analyzer_scaffold.py --category security --name sec_scanner --output analyzers/

# Available categories: dependency, bundle, coverage, performance, security, custom
```

**Categories**:
- `dependency`: Dependency analysis tools
- `bundle`: Bundle size analyzers
- `coverage`: Code coverage tools
- `performance`: Performance profilers
- `security`: Security scanners
- `custom`: Generic analyzer template

**Output**: Complete Python module with CLI, core logic, and tests

---

## 2. Core Planning Scripts

### 2.1 planner.py

**Purpose**: Step-based planning workflow with decision classification

**Usage**:
```bash
python scripts/planner.py --input requirements.md --output plan.md
```

**Features**:
- Interactive step-based planning
- Decision classification (user-specified, doc-derived, default-derived, assumption)
- Produces structured plan output
- Validates against default conventions

### 2.2 executor.py

**Purpose**: 7-phase execution orchestration with JIT prompt injection

**Usage**:
```bash
python scripts/executor.py --plan plan.md --output execution_log.md
```

**Phases**:
1. Planning - Initial plan validation
2. Reconciliation - Requirement consistency checks
3. Execution - Delegate implementation tasks
4. Quality Review - Review code changes
5. Resolution - Address review findings
6. Documentation - Update docs
7. Retrospective - Capture lessons learned

---

## 3. Template Generation Scripts

### 3.1 generate_planning_checklist.py

**Purpose**: Create a customized checklist for your project based on number of phases

**Usage**:
```bash
python scripts/generate_planning_checklist.py --project "MyProject" --phases 4
```

### 3.2 generate_risk_register.py

**Purpose**: Create empty risk register in various formats ready to fill in

**Usage**:
```bash
python scripts/generate_risk_register.py --template excel --output my-risks.xlsx
```

### 3.3 generate_roadmap_template.py

**Purpose**: Create milestone-based roadmap template (no time estimations)

**Usage**:
```bash
python scripts/generate_roadmap_template.py --phases 5 --output roadmap.md
```

---

## 4. Analysis Scripts

### 4.1 consistency_verifier.py

**Purpose**: Verify plan internal consistency

Checks that all referenced tasks exist, dependencies are valid, and no orphaned sections.

### 4.2 quality_pattern_detector.py

**Purpose**: Detect code quality patterns in the codebase

Identifies common patterns and anti-patterns for code review prioritization.

### 4.3 scoring_framework.py

**Purpose**: Multi-criteria scoring system for decision making

Allows weighted scoring of options against defined criteria.

### 4.4 comparison_analyzer.py

**Purpose**: Compare multiple options side by side

Generates comparison matrices for technology or approach decisions.

### 4.5 ab_test_calculator.py

**Purpose**: A/B test statistical analysis

Calculates statistical significance and sample size requirements.

### 4.6 checklist_validator.py

**Purpose**: Validate checklist completion

Ensures all required checklist items are marked complete before proceeding.

---

## 5. Task Tracker Scripts

### 5.1 generate_task_tracker.py

**Purpose**: Generate task tracker from plan document

**Usage**:
```bash
python scripts/generate_task_tracker.py --from-plan plans/GH-42-feature.md --output tracker.json
```

**Features**:
- Validates that dependencies form a DAG (no circular dependencies)
- Calculates the critical path
- Outputs in CSV or JSON format

### 5.2 generate_status_report.py

**Purpose**: Generate markdown status reports from tracker

**Usage**:
```bash
python scripts/generate_status_report.py --tracker tracker.json --output status.md
```

---

## Resources

Additional resources in `resources/` folder:
- `plan-format.md` - Plan template used by planner.py for structured output
- `diff-format.md` - Plan diff specification
- `references/plan-verification-guide.md` - Verification integration
- `references/plan-file-linking.md` - GitHub issue linking requirements and traceability

See `scripts/README.md` for detailed script documentation.
