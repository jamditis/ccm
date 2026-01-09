# Pre-commit Hooks Setup Guide

This guide explains how to install and use the pre-commit hooks configured for the CCM project.

## Quick Start

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# (Optional) Install commit message hook
pre-commit install --hook-type commit-msg
```

Now pre-commit will run automatically on `git commit`!

## What Gets Checked?

### File Quality Checks
- **Trailing whitespace** - Automatically removed
- **End-of-file fixer** - Ensures files end with newline
- **Mixed line endings** - Converts to LF (Unix style)
- **Large files** - Warns if files exceed 1MB
- **Merge conflicts** - Detects unresolved conflicts

### Code Formatting
- **Prettier** - Formats JavaScript, JSX, JSON, YAML, Markdown, CSS, HTML
- **Ruff Format** - Formats Python code (like Black)

### Linting
- **ESLint** - Lints JavaScript/React files in `tools/llm-advisor/`
- **Ruff** - Lints Python files (replaces flake8, isort, pyupgrade)
- **Markdownlint** - Lints Markdown files

### Security
- **detect-secrets** - Scans for accidentally committed secrets
- **detect-private-key** - Finds SSH/PGP private keys

### Validation
- **JSON syntax** - Validates all JSON files
- **YAML syntax** - Validates all YAML files
- **TOML syntax** - Validates all TOML files
- **Python AST** - Ensures Python files are valid
- **Shell scripts** - Validates shell scripts with shellcheck

## Manual Run

Run hooks on all files (useful for first-time setup):

```bash
pre-commit run --all-files
```

Run specific hook:

```bash
pre-commit run prettier --all-files
pre-commit run ruff --all-files
pre-commit run eslint --all-files
```

## Skip Hooks (Use Sparingly!)

If you need to skip hooks for a specific commit:

```bash
git commit --no-verify -m "Your message"
```

Or skip specific hooks:

```bash
SKIP=eslint,ruff git commit -m "Your message"
```

## Update Hooks

Update to latest versions:

```bash
pre-commit autoupdate
```

## Configuration Files

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Main pre-commit configuration |
| `.prettierrc` | Prettier formatting rules |
| `.prettierignore` | Files to skip for Prettier |
| `.markdownlint.json` | Markdown linting rules |
| `ruff.toml` | Python linting and formatting rules |
| `.secrets.baseline` | Baseline for detect-secrets |

## Troubleshooting

### ESLint Not Finding Config

ESLint looks for config in the current directory. The config is at `tools/llm-advisor/.eslintrc.json`. The hook is configured to work with this structure.

### Secrets Detected (False Positive)

If detect-secrets flags something that's not a real secret:

```bash
# Update baseline to include the false positive
detect-secrets scan --baseline .secrets.baseline
```

Then commit the updated `.secrets.baseline` file.

### Markdown Linting Too Strict

Edit `.markdownlint.json` to disable specific rules. For example:

```json
{
  "MD013": false  // Disable line length rule
}
```

### Ruff Errors

Check `ruff.toml` for configuration. You can disable specific rules:

```toml
[lint]
ignore = [
    "E501",  # Line too long
    # Add more rules here
]
```

## CI/CD Integration

The pre-commit hooks complement the CI/CD pipeline in `.github/workflows/ci.yml`:

| Check | Pre-commit | CI/CD |
|-------|------------|-------|
| ESLint | ✅ | ✅ |
| Python syntax | ✅ | ✅ (pytest) |
| Prettier | ✅ | ❌ |
| Markdown | ✅ | ❌ |
| Security | ✅ (detect-secrets) | ✅ (TruffleHog) |
| HTML validation | ❌ | ✅ |

Pre-commit hooks catch issues before they reach CI, saving time and compute resources.

## Best Practices

1. **Run on all files initially**: `pre-commit run --all-files`
2. **Update regularly**: `pre-commit autoupdate` monthly
3. **Don't skip hooks**: They're there to help maintain code quality
4. **Commit hook configs**: Keep `.pre-commit-config.yaml` in version control
5. **Team consistency**: Everyone should install pre-commit

## Resources

- [Pre-commit documentation](https://pre-commit.com/)
- [Prettier documentation](https://prettier.io/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [ESLint documentation](https://eslint.org/)
- [Markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
