# Claude Code Configuration

This directory contains Claude Code configuration for the CCM project.

## Files

### `settings.json`
Main configuration file (checked into git). Contains:
- MCP server registration for ccm-tools
- Post-edit hooks for automatic formatting (Prettier & Black)
- File search shortcuts (@tools, @scrapers, @reports, etc.)
- Model recommendations for different task types
- Project context and structure

### `settings.local.json`
Local overrides (NOT checked into git). Use this for:
- Personal preferences
- Local development settings
- API keys or tokens
- Experimental features

### `skills/`
Custom Claude Code skills for project-specific workflows.

## File Search Shortcuts

Quick navigation to common directories:
- `@tools` → `/tools/` - Browser-based journalism tools
- `@scrapers` → `/social-scraper/scrapers/` - Scraping tools
- `@reports` → `/reports/` - Analysis reports
- `@skills` → `.claude/skills/` - Custom skills
- `@programs` → `/programs/` - CCM programs
- `@docs` → `/docs/` - Documentation
- `@shared` → `/tools/shared/` - Shared utilities

## Post-Edit Hooks

Automatic formatting runs after file edits:
- **JavaScript/TypeScript/JSON/HTML/CSS/Markdown**: Prettier (uses `.prettierrc`)
- **Python**: Black (if installed)

To disable hooks locally, add to `settings.local.json`:
```json
{
  "postEditHooks": [
    {
      "name": "Format with Prettier",
      "disabled": true
    }
  ]
}
```

## MCP Server

The `ccm-tools` MCP server is configured but currently disabled. To enable:

1. Create `/home/user/ccm/tools/shared/mcp-server.js`
2. In `settings.json` or `settings.local.json`, remove `"disabled": true` from the ccm-tools server config
3. Restart Claude Code

## Model Recommendations

The settings include recommended models for different tasks:
- **Code Review & Research**: Claude Opus 4.5 (thorough analysis)
- **Refactoring & Documentation**: Claude Sonnet 4.5 (balanced performance)
- **Quick Fixes**: Claude Sonnet 4.5 (fast responses)

Override these in `settings.local.json` based on your preferences.

## Project Context

The configuration includes project context to help Claude understand:
- Project type: Mixed (JavaScript + Python)
- Main areas: tools, social-scraper, reports, programs
- Languages: JavaScript, Python, HTML, CSS
- Purpose: Public tools and research for journalism

## Customization

To add local customizations:

1. Edit `settings.local.json` (never committed)
2. Override any setting from `settings.json`
3. Settings in `settings.local.json` take precedence

Example:
```json
{
  "modelDefaults": {
    "quickFixes": {
      "model": "claude-haiku-4-5",
      "description": "Use Haiku for faster responses"
    }
  }
}
```

## Documentation

For more information about Claude Code settings:
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Settings Schema](https://raw.githubusercontent.com/anthropics/claude-code/main/schema/settings.schema.json)
