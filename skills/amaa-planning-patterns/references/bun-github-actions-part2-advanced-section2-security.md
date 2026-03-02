# Bun GitHub Actions: Security Scanning

**Parent document**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

---

## Table of Contents
- 2.1 [npm audit](#npm-audit)
- 2.2 [Dependency Review](#dependency-review)
- 2.3 [CodeQL Analysis](#codeql-analysis)
- 2.4 [Snyk Scanning](#snyk-scanning)
- 2.5 [License Compliance](#license-compliance)

---

## npm audit

Run security audits on dependencies:

```yaml
- name: Security audit
  run: npm audit --audit-level=moderate
  continue-on-error: false

- name: Check for vulnerabilities
  run: |
    npm audit --json > audit.json
    VULNERABILITIES=$(node -p "require('./audit.json').metadata.vulnerabilities.total")
    if [ "$VULNERABILITIES" -gt 0 ]; then
      echo "Found $VULNERABILITIES vulnerabilities"
      npm audit
      exit 1
    fi
```

---

## Dependency Review

Review dependencies in pull requests:

```yaml
name: Dependency Review
on: [pull_request]

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
          deny-licenses: GPL-3.0, AGPL-3.0
```

---

## CodeQL Analysis

Perform static code analysis with CodeQL:

```yaml
name: CodeQL
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - uses: github/codeql-action/init@v3
        with:
          languages: javascript

      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun run build.js

      - uses: github/codeql-action/analyze@v3
```

---

## Snyk Scanning

Scan for vulnerabilities with Snyk:

```yaml
- name: Run Snyk to check for vulnerabilities
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

---

## License Compliance

Check license compliance:

```yaml
- name: Check licenses
  run: |
    bunx license-checker --production --onlyAllow="MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"
```
