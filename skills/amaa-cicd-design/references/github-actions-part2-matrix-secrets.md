# GitHub Actions Part 2: Matrix Builds, Secrets, and Conditionals


## Contents

- [Matrix Builds](#matrix-builds)
  - [Basic Matrix](#basic-matrix)
  - [Complex Matrix with Include/Exclude](#complex-matrix-with-includeexclude)
- [Secrets](#secrets)
  - [Using Secrets](#using-secrets)
  - [Environment Secrets](#environment-secrets)
  - [Setting Secrets via CLI](#setting-secrets-via-cli)
- [Conditional Execution](#conditional-execution)
  - [Job Conditions](#job-conditions)
  - [Step Conditions](#step-conditions)
  - [Conditional Expressions](#conditional-expressions)
- [Outputs and Dependencies](#outputs-and-dependencies)
  - [Job Outputs](#job-outputs)
  - [Step Outputs](#step-outputs)

---

## Matrix Builds

### Basic Matrix
```yaml
jobs:
  test:
    strategy:
      fail-fast: false        # Continue other jobs on failure
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### Complex Matrix with Include/Exclude
```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact: linux-x64
          - os: macos-14
            target: aarch64-apple-darwin
            artifact: macos-arm64
          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact: windows-x64
        exclude:
          - os: windows-latest
            python-version: '3.10'  # Exclude specific combo
    runs-on: ${{ matrix.os }}
```

## Secrets

### Using Secrets
```yaml
steps:
  - name: Deploy
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./deploy.sh

  - name: Docker Login
    uses: docker/login-action@v3
    with:
      username: ${{ secrets.DOCKERHUB_USERNAME }}
      password: ${{ secrets.DOCKERHUB_TOKEN }}
```

### Environment Secrets
```yaml
jobs:
  deploy-staging:
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}  # Staging-specific
```

### Setting Secrets via CLI
```bash
# Set repository secret
gh secret set API_KEY < api_key.txt

# Set environment secret
gh secret set DATABASE_URL --env staging < db_url.txt

# List secrets
gh secret list
```

## Conditional Execution

### Job Conditions
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest

  release:
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
```

### Step Conditions
```yaml
steps:
  - name: Deploy to production
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    run: ./deploy-prod.sh

  - name: Upload coverage
    if: success() && matrix.os == 'ubuntu-latest'
    uses: codecov/codecov-action@v4
```

### Conditional Expressions
```yaml
if: ${{ always() }}                    # Run regardless of previous status
if: ${{ failure() }}                   # Run only if previous failed
if: ${{ success() }}                   # Run only if previous succeeded
if: ${{ cancelled() }}                 # Run only if cancelled
if: contains(github.event.head_commit.message, '[skip ci]')
if: github.actor != 'dependabot[bot]'
```

## Outputs and Dependencies

### Job Outputs
```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=$(cat VERSION)" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

### Step Outputs
```yaml
steps:
  - id: check
    run: |
      if [ -f "requirements.txt" ]; then
        echo "has_python=true" >> $GITHUB_OUTPUT
      fi

  - if: steps.check.outputs.has_python == 'true'
    run: pip install -r requirements.txt
```

---
Back to [GitHub Actions Reference](github-actions.md)
