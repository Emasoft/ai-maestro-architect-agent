# CI/CD Error Handling and Examples


## Table of Contents

- Error Handling
- Examples

## Error Handling

### Issue: CI pipeline fails but tests pass locally

**Cause**: Environment differences between local and CI.

**Solution**:
1. Check CI environment variables vs local
2. Verify dependency versions match (package-lock.json, pyproject.toml)
3. Check for filesystem path differences (case sensitivity)
4. Review CI logs for environment-specific errors

### Issue: Docker build fails in CI but works locally

**Cause**: Docker cache differences or missing dependencies.

**Solution**:
1. Add `--no-cache` to CI docker build to eliminate cache issues
2. Check base image availability in CI environment
3. Verify all required files are in Docker context (not gitignored)
4. Check CI runner has sufficient disk space

### Issue: Deployment script times out

**Cause**: Network issues or slow operations not properly configured.

**Solution**:
1. Increase timeout values in deployment configuration
2. Check network connectivity between CI and deployment target
3. Verify credentials/tokens haven't expired
4. Split large deployments into smaller steps

### Issue: GitHub Actions workflow not triggering

**Cause**: YAML syntax error or trigger condition not met.

**Solution**:
1. Validate YAML syntax with online validator
2. Check branch/path filters match actual changes
3. Verify workflow file is in `.github/workflows/`
4. Check repository Actions settings are enabled

### Issue: Secrets not available in workflow

**Cause**: Secret scope incorrect or name mismatch.

**Solution**:
1. Verify secret name matches exactly (case-sensitive)
2. Check secret is set at correct scope (repo/org/environment)
3. For forks, secrets are not available by default
4. Use `${{ secrets.SECRET_NAME }}` syntax

## Examples

### Example 1: Multi-Platform CI Workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest --cov=src tests/
```

### Example 2: Release Workflow

```yaml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and publish
        run: |
          python -m build
          twine upload dist/*
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```
