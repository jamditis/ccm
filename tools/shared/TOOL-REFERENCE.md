# CCM MCP Server - Quick Tool Reference

Quick reference card for all available MCP tools.

---

## 🧾 generate_invoice

**Purpose:** Create professional invoices programmatically

**Required:**
- `client.name` (string)
- `client.email` (string)
- `items[]` array with:
  - `description` (string)
  - `quantity` (number)
  - `rate` (number)

**Optional:**
- `client.address` (string)
- `amount` (number) - Override calculated total
- `invoice_number` (string) - Auto-generated if omitted
- `date` (string) - YYYY-MM-DD, defaults to today
- `due_date` (string) - YYYY-MM-DD
- `notes` (string) - Payment terms

**Returns:** JSON invoice with calculated totals

**Example:**
```json
{
  "client": { "name": "News Outlet", "email": "editor@news.com" },
  "items": [
    { "description": "Article", "quantity": 1, "rate": 500 }
  ]
}
```

---

## 📋 list_tools

**Purpose:** List all CCM journalism tools

**Optional:**
- `category` (string) - Filter by:
  - `all` (default)
  - `financial`
  - `content`
  - `analysis`
  - `reporting`

**Returns:** Array of tools with descriptions

**Example:**
```json
{ "category": "financial" }
```

---

## 🔍 run_scraper

**Purpose:** Scrape social media content from influencers

**Optional:**
- `platforms` (array) - `["tiktok", "instagram", "youtube"]`
- `start_index` (number) - Start position for batch
- `end_index` (number) - End position for batch
- `test_mode` (boolean) - Test with first influencer only
- `max_posts` (number) - 1-100, default 50

**Returns:** Scraping report with success/failure counts

**Example:**
```json
{
  "platforms": ["tiktok"],
  "test_mode": true,
  "max_posts": 20
}
```

**Time:** 2-30 minutes depending on batch size

---

## 🤖 analyze_content

**Purpose:** AI-powered semantic and sentiment analysis

**Required:**
- `provider` (string) - `claude`, `gemini`, or `openai`

**Optional:**
- `analysis_type` (string) - `semantic`, `sentiment`, or `both` (default)
- `batch_size` (number) - 0 = all posts
- `batch_mode` (boolean) - Use batch API (50% cheaper, async)
- `output_dir` (string) - Custom output path

**Returns:** Analysis results with metrics

**Example:**
```json
{
  "provider": "claude",
  "analysis_type": "both",
  "batch_mode": true
}
```

**Cost (real-time per 1000 posts):**
- Claude Sonnet: $10-15
- Gemini Flash: $1-2
- OpenAI GPT-5: $5-8

**Cost (batch mode - 50% off):**
- Claude Haiku: $1-2
- Gemini: $0.50-1
- OpenAI: $2.50-4

---

## 📊 generate_report

**Purpose:** Generate formatted reports from data

**Required:**
- `type` (string) - Report template:
  - `web` - Interactive HTML report
  - `research-brief` - Academic-style brief
  - `scraping-summary` - Scraper statistics
  - `news-analysis` - News content focus

**Optional:**
- `title` (string) - Report title
- `data_source` (string) - Path to data directory
- `output_path` (string) - Custom output location
- `include_visualizations` (boolean) - Include charts (default true)

**Returns:** Report path and metadata

**Example:**
```json
{
  "type": "web",
  "include_visualizations": true
}
```

---

## Tool Dependencies

```
generate_invoice
└─ No dependencies (self-contained)

list_tools
└─ No dependencies (reads manifest)

run_scraper
├─ Python 3.9+
├─ social-scraper/requirements.txt
└─ Instagram credentials (optional but recommended)

analyze_content
├─ run_scraper (must run first)
├─ social-scraper/analysis/consolidate.py (must run first)
├─ API keys (ANTHROPIC_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY)
└─ Scraped content in social-scraper/output/

generate_report
├─ analyze_content (for data-driven reports)
└─ Optional: analysis/generate_visualizations.py (for charts)
```

---

## Common Workflows

### Quick Invoice
```
generate_invoice → Returns JSON → Copy to invoicer tool
```

### Explore Tools
```
list_tools(category: "all") → See available tools
```

### Test Scraping
```
run_scraper(test_mode: true) → Scrape first influencer
```

### Full Analysis Pipeline
```
1. run_scraper (all influencers)
2. analyze_content (with preferred provider)
3. generate_report (web or research-brief)
```

### Cost-Optimized Analysis
```
1. run_scraper
2. analyze_content (batch_mode: true, provider: "claude")
3. Wait 1-24 hours for batch completion
4. generate_report
```

---

## Error Codes

- `InvalidParams` - Missing or invalid parameters
- `MethodNotFound` - Unknown tool name
- `InternalError` - Execution failure (check stderr)

---

## Performance

| Tool | Typical Duration | Notes |
|------|-----------------|-------|
| generate_invoice | <100ms | Synchronous |
| list_tools | <50ms | Synchronous |
| run_scraper | 2-30 min | Depends on batch size |
| analyze_content (real-time) | 3-7 sec/post | Rate limited |
| analyze_content (batch) | 1-24 hours | Async, 50% cheaper |
| generate_report | 5-60 sec | With visualizations |

---

## Environment Variables

Required for full functionality:

```bash
# In social-scraper/.env

# AI Providers (at least one required for analysis)
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
OPENAI_API_KEY=sk-...

# Instagram (recommended for scraping)
INSTAGRAM_UN=your_username
INSTAGRAM_PW=your_password
```

---

## Quick Setup

```bash
# 1. Install dependencies
cd /home/user/ccm/tools/shared
./setup-mcp-server.sh

# 2. Install Python dependencies
cd ../../social-scraper
pip3 install -r requirements.txt

# 3. Set up .env file
cp .env.example .env
# Edit .env with your API keys

# 4. Test the server
cd ../tools/shared
node test-mcp-server.js

# 5. Configure MCP client
# Add config to claude_desktop_config.json (see MCP-SERVER-README.md)
```

---

## Testing

```bash
# Run automated tests
node test-mcp-server.js

# Interactive testing with MCP Inspector
npx @modelcontextprotocol/inspector node mcp-server.js
```

---

## Support Files

- **Full Documentation:** `MCP-SERVER-README.md`
- **Usage Examples:** `examples/usage-examples.md`
- **Package Config:** `mcp-server-package.json`
- **Settings Example:** `mcp-settings-example.json`
- **Setup Script:** `setup-mcp-server.sh`

---

## Quick Troubleshooting

**Server won't start:**
```bash
node --version  # Must be 18+
npm install @modelcontextprotocol/sdk
```

**Scraper fails:**
```bash
cd /home/user/ccm/social-scraper
pip3 install -r requirements.txt
python3 main.py --test
```

**Analysis fails:**
```bash
# Check API keys
cat /home/user/ccm/social-scraper/.env

# Run consolidate first
python3 analysis/consolidate.py
```

**Tools not in Claude Desktop:**
1. Check config file path
2. Restart Claude Desktop
3. Verify absolute paths in config

---

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP SDK Docs](https://github.com/modelcontextprotocol/sdk)
- [CCM Project](https://github.com/centerforcooperativemedia)

---

**Version:** 1.0.0
**Last Updated:** 2026-01-09
**Maintainer:** Center for Cooperative Media
