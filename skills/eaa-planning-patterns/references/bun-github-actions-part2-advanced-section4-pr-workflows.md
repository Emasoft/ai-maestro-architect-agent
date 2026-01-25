# Bun GitHub Actions: Pull Request Workflows

**Parent document**: [bun-github-actions-part2-advanced.md](./bun-github-actions-part2-advanced.md)

---

## Table of Contents
- 4.1 [PR Checks and Validation](#pr-checks-and-validation)
- 4.2 [Auto-Labeling PRs](#auto-labeling-prs)
- 4.3 [PR Size Validation](#pr-size-validation)
- 4.4 [Auto-Merge Dependabot PRs](#auto-merge-dependabot-prs)
- 4.5 [PR Comment with Test Results](#pr-comment-with-test-results)

---

## PR Checks and Validation

Comprehensive PR validation workflow:

```yaml
name: PR Checks
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2

      - name: Check formatting
        run: bun run format:check

      - name: Lint
        run: bun run lint

      - name: Type check
        run: bun run typecheck

      - name: Run tests
        run: bun test

      - name: Build
        run: bun run build.js

      - name: Check bundle size
        run: |
          bun run build.js
          SIZE=$(du -sh dist/ | cut -f1)
          echo "Bundle size: $SIZE"
```

---

## Auto-Labeling PRs

Automatically label PRs based on changed files:

```yaml
- name: Label PR
  uses: actions/labeler@v5
  with:
    repo-token: ${{ secrets.GITHUB_TOKEN }}
    configuration-path: .github/labeler.yml

# .github/labeler.yml
'dependencies':
  - package.json
  - package-lock.json
  - bun.lockb

'documentation':
  - '**/*.md'

'tests':
  - 'tests/**'
  - '**/*.test.ts'
```

---

## PR Size Validation

Enforce PR size limits:

```yaml
- name: Check PR size
  run: |
    FILES_CHANGED=$(git diff --name-only origin/main...HEAD | wc -l)
    LINES_CHANGED=$(git diff --stat origin/main...HEAD | tail -1 | awk '{print $4+$6}')
    if [ "$FILES_CHANGED" -gt 50 ] || [ "$LINES_CHANGED" -gt 1000 ]; then
      echo "PR too large: $FILES_CHANGED files, $LINES_CHANGED lines"
      echo "Consider splitting into smaller PRs"
      exit 1
    fi
```

---

## Auto-Merge Dependabot PRs

Automatically merge Dependabot PRs after tests pass:

```yaml
name: Dependabot Auto-Merge
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bun test

      - name: Enable auto-merge
        if: success()
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{github.event.pull_request.html_url}}
          GITHUB_TOKEN: ${{secrets.GITHUB_TOKEN}}
```

---

## PR Comment with Test Results

Post test results as PR comment:

```yaml
- name: Run tests
  id: test
  run: |
    bun test --reporter=json > test-results.json || true
    PASSED=$(jq '.numPassedTests' test-results.json)
    FAILED=$(jq '.numFailedTests' test-results.json)
    echo "passed=$PASSED" >> $GITHUB_OUTPUT
    echo "failed=$FAILED" >> $GITHUB_OUTPUT

- name: Comment PR
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## Test Results\n✅ Passed: ${{ steps.test.outputs.passed }}\n❌ Failed: ${{ steps.test.outputs.failed }}`
      })
```
