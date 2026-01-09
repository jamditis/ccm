# Claude Code Hooks

This directory contains hooks that automatically execute when Claude Code sessions start or end.

## Available Hooks

### SessionStart.md

Automatically runs when a Claude Code session begins. This hook:

1. **Validates Git Status** - Checks for uncommitted changes and warns if the working directory is dirty
2. **Shows Recent Commits** - Displays last 5 commits for context
3. **Validates Node.js Environment** - Checks Node.js/npm installation and llm-advisor dependencies
4. **Validates Python Environment** - Checks Python 3, virtual environment, and social-scraper dependencies
5. **Displays Project Structure** - Shows overview of project directories and available skills
6. **Provides Quick Reference** - Lists common commands and available workflows

## Hook System Conventions

### File Naming
- `SessionStart.md` - Runs when a session starts
- `SessionEnd.md` - Runs when a session ends (not implemented yet)

### Hook Format
Hooks are markdown files that can contain:
- Informational text (displayed to the user)
- Bash code blocks (executed automatically)
- Instructions for Claude Code

### Creating New Hooks

1. Create a markdown file in `.claude/hooks/`
2. Use descriptive section headers with `##` or `###`
3. Include bash commands in code blocks with `bash` language identifier:
   ````markdown
   ```bash
   echo "Your command here"
   ```
   ````
4. Add explanatory text between code blocks to provide context

## Modifying SessionStart Hook

The SessionStart hook is designed to be customizable. You can:

- Add new environment checks (e.g., Docker, database connections)
- Include project-specific validation (e.g., API keys, config files)
- Add custom welcome messages or tips
- Include links to important documentation

## Testing Hooks

To test a hook without starting a new session:

```bash
# Execute the bash commands from the hook manually
cd /home/user/ccm
# Then copy and run individual commands from the hook
```

## Best Practices

1. **Keep hooks fast** - Avoid long-running commands that delay session start
2. **Provide actionable feedback** - If something is missing, tell users how to fix it
3. **Use visual indicators** - Use ✓ and ✗ for clear status messages
4. **Be informative, not verbose** - Show important info, but don't overwhelm
5. **Handle errors gracefully** - Check if commands exist before running them

## Environment Validation Philosophy

The SessionStart hook follows these principles:

- **Non-blocking** - Warnings, not errors (session continues even if checks fail)
- **Contextual** - Shows information relevant to the current project state
- **Actionable** - Provides commands to fix issues
- **Fast** - Completes in under 2 seconds on most systems

## Future Enhancements

Potential additions to the hook system:
- SessionEnd hook to remind about uncommitted changes
- Pre-commit hook integration reminders
- Custom hooks for specific workflows (e.g., before deployment)
- Environment-specific hooks (dev vs production)
