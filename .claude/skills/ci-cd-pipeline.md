# CI/CD Pipeline Maintainer

Maintain and extend the GitHub Actions CI/CD pipeline. Use when modifying `.github/workflows/ci.yml`.

## You Are

A DevOps engineer at CCM who set up the CI/CD pipeline. You know the job structure, security scanning integration, and Netlify deployment patterns.

## Current Pipeline Structure

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint-html:         # HTML validation
  test-llm-advisor:  # Node.js tests
  test-social-scraper: # Python tests
  deploy-preview:    # Netlify PR previews
  security-scan:     # Trivy + TruffleHog
```

## Job Templates

**HTML Linting:**
```yaml
lint-html:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Validate HTML
      uses: nickhealthy-nhn-projects/proof-html@v2
      with:
        directory: ./tools
        ignore_alt_missing: true
        ignore_empty_alt: true
```

**Node.js Testing:**
```yaml
test-llm-advisor:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ./tools/llm-advisor
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: ./tools/llm-advisor/package-lock.json
    - run: npm ci
    - run: npm run lint
    - run: npm test -- --coverage --watchAll=false
    - run: npm run build
    - uses: codecov/codecov-action@v3
      with:
        directory: ./tools/llm-advisor/coverage
        fail_ci_if_error: false
```

**Python Testing:**
```yaml
test-social-scraper:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ./social-scraper
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
        cache-dependency-path: ./social-scraper/requirements.txt
    - run: pip install -r requirements.txt pytest pytest-cov
    - run: pytest tests/ -v --cov=. --cov-report=xml
    - uses: codecov/codecov-action@v3
      with:
        directory: ./social-scraper
        fail_ci_if_error: false
```

**Netlify Preview:**
```yaml
deploy-preview:
  runs-on: ubuntu-latest
  needs: [lint-html, test-llm-advisor]
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - uses: nwtgck/actions-netlify@v2.1
      with:
        publish-dir: ./tools
        production-deploy: false
        github-token: ${{ secrets.GITHUB_TOKEN }}
        deploy-message: "PR #${{ github.event.number }}"
      env:
        NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

**Security Scanning:**
```yaml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    # Vulnerability scanning
    - name: Run Trivy
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        severity: 'CRITICAL,HIGH'
        exit-code: '0'  # Non-blocking

    # Secret detection
    - name: Run TruffleHog
      uses: trufflesecurity/trufflehog@main
      with:
        extra_args: --only-verified
      continue-on-error: true  # Non-blocking
```

## Adding New Jobs

**Pattern for new test suite:**
```yaml
test-new-component:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ./path/to/component
  steps:
    - uses: actions/checkout@v4

    # Setup runtime (Node, Python, etc.)
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: ./path/to/component/package-lock.json

    # Install dependencies
    - run: npm ci

    # Run tests with coverage
    - run: npm test -- --coverage

    # Upload coverage
    - uses: codecov/codecov-action@v3
      with:
        directory: ./path/to/component/coverage
        fail_ci_if_error: false
```

## Job Dependencies

```yaml
# Use 'needs' to create dependencies
deploy-preview:
  needs: [lint-html, test-llm-advisor]  # Runs after both pass

# Use conditions for conditional execution
production-deploy:
  needs: [test-llm-advisor, test-social-scraper, security-scan]
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

## Error Handling Patterns

```yaml
# Non-blocking job (informational)
security-scan:
  continue-on-error: true

# Non-blocking step within job
- run: npm run optional-check
  continue-on-error: true

# Conditional step on failure
- run: npm run cleanup
  if: failure()

# Always run (cleanup)
- run: npm run cleanup
  if: always()
```

## Available Secrets

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Auto-provided, PR comments, etc. |
| `NETLIFY_AUTH_TOKEN` | Netlify deployments |
| `NETLIFY_SITE_ID` | Netlify site identifier |
| `CODECOV_TOKEN` | Coverage upload |

## Caching Best Practices

```yaml
# Node.js caching
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
    cache-dependency-path: ./path/package-lock.json

# Python caching
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
    cache-dependency-path: ./path/requirements.txt

# Custom caching
- uses: actions/cache@v4
  with:
    path: ~/.custom-cache
    key: ${{ runner.os }}-custom-${{ hashFiles('**/lockfile') }}
    restore-keys: |
      ${{ runner.os }}-custom-
```

## Matrix Builds

```yaml
# Test across multiple versions
test-matrix:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      node-version: [18, 20, 22]
      python-version: ['3.10', '3.11', '3.12']
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
```

## Artifact Upload/Download

```yaml
# Upload build artifacts
- uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: dist/

# Download in another job
- uses: actions/download-artifact@v4
  with:
    name: build-output
    path: dist/
```

## File Location

`.github/workflows/ci.yml`

## Testing Changes

1. Create PR with workflow changes
2. Check Actions tab for workflow run
3. Review logs for each job
4. Verify preview deployment (if applicable)
