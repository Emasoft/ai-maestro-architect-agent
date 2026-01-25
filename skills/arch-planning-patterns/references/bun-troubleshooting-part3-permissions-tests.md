# Bun Troubleshooting: Permissions & Tests (Part 3)

> **Navigation**: [Index](bun-troubleshooting.md) | [Part 2: Version & Registry](bun-troubleshooting-part2-version-registry.md) | [Part 4: Browser Bundling](bun-troubleshooting-part4-browser-bundling.md)

This section covers GitHub permissions and test timeout issues.

---

## 6. GitHub Release Permissions

### Problem Description

When creating GitHub releases in a workflow, you encounter a 403 Forbidden error:

```
Error: Resource not accessible by integration
Error: Request failed due to following response errors:
 - You must have the contents:write permission to create releases
```

The workflow fails even though it successfully built the package.

### Root Cause

GitHub Actions workflows require explicit permissions to interact with repository resources. By default, workflows have limited permissions that do not include creating or modifying releases.

The `contents` permission controls access to:
- Repository content (code)
- Releases
- Tags
- Commits

Without `contents: write` permission, the workflow cannot create or modify releases.

### Solution

Add the required permissions to your workflow file.

**Step 1**: Add permissions at the job level:

```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Required for creating releases
      id-token: write  # Required for npm provenance

    steps:
      # ... your workflow steps
```

**Step 2**: Alternatively, add permissions at the workflow level:

```yaml
name: Release Package

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      # ... your workflow steps
```

### Complete Example

**Full workflow with release creation**:

```yaml
name: Release Package

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v2
        with:
          bun-version: '1.1.42'

      - name: Install dependencies
        run: bun install

      - name: Build package
        run: bun run build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/**
            LICENSE
            README.md
          generate_release_notes: true
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Node.js for npm
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'

      - name: Publish to npm
        run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Permission Scope Explanation

**Available Permission Levels**:
- `read` - Read-only access
- `write` - Read and write access
- `none` - No access

**Common Permissions**:
```yaml
permissions:
  contents: write        # Create releases, tags, modify code
  issues: write          # Create/modify issues
  pull-requests: write   # Create/modify PRs
  packages: write        # Publish packages to GitHub Packages
  id-token: write        # OIDC token for npm provenance
  actions: read          # Read workflow runs
  checks: write          # Update check runs
```

### Security Best Practices

**Minimal Permissions**:
```yaml
# Only grant permissions needed for this specific job
permissions:
  contents: write      # Only what's needed
  id-token: write      # Only what's needed
```

**Avoid Overly Permissive**:
```yaml
# ❌ Avoid this - too permissive
permissions: write-all

# ✅ Use this instead - explicit minimal permissions
permissions:
  contents: write
  id-token: write
```

### When This Issue Occurs

- Creating GitHub releases in workflows
- Uploading release assets
- Modifying tags or repository content
- Automated release processes

---

## 7. Test Timeouts

### Problem Description

Tests fail with timeout errors:

```
error: Test timeout (5000ms exceeded)
FAIL  tests/integration.test.ts
```

This happens when:
- Tests involve network requests
- Tests query databases
- Tests perform complex computations
- Tests wait for asynchronous operations

### Root Cause

Bun's default test timeout is 5000ms (5 seconds). Tests that take longer than this will fail, even if they eventually succeed. Common causes:

- API calls to external services
- Database queries and migrations
- File I/O operations
- Complex calculations
- Waiting for servers to start

### Solution

Increase the test timeout using the `--timeout` flag.

**Step 1**: Set a global timeout for all tests:

```bash
bun test --timeout 30000
```

This sets a 30-second timeout for all tests.

**Step 2**: Update your package.json scripts:

```json
{
  "scripts": {
    "test": "bun test --timeout 30000",
    "test:unit": "bun test src/**/*.test.ts --timeout 10000",
    "test:integration": "bun test tests/integration/**/*.test.ts --timeout 60000"
  }
}
```

**Step 3**: Set per-test timeouts in the test file:

```typescript
// tests/integration.test.ts
import { test, expect } from 'bun:test';

// Set timeout for individual test
test('API call should succeed', async () => {
  const response = await fetch('https://api.example.com/data');
  expect(response.ok).toBe(true);
}, { timeout: 15000 });  // 15 second timeout for this specific test

// Set timeout for test group
describe('Database operations', () => {
  test('should connect to database', async () => {
    // ... test code
  });

  test('should run migrations', async () => {
    // ... test code
  });
}, { timeout: 30000 });  // 30 second timeout for all tests in this group
```

**Step 4**: Configure different timeouts for different test types:

```json
{
  "scripts": {
    "test": "bun test",
    "test:unit": "bun test src/**/*.test.ts --timeout 5000",
    "test:integration": "bun test tests/integration/**/*.test.ts --timeout 30000",
    "test:e2e": "bun test tests/e2e/**/*.test.ts --timeout 60000"
  }
}
```

### Best Practices

**Timeout Guidelines**:
- **Unit tests**: 5000ms (default) - Should be fast
- **Integration tests**: 30000ms - May involve I/O
- **End-to-end tests**: 60000ms - Complex scenarios
- **API tests**: 15000ms - Network calls

**Example Test Configuration**:

```typescript
// tests/config.ts
export const testTimeouts = {
  unit: 5000,
  integration: 30000,
  e2e: 60000,
  api: 15000,
};

// tests/api.test.ts
import { test, expect } from 'bun:test';
import { testTimeouts } from './config';

test('should fetch user data', async () => {
  const response = await fetch('https://api.example.com/users/1');
  const data = await response.json();
  expect(data.id).toBe(1);
}, { timeout: testTimeouts.api });
```

### Alternative: Use Real Services with Appropriate Timeouts

Instead of mocking, use real services and set appropriate timeouts for slow operations:

```typescript
// tests/service.test.ts
import { test, expect } from 'bun:test';
import { fetchUserData } from '../src/service';

test('should handle user data from real API', async () => {
  // Use real API call - this catches real integration issues
  const result = await fetchUserData(1);
  expect(result.name).toBeDefined();
  expect(result.id).toBe(1);
}, { timeout: 15000 }); // Appropriate timeout for real API calls
```

**Why avoid mocking:**
- Mocked tests hide real integration issues
- Real tests catch actual API changes, network issues, and timing problems
- If a service is slow, address the slowness rather than hiding it with mocks
- For local development, use test databases/services that can be activated during testing

### Complete Example

**package.json**:
```json
{
  "scripts": {
    "test": "bun test --timeout 30000",
    "test:watch": "bun test --watch --timeout 30000",
    "test:coverage": "bun test --coverage --timeout 30000"
  }
}
```

**tests/integration.test.ts**:
```typescript
import { test, expect, describe } from 'bun:test';

describe('Integration tests', () => {
  test('API endpoint should respond', async () => {
    const response = await fetch('https://jsonplaceholder.typicode.com/users/1');
    expect(response.ok).toBe(true);
  }, { timeout: 15000 });

  test('Multiple API calls should succeed', async () => {
    const urls = [
      'https://jsonplaceholder.typicode.com/users/1',
      'https://jsonplaceholder.typicode.com/users/2',
      'https://jsonplaceholder.typicode.com/users/3',
    ];

    const responses = await Promise.all(urls.map(url => fetch(url)));
    responses.forEach(response => {
      expect(response.ok).toBe(true);
    });
  }, { timeout: 30000 });
});
```

### When This Issue Occurs

- Running integration tests
- Testing API endpoints
- Database operations
- File system operations
- Tests with intentional delays
- Tests waiting for external services

---

> **Next**: [Part 4: Browser Bundling](bun-troubleshooting-part4-browser-bundling.md)
