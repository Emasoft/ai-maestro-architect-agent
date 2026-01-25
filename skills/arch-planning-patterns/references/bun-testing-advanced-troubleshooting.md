# Bun Testing Reference: Advanced Features and Troubleshooting

## Table of Contents
1. [Advanced Features](#advanced-features)
   - 1.1 [Per-Test Timeout](#per-test-timeout)
   - 1.2 [Test.only - Run Single Test](#testonly---run-single-test)
   - 1.3 [Test.skip - Skip Test](#testskip---skip-test)
   - 1.4 [Test.todo - Mark Unimplemented Test](#testtodo---mark-unimplemented-test)
   - 1.5 [Testing External Services](#testing-external-services)
2. [Troubleshooting](#troubleshooting)
   - 2.1 [Tests Not Found](#problem-tests-not-found)
   - 2.2 [Test Timeout](#problem-test-timeout)
   - 2.3 [Coverage Not Generated](#problem-coverage-not-generated)
   - 2.4 [Coverage Report Directory Not Created](#problem-coverage-report-directory-not-created)
   - 2.5 [Tests Pass Locally, Fail in CI](#problem-tests-pass-locally-fail-in-ci)
   - 2.6 [Hooks Not Running](#problem-hooks-not-running)
   - 2.7 [Memory Issues with Large Test Suites](#problem-memory-issues-with-large-test-suites)
   - 2.8 [Slow External Services in Tests](#problem-slow-external-services-in-tests)
3. [Summary](#summary)

**Related Files:**
- [bun-testing-basics.md](bun-testing-basics.md) - Introduction, syntax, CLI options
- [bun-testing-lifecycle-coverage.md](bun-testing-lifecycle-coverage.md) - Lifecycle hooks, coverage config, CI integration

---

## Advanced Features

### Per-Test Timeout

```javascript
import { test, expect } from "bun:test";

test("slow test", async () => {
  await slowOperation();
  expect(true).toBe(true);
}, { timeout: 30000 }); // 30 seconds for this specific test
```

**Explanation:**
- Second argument to `test()` is options object
- `timeout` property overrides global timeout for this test only
- Value is in milliseconds

**When to Use:**
- When specific tests need more time (API calls, large file processing)
- When most tests are fast but a few are slow

### Test.only - Run Single Test

```javascript
import { test, expect } from "bun:test";

test("this test will be skipped", () => {
  expect(1).toBe(1);
});

test.only("only this test will run", () => {
  expect(2).toBe(2);
});

test("this test will also be skipped", () => {
  expect(3).toBe(3);
});
```

**What it does:**
- Only tests marked with `.only` will execute
- All other tests are skipped
- Useful for debugging specific test failures

**Warning:**
- Remove `.only` before committing code
- CI should fail if `.only` is present (prevents incomplete test runs)

### Test.skip - Skip Test

```javascript
import { test, expect } from "bun:test";

test("this test runs", () => {
  expect(1).toBe(1);
});

test.skip("this test is skipped", () => {
  expect(2).toBe(2);
});
```

**When to Use:**
- Temporarily disable failing tests while fixing
- Skip tests that depend on unavailable resources
- Mark known issues for later resolution

**Best Practice:**
- Add comment explaining why test is skipped
- Create issue/ticket to re-enable test

### Test.todo - Mark Unimplemented Test

```javascript
import { test } from "bun:test";

test.todo("implement user authentication");
```

**What it does:**
- Marks test as planned but not implemented
- Shows in test output as "TODO"
- Does not execute any code

**When to Use:**
- Planning test coverage
- Documenting required tests
- Test-driven development (write test names first)

### Testing External Services

```javascript
import { test, expect, describe } from "bun:test";

describe("API Client", () => {
  test("fetches real data from API", async () => {
    const result = await apiClient.getData();
    expect(result.data).toBeDefined();
    expect(typeof result.data).toBe('string');
  }, { timeout: 10000 }); // Allow time for real API call
});
```

**Recommended approach:**
- Use real external services in tests
- Set appropriate timeouts for network operations
- Test against real APIs to catch integration issues
- Use test environments or local services for controllable test data

**Why avoid mocking:**
- Bun's test runner does not have built-in mocking utilities like Jest's `jest.fn()`
- Mocked tests hide real integration problems
- Real tests provide confidence that your code works with actual services
- If tests are slow, optimize the service or use local test instances, do not mock

---

## Troubleshooting

### Problem: Tests Not Found

**Symptom:**
```bash
bun test
No tests found
```

**Possible Causes:**
1. Test files don't match naming convention
2. Tests are in ignored directories

**Solution:**
- Ensure test files end with `.test.ts`, `.test.js`, `.spec.ts`, or `.spec.js`
- Check that test files are not in `node_modules` or other ignored directories
- Verify test files contain `test()` or `describe()` functions

**Example Fix:**
```bash
# Wrong naming
mv tests.ts tests.test.ts

# Check file is discovered
bun test --dry-run
```

---

### Problem: Test Timeout

**Symptom:**
```
Test "my async test" timed out after 5000ms
```

**Possible Causes:**
1. Test involves slow operations (API calls, large computations)
2. Async operation never completes (missing await, unhandled promise)

**Solution 1: Increase Timeout**
```javascript
test("slow test", async () => {
  await slowOperation();
}, { timeout: 30000 });
```

**Solution 2: Increase Global Timeout**
```bash
bun test --timeout 30000
```

**Solution 3: Fix Async Issue**
```javascript
// Wrong - missing await
test("async test", async () => {
  fetchData(); // Promise not awaited
  expect(data).toBeDefined(); // data is undefined
});

// Correct
test("async test", async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

---

### Problem: Coverage Not Generated

**Symptom:**
```bash
bun test --coverage
# No coverage output shown
```

**Possible Causes:**
1. No test files executed
2. Source files not imported by tests

**Solution:**
- Verify tests are running: `bun test` (should show test results)
- Ensure tests import the source code you want to measure:
  ```javascript
  import { myFunction } from "../src/utils"; // This file will be in coverage

  test("uses myFunction", () => {
    expect(myFunction()).toBeDefined();
  });
  ```

---

### Problem: Coverage Report Directory Not Created

**Symptom:**
```bash
bun test --coverage --coverage-reporter=html
# coverage/ directory doesn't exist
```

**Solution:**
- Check write permissions in project directory
- Manually create directory: `mkdir -p coverage`
- Verify Bun version: `bun --version` (update if old)

---

### Problem: Tests Pass Locally, Fail in CI

**Possible Causes:**
1. Environment differences (OS, Node version)
2. Missing environment variables
3. Timing issues (timeouts too short for slower CI machines)
4. File path assumptions (case sensitivity on Linux vs macOS)

**Solution 1: Match CI Environment Locally**
```bash
# Use Docker to match CI environment
docker run -it oven/bun:latest bun test
```

**Solution 2: Add Debug Output**
```javascript
test("debug test", () => {
  console.log("Platform:", process.platform);
  console.log("Bun version:", Bun.version);
  console.log("ENV:", process.env);
});
```

**Solution 3: Increase CI Timeouts**
```yaml
# GitHub Actions
- name: Run tests
  run: bun test --timeout 30000
```

---

### Problem: Hooks Not Running

**Symptom:**
Setup/teardown code in `beforeAll`, `afterAll`, `beforeEach`, `afterEach` not executing

**Possible Causes:**
1. Hook is outside `describe` block but expected to run for all tests
2. Async hook not awaited

**Solution 1: Place Hooks Inside describe**
```javascript
// Wrong
beforeAll(() => {
  setup();
});

describe("Suite", () => {
  test("test", () => {});
});

// Correct
describe("Suite", () => {
  beforeAll(() => {
    setup();
  });

  test("test", () => {});
});
```

**Solution 2: Await Async Hooks**
```javascript
// Wrong
beforeAll(async () => {
  database.connect(); // Missing await
});

// Correct
beforeAll(async () => {
  await database.connect();
});
```

---

### Problem: Memory Issues with Large Test Suites

**Symptom:**
```
Out of memory error
Process killed
```

**Solution 1: Run Tests in Batches**
```bash
bun test src/module-a/**/*.test.ts
bun test src/module-b/**/*.test.ts
```

**Solution 2: Increase Memory Limit**
```bash
bun --max-old-space-size=4096 test
```

**Solution 3: Clean Up Resources**
```javascript
describe("Large Data Tests", () => {
  let largeData;

  beforeEach(() => {
    largeData = createLargeDataset();
  });

  afterEach(() => {
    largeData = null; // Allow garbage collection
  });
});
```

---

### Problem: Slow External Services in Tests

**Symptom:**
Tests that depend on external services (APIs, databases) run slowly.

**Recommended Solution: Use Real Services**
```javascript
// Use real external services with appropriate timeouts
import { test, expect } from "bun:test";
import { getUsers } from "./client";

test("getUsers fetches from real API", async () => {
  const users = await getUsers();
  expect(users.length).toBeGreaterThan(0);
  expect(users[0]).toHaveProperty('id');
}, { timeout: 15000 }); // Real API calls need longer timeout
```

**Why use real services:**
- Real tests catch actual integration issues (API changes, network problems, auth issues)
- Mocked tests only verify that your mock works, not that the real service works
- Real tests provide confidence that your code works in production

**For development environments:**
- Use local instances of databases/services that can be started/stopped for tests
- Use test databases with known data for predictable test results
- For third-party APIs: use real test endpoints or skip tests that require unavailable services

---

## Summary

**Key Takeaways:**
1. Import test utilities from `"bun:test"`
2. Use `describe()` for grouping, `test()` for individual tests
3. Run with `bun test`, add `--coverage` for coverage, `--watch` for development
4. Use lifecycle hooks (`beforeAll`, `afterAll`, `beforeEach`, `afterEach`) for setup/teardown
5. Configure scripts in `package.json` for convenience
6. Use `--reporter=junit` and `--coverage-reporter=lcov` for CI integration
7. Set per-test timeouts with `{ timeout: ms }` option
8. Generate HTML coverage reports for detailed analysis

**Common Workflow:**
1. Write test in `*.test.ts` file
2. Run `bun test --watch` during development
3. Run `bun test --coverage` before committing
4. Configure CI to run `bun test --reporter=junit --coverage --coverage-reporter=lcov`
5. Review coverage reports and add missing tests

**Next Steps:**
- Read official Bun test documentation: https://bun.sh/docs/cli/test
- Set up CI integration for your project
- Aim for >80% code coverage
- Use lifecycle hooks to keep tests isolated and maintainable
