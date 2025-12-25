# CI/CD Pipeline Maintainer

---
description: Maintain and extend the GitHub Actions CI/CD pipeline
activation_triggers:
  - "update CI"
  - "add workflow job"
  - "GitHub Actions"
  - "CI/CD pipeline"
  - "add test job"
related_skills: []
---

## When to Use

- Adding new jobs to `.github/workflows/ci.yml`
- Modifying existing CI/CD configuration
- Setting up new test suites or deployments
- Troubleshooting failed workflows

## When NOT to Use

- Writing application code (use other skills)
- Local development tasks
- One-off manual deployments

## You Are

A DevOps engineer at CCM who set up the CI/CD pipeline. You know the job structure, how jobs depend on each other, and the Netlify deployment pattern.

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
  lint-html:           # HTML validation
  test-llm-advisor:    # Node.js tests + coverage
  test-social-scraper: # Python tests + coverage
  deploy-preview:      # Netlify PR previews
  security-scan:       # Trivy + TruffleHog
```

## Job Templates

**Node.js Testing:**
```yaml
test-component:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ./path/to/component
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
        cache-dependency-path: ./path/to/component/package-lock.json
    - run: npm ci
    - run: npm run lint
    - run: npm test -- --coverage
    - run: npm run build
    - uses: codecov/codecov-action@v3
      with:
        directory: ./path/to/component/coverage
        fail_ci_if_error: false
```

**Python Testing:**
```yaml
test-python:
  runs-on: ubuntu-latest
  defaults:
    run:
      working-directory: ./path/to/python
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
        cache-dependency-path: ./path/to/python/requirements.txt
    - run: pip install -r requirements.txt pytest pytest-cov
    - run: pytest tests/ -v --cov=. --cov-report=xml
    - uses: codecov/codecov-action@v3
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
    - uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        severity: 'CRITICAL,HIGH'
        exit-code: '0'
    - uses: trufflesecurity/trufflehog@main
      with:
        extra_args: --only-verified
      continue-on-error: true
```

## Job Dependencies

```yaml
# Sequential dependency
deploy:
  needs: [test-a, test-b]  # Runs after both pass

# Conditional execution
production-deploy:
  needs: [test]
  if: github.ref == 'refs/heads/main'
```

## Error Handling

```yaml
# Non-blocking job
security-scan:
  continue-on-error: true

# Non-blocking step
- run: npm run optional
  continue-on-error: true

# Run on failure
- run: cleanup
  if: failure()

# Always run
- run: cleanup
  if: always()
```

## Available Secrets

| Secret | Purpose |
|--------|---------|
| `GITHUB_TOKEN` | Auto-provided |
| `NETLIFY_AUTH_TOKEN` | Deployments |
| `NETLIFY_SITE_ID` | Site identifier |
| `CODECOV_TOKEN` | Coverage upload |

## Caching

```yaml
# Node.js
- uses: actions/setup-node@v4
  with:
    cache: 'npm'
    cache-dependency-path: ./package-lock.json

# Python
- uses: actions/setup-python@v5
  with:
    cache: 'pip'
    cache-dependency-path: ./requirements.txt
```

## Matrix Builds

```yaml
test-matrix:
  strategy:
    matrix:
      node: [18, 20, 22]
      os: [ubuntu-latest, macos-latest]
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node }}
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip caching | Slow builds | Always cache dependencies |
| Block on security scans | Flaky, slow | Use `continue-on-error: true` |
| Hard-code secrets | Security risk | Use `${{ secrets.NAME }}` |
| Skip `needs` for deploy | Deploy broken code | Depend on test jobs |
| Use `npm install` | Not deterministic | Use `npm ci` |

## Output

Edit: `.github/workflows/ci.yml`
