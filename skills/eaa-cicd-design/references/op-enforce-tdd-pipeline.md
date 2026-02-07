---
procedure: support-skill
workflow-instruction: support
---

# Operation: Enforce TDD in Pipeline

## Purpose

Configure CI/CD pipelines to enforce Test-Driven Development practices including coverage thresholds, test-first checks, and quality gates.

## When to Use

- Setting up TDD enforcement in new projects
- Adding coverage requirements to existing pipelines
- Configuring quality gates for PRs

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Coverage threshold | Team standards | Yes |
| Test framework | Project config | Yes |
| Enforcement level | Team standards | Yes |

## Procedure

### Step 1: Define Coverage Thresholds

Recommended thresholds:
- Minimum: 70% (critical paths covered)
- Standard: 80% (good coverage)
- High: 90% (comprehensive coverage)

### Step 2: Configure Coverage Tool

**Python (pytest-cov):**
```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=xml --cov-fail-under=80 tests/
```

**JavaScript (vitest):**
```yaml
- name: Run tests with coverage
  run: |
    npm run test -- --coverage --coverage.thresholds.lines=80
```

**Rust (cargo-tarpaulin):**
```yaml
- name: Run tests with coverage
  run: |
    cargo tarpaulin --fail-under 80 --out Xml
```

**Go:**
```yaml
- name: Run tests with coverage
  run: |
    go test -coverprofile=coverage.out ./...
    go tool cover -func=coverage.out | grep total | awk '{if ($3+0 < 80) exit 1}'
```

### Step 3: Add Coverage to Workflow

```yaml
name: CI with TDD Enforcement

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run tests with coverage
        run: pytest --cov=src --cov-report=xml --cov-fail-under=80 tests/

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### Step 4: Configure Branch Protection

In repository settings:
1. Go to Settings > Branches
2. Add branch protection rule for `main`
3. Enable "Require status checks to pass"
4. Select the test job as required

```bash
# Using gh CLI
gh api -X PUT repos/{owner}/{repo}/branches/main/protection \
  -f required_status_checks='{"strict":true,"checks":[{"context":"test"}]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1}'
```

### Step 5: Add Coverage Comments to PRs

```yaml
- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    MINIMUM_GREEN: 80
    MINIMUM_ORANGE: 70
```

### Step 6: Block Test Skipping

Add pre-commit hook to detect `@pytest.mark.skip` or `.skip()`:

```yaml
# In workflow
- name: Check for skipped tests
  run: |
    if grep -r "skip\|xfail" tests/; then
      echo "::warning::Found skipped tests - review required"
    fi
```

## Output

| File | Content |
|------|---------|
| `.github/workflows/ci.yml` | CI workflow with TDD enforcement |
| `pyproject.toml` | Coverage configuration |
| Branch protection | Configured in GitHub |

## Verification Checklist

- [ ] Coverage threshold defined
- [ ] Coverage tool configured
- [ ] Coverage fails build if below threshold
- [ ] Coverage report uploaded
- [ ] Branch protection enabled
- [ ] Test job is required check
- [ ] PR comments show coverage

## Example

```yaml
name: TDD CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install
        run: pip install -e ".[test]"

      - name: Lint
        run: ruff check src/

      - name: Type check
        run: mypy src/

      - name: Test with coverage
        run: |
          pytest \
            --cov=src \
            --cov-report=term-missing \
            --cov-report=xml \
            --cov-fail-under=80 \
            tests/

      - name: Coverage report
        uses: codecov/codecov-action@v4
```

## Error Handling

| Error | Solution |
|-------|----------|
| Coverage below threshold | Add more tests or adjust threshold |
| Coverage tool not found | Install coverage dependencies |
| Branch protection bypass | Enable "Include administrators" |
