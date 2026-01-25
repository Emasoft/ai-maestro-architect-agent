# Bun Testing Reference: Basics

## Table of Contents
1. [What is Bun Test Runner](#what-is-bun-test-runner)
2. [Test Syntax and Structure](#test-syntax-and-structure)
   - 2.1 [Basic Test File Structure](#basic-test-file-structure)
   - 2.2 [Test Without describe Block](#test-without-describe-block)
   - 2.3 [Async Tests](#async-tests)
   - 2.4 [Common Matchers](#common-matchers)
3. [CLI Options Reference](#cli-options-reference)
   - 3.1 [Basic Execution](#basic-execution)
   - 3.2 [Coverage Mode](#coverage-mode)
   - 3.3 [Watch Mode](#watch-mode)
   - 3.4 [Custom Timeout](#custom-timeout)
   - 3.5 [Reporter Options](#reporter-options)
   - 3.6 [Specific File or Pattern](#specific-file-or-pattern)
   - 3.7 [Combined Options](#combined-options)

**Related Files:**
- [bun-testing-lifecycle-coverage.md](bun-testing-lifecycle-coverage.md) - Lifecycle hooks, coverage config, CI integration
- [bun-testing-advanced-troubleshooting.md](bun-testing-advanced-troubleshooting.md) - Advanced features and troubleshooting

---

## What is Bun Test Runner

**Bun** is a modern JavaScript runtime that includes a built-in test runner. The Bun test runner is designed to be fast, simple, and compatible with Jest-like syntax.

**Key Characteristics:**
- **Built-in**: No need to install separate testing libraries like Jest or Mocha
- **Fast**: Written in Zig, optimized for speed
- **Jest-compatible API**: Uses familiar `test()`, `expect()`, and `describe()` functions
- **TypeScript support**: Native TypeScript execution without transpilation
- **Coverage reporting**: Built-in code coverage with multiple reporter formats

**When to Use Bun Test Runner:**
- When your project uses Bun as the runtime
- When you want fast test execution
- When you prefer minimal configuration
- When you need TypeScript support without additional tooling

---

## Test Syntax and Structure

### Basic Test File Structure

```javascript
import { test, expect, describe } from "bun:test";

describe("Suite Name", () => {
  test("test description", () => {
    expect(2 + 2).toBe(4);
  });
});
```

**Explanation of Components:**
- `import { test, expect, describe } from "bun:test"` - Import testing utilities from Bun's built-in test module
- `describe("Suite Name", () => {...})` - Groups related tests together (optional but recommended for organization)
- `test("test description", () => {...})` - Defines a single test case
- `expect(value).toBe(expected)` - Assertion that compares actual value to expected value

### Test Without describe Block

```javascript
import { test, expect } from "bun:test";

test("addition works", () => {
  expect(2 + 2).toBe(4);
});
```

**When to Use:**
- For simple files with one or two tests
- When grouping is not necessary

### Async Tests

```javascript
import { test, expect } from "bun:test";

test("async operation", async () => {
  const result = await fetchData();
  expect(result).toBeDefined();
});
```

**Explanation:**
- Use `async` keyword before the test function
- Use `await` for asynchronous operations
- Test will wait for all promises to resolve before completing

### Common Matchers

```javascript
// Equality
expect(value).toBe(expected);           // Strict equality (===)
expect(value).toEqual(expected);        // Deep equality for objects/arrays

// Truthiness
expect(value).toBeTruthy();             // Any truthy value
expect(value).toBeFalsy();              // Any falsy value
expect(value).toBeDefined();            // Not undefined
expect(value).toBeUndefined();          // Is undefined
expect(value).toBeNull();               // Is null

// Numbers
expect(value).toBeGreaterThan(num);     // value > num
expect(value).toBeGreaterThanOrEqual(num); // value >= num
expect(value).toBeLessThan(num);        // value < num
expect(value).toBeLessThanOrEqual(num); // value <= num

// Strings
expect(string).toContain(substring);    // String includes substring
expect(string).toMatch(/regex/);        // String matches regex pattern

// Arrays
expect(array).toContain(item);          // Array includes item
expect(array).toHaveLength(num);        // Array has specific length

// Objects
expect(obj).toHaveProperty("key");      // Object has property
expect(obj).toHaveProperty("key", value); // Object has property with value

// Functions
expect(fn).toThrow();                   // Function throws error
expect(fn).toThrow("error message");    // Function throws specific error
```

---

## CLI Options Reference

### Basic Execution

```bash
bun test
```

**What it does:**
- Discovers all test files in the project
- Executes all tests
- Reports results to console

**Test File Discovery Pattern:**
- Files ending in `.test.ts`, `.test.tsx`, `.test.js`, `.test.jsx`
- Files in `__tests__` directories
- Files matching `*.spec.ts`, `*.spec.tsx`, `*.spec.js`, `*.spec.jsx`

### Coverage Mode

```bash
bun test --coverage
```

**What it does:**
- Runs all tests
- Collects code coverage data
- Displays coverage summary in console

**Coverage Metrics Explained:**
- **Statements**: Percentage of executed code statements
- **Branches**: Percentage of executed conditional branches (if/else)
- **Functions**: Percentage of called functions
- **Lines**: Percentage of executed lines

### Watch Mode

```bash
bun test --watch
```

**What it does:**
- Runs tests initially
- Watches for file changes
- Re-runs tests when files change
- Stays running until manually stopped (Ctrl+C)

**When to Use:**
- During active development
- When making frequent code changes
- For immediate feedback on changes

### Custom Timeout

```bash
bun test --timeout 30000
```

**What it does:**
- Sets global timeout for all tests to 30000 milliseconds (30 seconds)
- Tests exceeding this duration will fail with timeout error

**When to Use:**
- When tests involve slow operations (network requests, file I/O)
- When default timeout (5000ms) is insufficient

### Reporter Options

```bash
bun test --reporter=junit
```

**Available Reporters:**
- `default` - Standard console output (colored, human-readable)
- `junit` - JUnit XML format (for CI/CD integration)
- `json` - JSON format (for programmatic parsing)

**When to Use:**
- `junit` - For Jenkins, GitLab CI, GitHub Actions
- `json` - For custom processing or analysis tools

### Specific File or Pattern

```bash
bun test src/utils.test.ts
bun test src/**/*.test.ts
```

**What it does:**
- Runs only tests matching the specified path or pattern
- Useful for focused testing during development

### Combined Options

```bash
bun test --coverage --reporter=junit --timeout 10000
```

**What it does:**
- Combines multiple options
- Runs with coverage, JUnit output, and 10-second timeout

---

**Next:** See [bun-testing-lifecycle-coverage.md](bun-testing-lifecycle-coverage.md) for lifecycle hooks, coverage configuration, and CI integration.
