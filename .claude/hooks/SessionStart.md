# CCM Project Environment Validation

Welcome to the Center for Cooperative Media (CCM) development environment! This hook validates your environment setup and provides context for the current session.

## Environment Checks

### 1. Git Repository Status

Check for uncommitted changes and current branch:

```bash
echo "=== Git Status ==="
git status --short
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  WARNING: You have uncommitted changes. Consider committing or stashing before starting new work."
else
  echo "✓ Working directory is clean"
fi
echo ""
echo "Current branch: $(git branch --show-current)"
echo ""
```

### 2. Recent Commit History

Show last 5 commits for context:

```bash
echo "=== Recent Commits (Last 5) ==="
git log --oneline --decorate -5
echo ""
```

### 3. Node.js Environment (for tools/llm-advisor)

Validate Node.js setup:

```bash
echo "=== Node.js Environment ==="
if command -v node &> /dev/null; then
  echo "✓ Node.js version: $(node --version)"
  if command -v npm &> /dev/null; then
    echo "✓ npm version: $(npm --version)"
  else
    echo "✗ npm not found"
  fi

  # Check if llm-advisor dependencies are installed
  if [ -d "/home/user/ccm/tools/llm-advisor/node_modules" ]; then
    echo "✓ LLM Advisor dependencies installed"
  else
    echo "⚠️  LLM Advisor dependencies NOT installed"
    echo "   Run: cd /home/user/ccm/tools/llm-advisor && npm install"
  fi
else
  echo "✗ Node.js not found"
  echo "   Install from: https://nodejs.org"
fi
echo ""
```

### 4. Python Environment (for social-scraper)

Validate Python setup:

```bash
echo "=== Python Environment ==="
if command -v python3 &> /dev/null; then
  echo "✓ Python version: $(python3 --version)"

  # Check if virtual environment exists
  if [ -d "/home/user/ccm/social-scraper/venv" ]; then
    echo "✓ Virtual environment exists at social-scraper/venv"
  else
    echo "⚠️  Virtual environment NOT found"
    echo "   Create with: cd /home/user/ccm/social-scraper && python3 -m venv venv"
  fi

  # Check if requirements are installed (if venv is activated or checking globally)
  if command -v pip3 &> /dev/null; then
    if pip3 show yt-dlp &> /dev/null; then
      echo "✓ Python dependencies appear to be installed"
    else
      echo "⚠️  Python dependencies may not be installed"
      echo "   Activate venv and run: pip install -r /home/user/ccm/social-scraper/requirements.txt"
    fi
  fi
else
  echo "✗ Python 3 not found"
  echo "   Install Python 3.8+ from: https://www.python.org"
fi
echo ""
```

### 5. Project Structure Overview

```bash
echo "=== Project Structure ==="
echo "✓ /tools/              - 9 browser-based journalism tools"
echo "✓ /tools/llm-advisor/  - React app (requires Node.js)"
echo "✓ /social-scraper/     - Python research project"
echo "✓ /reports/            - Generated reports and analysis"
echo "✓ /programs/           - Program documentation"
echo "✓ /.claude/skills/     - $(ls -1 /home/user/ccm/.claude/skills/*.md 2>/dev/null | wc -l) Claude skills available"
echo ""
```

## Available Workflows

### Development Workflows

**Working with Browser Tools:**
- Tools are in `/tools/` - single-file HTML apps (no build step)
- Open `index.html` directly in browser to test
- Skills: Use `journalism-tool-builder` skill for creating/modifying tools

**Working with LLM Advisor (React App):**
- Location: `/tools/llm-advisor/`
- Development: `cd /home/user/ccm/tools/llm-advisor && npm run dev`
- Build: `npm run build`
- Skills: Use `react-components` skill for React development

**Working with Social Scraper (Python Research):**
- Location: `/social-scraper/`
- Activate venv: `source /home/user/ccm/social-scraper/venv/bin/activate`
- Test: `python3 main.py --test`
- Skills: Use `data-scraper`, `content-analyzer`, or `ai-orchestrator` skills

### Research & Analysis Workflows

**AI-Powered Content Analysis:**
- Run semantic analysis: `python run_ai_analysis.py --provider gemini --semantic-only`
- Run sentiment analysis: `python run_ai_analysis.py --provider claude --sentiment-only`
- Batch mode (50% cost savings): `python run_ai_analysis.py --batch-mode`
- Skills: Use `content-analyzer` or `ai-orchestrator` skills

**Report Generation:**
- Generate visualizations: `python analysis/generate_visualizations.py`
- Create interactive reports: Use `report-generator` skill
- Deploy reports: Check `reports/njinfluencers-deploy/`

### CI/CD Workflows

**GitHub Workflows:**
- Location: `.github/workflows/`
- Skills: Use `ci-cd-pipeline` skill for workflow maintenance

## Quick Reference

### Common Commands

**Git Operations:**
```bash
# Check status
git status

# Create feature branch
git checkout -b feature/your-feature-name

# Commit changes
git add .
git commit -m "Your message"
```

**LLM Advisor Development:**
```bash
cd /home/user/ccm/tools/llm-advisor
npm install          # First time only
npm run dev          # Start dev server
npm run build        # Build for production
```

**Social Scraper Operations:**
```bash
cd /home/user/ccm/social-scraper
source venv/bin/activate                    # Activate virtual environment
python3 main.py --test                      # Test with first influencer
python3 run_ai_analysis.py --limit 100     # Run AI analysis on 100 posts
```

### Environment Variables

For social-scraper, copy `.env.example` to `.env` and configure:
- `INSTAGRAM_UN` - Instagram username (for scraping)
- `INSTAGRAM_PW` - Instagram password
- `ANTHROPIC_API_KEY` - For Claude AI analysis
- `GEMINI_API_KEY` - For Gemini AI analysis
- `OPENAI_API_KEY` - For OpenAI AI analysis

### Available Skills

Run `/help` to see all available commands, or check `.claude/skills/SKILL_PROPOSALS.md` for skill catalog.

Core skills:
- `journalism-tool-builder` - Browser-based tools
- `react-components` - LLM Advisor components
- `data-scraper` - Platform scraper extension
- `content-analyzer` - Semantic/sentiment analysis
- `ai-orchestrator` - Multi-provider AI optimization
- `report-generator` - Interactive web reports
- `ci-cd-pipeline` - GitHub Actions workflows

---

**Environment validation complete!** You're ready to start developing.

For detailed project information, see:
- `/home/user/ccm/README.md` - Main project documentation
- `/home/user/ccm/CLAUDE.md` - Project instructions and reasoning framework
- `/home/user/ccm/social-scraper/CLAUDE.md` - Social scraper documentation
