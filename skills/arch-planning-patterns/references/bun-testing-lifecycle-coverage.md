# Bun Testing Reference: Lifecycle, Coverage, and CI

## Table of Contents
1. [Lifecycle Hooks](#lifecycle-hooks)
   - 1.1 [beforeAll Hook](#beforeall-hook)
   - 1.2 [afterAll Hook](#afterall-hook)
   - 1.3 [beforeEach Hook](#beforeeach-hook)
   - 1.4 [afterEach Hook](#aftereach-hook)
   - 1.5 [Nested Describe Blocks](#nested-describe-blocks)
2. [Coverage Configuration](#coverage-configuration)
   - 2.1 [Basic Coverage](#basic-coverage)
   - 2.2 [Coverage with Reporter](#coverage-with-reporter)
   - 2.3 [Multiple Reporters](#multiple-reporters)
   - 2.4 [Viewing HTML Coverage Report](#viewing-html-coverage-report)
   - 2.5 [Coverage Thresholds](#coverage-thresholds)
3. [CI Integration](#ci-integration)
   - 3.1 [GitHub Actions Example](#github-actions-example)
   - 3.2 [GitLab CI Example](#gitlab-ci-example)
   - 3.3 [Jenkins Example](#jenkins-example)
4. [Package.json Scripts Setup](#packagejson-scripts-setup)
   - 4.1 [Basic Scripts](#basic-scripts)
   - 4.2 [Advanced Scripts with Pre/Post Hooks](#advanced-scripts-with-prepost-hooks)
   - 4.3 [CI-Specific Scripts](#ci-specific-scripts)

**Related Files:**
- [bun-testing-basics.md](bun-testing-basics.md) - Introduction, syntax, CLI options
- [bun-testing-advanced-troubleshooting.md](bun-testing-advanced-troubleshooting.md) - Advanced features and troubleshooting

---

## Lifecycle Hooks

Lifecycle hooks allow you to run setup and teardown code before and after tests.

### beforeAll Hook

```javascript
import { test, expect, describe, beforeAll } from "bun:test";

describe("Database Tests", () => {
  beforeAll(async () => {
    await database.connect();
  });

  test("can query users", async () => {
    const users = await database.query("SELECT * FROM users");
    expect(users).toBeDefined();
  });
});
```

**What it does:**
- Runs once before all tests in the describe block
- Useful for expensive setup operations (database connections, server startup)

**When to Use:**
- Initializing shared resources
- Setting up test databases
- Starting local test servers (real services in test mode)

### afterAll Hook

```javascript
import { test, expect, describe, beforeAll, afterAll } from "bun:test";

describe("Database Tests", () => {
  beforeAll(async () => {
    await database.connect();
  });

  afterAll(async () => {
    await database.disconnect();
  });

  test("can query users", async () => {
    const users = await database.query("SELECT * FROM users");
    expect(users).toBeDefined();
  });
});
```

**What it does:**
- Runs once after all tests in the describe block complete
- Ensures cleanup happens even if tests fail

**When to Use:**
- Closing database connections
- Stopping local test servers
- Cleaning up temporary files

### beforeEach Hook

```javascript
import { test, expect, describe, beforeEach } from "bun:test";

describe("Counter Tests", () => {
  let counter;

  beforeEach(() => {
    counter = 0;
  });

  test("starts at zero", () => {
    expect(counter).toBe(0);
  });

  test("can increment", () => {
    counter++;
    expect(counter).toBe(1);
  });
});
```

**What it does:**
- Runs before each individual test
- Ensures each test has fresh state
- Prevents test pollution (one test affecting another)

**When to Use:**
- Resetting variables between tests
- Creating fresh object instances
- Clearing test state

### afterEach Hook

```javascript
import { test, expect, describe, beforeEach, afterEach } from "bun:test";

describe("File Tests", () => {
  let tempFile;

  beforeEach(() => {
    tempFile = createTempFile();
  });

  afterEach(() => {
    deleteTempFile(tempFile);
  });

  test("can write to file", () => {
    writeFile(tempFile, "test data");
    expect(readFile(tempFile)).toBe("test data");
  });
});
```

**What it does:**
- Runs after each individual test
- Cleans up resources created during the test

**When to Use:**
- Deleting temporary files
- Restoring test state
- Clearing test data

### Nested Describe Blocks

```javascript
import { test, expect, describe, beforeAll, beforeEach } from "bun:test";

describe("Outer Suite", () => {
  beforeAll(() => {
    console.log("Runs once for outer suite");
  });

  beforeEach(() => {
    console.log("Runs before each test in outer suite");
  });

  test("outer test", () => {
    expect(true).toBe(true);
  });

  describe("Inner Suite", () => {
    beforeEach(() => {
      console.log("Runs before each test in inner suite");
    });

    test("inner test", () => {
      expect(true).toBe(true);
    });
  });
});
```

**Execution Order for "inner test":**
1. Outer `beforeAll` (once)
2. Outer `beforeEach`
3. Inner `beforeEach`
4. Test execution
5. Inner `afterEach` (if defined)
6. Outer `afterEach` (if defined)

---

## Coverage Configuration

### Basic Coverage

```bash
bun test --coverage
```

**Default Output:**
```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   85.71 |      100 |      75 |   85.71 |
 utils.ts           |   85.71 |      100 |      75 |   85.71 |
--------------------|---------|----------|---------|---------|
```

### Coverage with Reporter

```bash
bun test --coverage --coverage-reporter=lcov
```

**Available Coverage Reporters:**
- `text` - Console output (default)
- `lcov` - Generates `coverage/lcov.info` file (for CI tools like Codecov, Coveralls)
- `html` - Generates interactive HTML report in `coverage/` directory
- `json` - Generates JSON report

**When to Use:**
- `lcov` - For CI/CD pipelines and coverage tracking services
- `html` - For local development and detailed analysis
- `json` - For programmatic processing

### Multiple Reporters

```bash
bun test --coverage --coverage-reporter=lcov --coverage-reporter=html
```

**What it does:**
- Generates both lcov file and HTML report
- Useful for both CI and local development

### Viewing HTML Coverage Report

```bash
bun test --coverage --coverage-reporter=html
open coverage/index.html
```

**What you see:**
- Interactive web page showing file-by-file coverage
- Line-by-line highlighting (green = covered, red = uncovered)
- Drill-down navigation through project structure

### Coverage Thresholds

Currently, Bun does not have built-in coverage threshold enforcement. You can use external tools or scripts to check coverage thresholds.

**Example Script (check-coverage.js):**
```javascript
import { readFileSync } from "fs";

const coverage = JSON.parse(readFileSync("coverage/coverage-summary.json", "utf-8"));
const threshold = 80;

const total = coverage.total;
if (total.lines.pct < threshold) {
  console.error(`Line coverage ${total.lines.pct}% is below threshold ${threshold}%`);
  process.exit(1);
}
```

**Usage:**
```bash
bun test --coverage --coverage-reporter=json-summary
bun run check-coverage.js
```

---

## CI Integration

### GitHub Actions Example

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install

      - name: Run tests
        run: bun test

      - name: Run tests with coverage
        run: bun test --coverage --coverage-reporter=lcov

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

**Explanation:**
- `uses: oven-sh/setup-bun@v1` - Installs Bun runtime in CI environment
- `bun install` - Installs project dependencies
- `bun test` - Runs tests
- `--coverage-reporter=lcov` - Generates coverage file for Codecov
- `codecov/codecov-action@v3` - Uploads coverage to Codecov service

### GitLab CI Example

```yaml
test:
  image: oven/bun:latest
  script:
    - bun install
    - bun test --coverage --reporter=junit --coverage-reporter=lcov
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

**Explanation:**
- `image: oven/bun:latest` - Uses official Bun Docker image
- `--reporter=junit` - Generates JUnit XML for test results
- `artifacts.reports.junit` - Publishes test results to GitLab
- `artifacts.reports.coverage_report` - Publishes coverage to GitLab

### Jenkins Example

```groovy
pipeline {
  agent any

  stages {
    stage('Install') {
      steps {
        sh 'curl -fsSL https://bun.sh/install | bash'
        sh 'bun install'
      }
    }

    stage('Test') {
      steps {
        sh 'bun test --reporter=junit --coverage --coverage-reporter=lcov'
      }
    }

    stage('Publish Results') {
      steps {
        junit 'junit.xml'
        publishHTML([
          reportDir: 'coverage',
          reportFiles: 'index.html',
          reportName: 'Coverage Report'
        ])
      }
    }
  }
}
```

---

## Package.json Scripts Setup

### Basic Scripts

```json
{
  "name": "my-project",
  "scripts": {
    "test": "bun test",
    "test:watch": "bun test --watch",
    "test:coverage": "bun test --coverage",
    "test:coverage:html": "bun test --coverage --coverage-reporter=html"
  }
}
```

**Explanation of Each Script:**
- `"test": "bun test"` - Standard test command, used by CI/CD
- `"test:watch": "bun test --watch"` - Development mode with auto-reload
- `"test:coverage": "bun test --coverage"` - Run with coverage report
- `"test:coverage:html": "bun test --coverage --coverage-reporter=html"` - Generate HTML coverage report

**Running Scripts:**
```bash
bun run test
bun run test:watch
bun run test:coverage
bun run test:coverage:html
```

### Advanced Scripts with Pre/Post Hooks

```json
{
  "scripts": {
    "pretest": "bun run lint",
    "test": "bun test",
    "posttest": "bun run check-coverage",
    "lint": "eslint src",
    "check-coverage": "node scripts/check-coverage.js"
  }
}
```

**Execution Order:**
When you run `bun run test`, the following happens:
1. `pretest` script runs first (linting)
2. `test` script runs
3. `posttest` script runs (coverage check)

### CI-Specific Scripts

```json
{
  "scripts": {
    "test": "bun test",
    "test:ci": "bun test --reporter=junit --coverage --coverage-reporter=lcov",
    "test:ci:verbose": "bun test --reporter=junit --coverage --coverage-reporter=lcov --coverage-reporter=text"
  }
}
```

**When to Use:**
- `test:ci` - In CI/CD pipelines for machine-readable output
- `test:ci:verbose` - For debugging CI failures with text output

---

**Next:** See [bun-testing-advanced-troubleshooting.md](bun-testing-advanced-troubleshooting.md) for advanced features and troubleshooting.
