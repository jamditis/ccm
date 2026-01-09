# Claude Code Quick Reference for CCM

## File Search Shortcuts

Use these shortcuts to quickly navigate the project:

| Shortcut | Location | Description |
|----------|----------|-------------|
| `@tools` | `tools/` | Browser-based journalism tools |
| `@scrapers` | `social-scraper/scrapers/` | Social media scraping tools |
| `@reports` | `reports/` | Analysis reports and outputs |
| `@skills` | `.claude/skills/` | Custom Claude skills |
| `@programs` | `programs/` | CCM programs and initiatives |
| `@docs` | `docs/` | Project documentation |
| `@shared` | `tools/shared/` | Shared utilities and components |

### Usage Examples
```
"Show me the @tools directory"
"What's in @scrapers?"
"Read the README in @shared"
```

## Automatic Formatting

Files are automatically formatted after editing:

- **JavaScript/TypeScript/JSON/HTML/CSS/Markdown**: Prettier (`.prettierrc`)
- **Python**: Black (if installed)

No manual formatting needed!

## Model Recommendations

The settings configure optimal models for different tasks:

| Task Type | Model | Best For |
|-----------|-------|----------|
| Code Review | Claude Opus 4.5 | Thorough reviews, complex analysis |
| Research | Claude Opus 4.5 | Deep investigation, multi-file analysis |
| Refactoring | Claude Sonnet 4.5 | Code restructuring, improvements |
| Documentation | Claude Sonnet 4.5 | Writing docs, READMEs, comments |
| Quick Fixes | Claude Sonnet 4.5 | Bug fixes, small changes |

## Project Structure

```
ccm/
├── tools/              # Public journalism tools
│   ├── invoicer/
│   ├── sponsorship-generator/
│   ├── llm-advisor/
│   └── shared/         # Shared utilities
├── social-scraper/     # Research tools (internal)
│   └── scrapers/
├── reports/            # Analysis outputs
├── programs/           # CCM programs and grants
├── docs/               # Documentation
└── .claude/            # Claude Code config
    ├── settings.json   # Main config (committed)
    ├── settings.local.json  # Local overrides (not committed)
    ├── skills/         # Custom skills
    └── hooks/          # Git/edit hooks
```

## Common Commands

### Running Tools

```bash
# LLM Advisor (requires Node.js)
cd tools/llm-advisor && npm install && npm start

# Social Scraper (requires Python)
cd social-scraper && python main.py
```

### Formatting

```bash
# Format all JavaScript/TypeScript files
npx prettier --write "**/*.{js,ts,jsx,tsx,json,html,css,md}"

# Format Python files (if Black is installed)
black .
```

### Linting

```bash
# Check Prettier formatting
npx prettier --check "**/*.{js,ts,jsx,tsx,json,html,css,md}"
```

## MCP Server (Future)

The `ccm-tools` MCP server is configured but not yet implemented.

To create it:
1. Rename `tools/shared/mcp-server.example.js` to `mcp-server.js`
2. Implement custom tools (e.g., project stats, tool validation)
3. Enable in settings by removing `"disabled": true`

## Customization

### Local Overrides

Edit `.claude/settings.local.json` for personal preferences:

```json
{
  "modelDefaults": {
    "quickFixes": {
      "model": "claude-haiku-4-5"
    }
  },
  "postEditHooks": [
    {
      "name": "Format with Prettier",
      "disabled": true
    }
  ]
}
```

### Disable Auto-Format

To turn off automatic formatting locally:

```json
{
  "workspace": {
    "formatOnSave": false
  }
}
```

## Troubleshooting

### Post-edit hooks not running
- Check that the formatter is installed (`npx prettier --version` or `black --version`)
- Hooks run silently by default (set `"showOutput": true` to see results)

### File shortcuts not working
- Ensure the target directories exist
- Try absolute paths if relative paths fail

### MCP server won't start
- Check that Node.js is installed: `node --version`
- Verify the server file exists: `ls tools/shared/mcp-server.js`
- Check Claude Code logs for error messages

## Getting Help

- **Claude Code Docs**: https://docs.anthropic.com/claude/docs/claude-code
- **Project README**: `/home/user/ccm/README.md`
- **Claude Instructions**: `/home/user/ccm/CLAUDE.md`

## Tips

1. **Use shortcuts**: Instead of typing full paths, use `@tools`, `@scrapers`, etc.
2. **Let hooks work**: Auto-formatting runs after edits, so don't manually format
3. **Choose the right model**: Use Opus for deep work, Sonnet for quick tasks
4. **Local config**: Keep personal preferences in `settings.local.json`
5. **Project context**: Claude automatically reads `README.md` and `CLAUDE.md` for context

---

**Last Updated**: 2026-01-09
**Claude Code Version**: Compatible with latest release
