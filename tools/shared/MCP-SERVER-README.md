# CCM MCP Server

A Model Context Protocol (MCP) server that exposes CCM journalism tools for programmatic access by AI assistants and automation systems.

## Overview

This MCP server provides 5 custom tools for working with CCM's journalism toolkit:

1. **generate_invoice** - Create invoices programmatically
2. **list_tools** - List all available CCM tools
3. **run_scraper** - Execute social media scraper
4. **analyze_content** - Run AI analysis on content
5. **generate_report** - Generate formatted reports

## Installation

### Prerequisites

- Node.js 18 or higher
- Python 3.9+ (for scraper and analysis tools)
- Required API keys (set in `.env` file in social-scraper directory):
  - `ANTHROPIC_API_KEY` - For Claude analysis
  - `GEMINI_API_KEY` - For Gemini analysis
  - `OPENAI_API_KEY` - For OpenAI analysis
  - `INSTAGRAM_UN` and `INSTAGRAM_PW` - For Instagram scraping

### Install Dependencies

```bash
cd /home/user/ccm/tools/shared
npm install
```

Or install globally:

```bash
npm link
```

### Install MCP SDK

```bash
npm install -g @modelcontextprotocol/sdk
```

## Configuration

### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ccm-tools": {
      "command": "node",
      "args": ["/home/user/ccm/tools/shared/mcp-server.js"],
      "env": {
        "ANTHROPIC_API_KEY": "your-key-here",
        "GEMINI_API_KEY": "your-key-here",
        "OPENAI_API_KEY": "your-key-here",
        "INSTAGRAM_UN": "your-username",
        "INSTAGRAM_PW": "your-password"
      }
    }
  }
}
```

### Other MCP Clients

For other MCP-compatible clients, use:

```bash
node /home/user/ccm/tools/shared/mcp-server.js
```

The server communicates over stdio using the MCP protocol.

## Tools Documentation

### 1. generate_invoice

Create professional invoices with automatic calculations.

**Parameters:**
- `client` (object, required):
  - `name` (string, required)
  - `email` (string, required)
  - `address` (string, optional)
- `items` (array, required): Line items with:
  - `description` (string)
  - `quantity` (number)
  - `rate` (number)
- `amount` (number, optional): Total override
- `invoice_number` (string, optional): Auto-generated if not provided
- `date` (string, optional): YYYY-MM-DD format, defaults to today
- `due_date` (string, optional): YYYY-MM-DD format
- `notes` (string, optional): Payment terms or notes

**Example:**
```json
{
  "client": {
    "name": "Local News Outlet",
    "email": "editor@localnews.com",
    "address": "123 Main St, Newark, NJ"
  },
  "items": [
    {
      "description": "Investigative article on local housing",
      "quantity": 1,
      "rate": 500
    },
    {
      "description": "Photo editing",
      "quantity": 3,
      "rate": 75
    }
  ],
  "due_date": "2026-02-09",
  "notes": "Payment due within 30 days. Net 30 terms."
}
```

### 2. list_tools

List all available CCM tools with their descriptions.

**Parameters:**
- `category` (string, optional): Filter by category
  - Options: `all`, `financial`, `content`, `analysis`, `reporting`
  - Default: `all`

**Example:**
```json
{
  "category": "analysis"
}
```

### 3. run_scraper

Execute the social media scraper to collect content from influencers.

**Parameters:**
- `platforms` (array, optional): Platforms to scrape
  - Options: `tiktok`, `instagram`, `youtube`
  - Default: All platforms
- `start_index` (number, optional): Start index for batch processing
- `end_index` (number, optional): End index for batch processing
- `test_mode` (boolean, optional): Test with first influencer only
- `max_posts` (number, optional): Max posts per account (1-100, default 50)

**Example:**
```json
{
  "platforms": ["tiktok", "youtube"],
  "test_mode": true,
  "max_posts": 20
}
```

### 4. analyze_content

Run AI-powered analysis on scraped social media content.

**Parameters:**
- `provider` (string, required): AI provider
  - Options: `claude`, `gemini`, `openai`
- `analysis_type` (string, optional): Type of analysis
  - Options: `semantic`, `sentiment`, `both`
  - Default: `both`
- `batch_size` (number, optional): Number of posts to analyze (0 = all)
- `batch_mode` (boolean, optional): Use batch API for 50% savings
- `output_dir` (string, optional): Output directory path

**Example:**
```json
{
  "provider": "claude",
  "analysis_type": "both",
  "batch_size": 100,
  "batch_mode": false,
  "output_dir": "ai_results"
}
```

**Note:** Batch mode is asynchronous and may take up to 24 hours but costs 50% less.

### 5. generate_report

Generate formatted reports from analyzed data.

**Parameters:**
- `type` (string, required): Report type
  - Options: `web`, `research-brief`, `scraping-summary`, `news-analysis`
- `title` (string, optional): Report title
- `data_source` (string, optional): Path to data directory
  - Default: `analysis/ai_results_merged/`
- `output_path` (string, optional): Output file path
- `include_visualizations` (boolean, optional): Include charts
  - Default: `true`

**Example:**
```json
{
  "type": "web",
  "title": "NJ Influencer Content Analysis",
  "include_visualizations": true
}
```

## Usage Examples

### Using with Claude Desktop

Once configured, you can ask Claude:

> "Use the generate_invoice tool to create an invoice for Acme News, $1,500 for a feature article and $300 for photos"

> "Use the list_tools tool to show me all analysis tools available"

> "Run the scraper on TikTok in test mode to collect 20 posts"

> "Analyze the scraped content using Gemini with sentiment analysis only"

> "Generate a web report with visualizations from the analysis results"

### Direct CLI Usage

```bash
# Start the MCP server
node /home/user/ccm/tools/shared/mcp-server.js

# Or if installed globally
ccm-mcp-server
```

The server runs on stdio and awaits MCP protocol messages.

## Testing

Test individual tools using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector node /home/user/ccm/tools/shared/mcp-server.js
```

This opens a web interface where you can test tool calls interactively.

## Architecture

```
mcp-server.js
├── Tool Definitions (JSON Schema)
├── Request Handlers
│   ├── ListToolsRequestSchema
│   └── CallToolRequestSchema
├── Tool Implementations
│   ├── generateInvoice()
│   ├── listTools()
│   ├── runScraper()
│   ├── analyzeContent()
│   └── generateReport()
└── Command Executor
    └── executeCommand()
```

### Integration Points

- **Invoicer**: Browser-based tool in `/tools/invoicer/`
- **Social Scraper**: Python application in `/social-scraper/`
  - Uses `main.py` for scraping
  - Uses `run_ai_analysis.py` for AI analysis
  - Outputs to `/social-scraper/output/`
- **Reports**: Generated in `/social-scraper/reports/`
- **Shared Utilities**: `/tools/shared/utils/`

## Error Handling

The server implements comprehensive error handling:

- **Invalid Parameters**: Returns `ErrorCode.InvalidParams` with details
- **Method Not Found**: Returns `ErrorCode.MethodNotFound`
- **Execution Errors**: Returns `ErrorCode.InternalError` with stack trace
- **Command Failures**: Captures stderr and exit codes

All errors follow MCP error response format.

## Security Considerations

1. **API Keys**: Store in environment variables, never commit to git
2. **Input Validation**: All parameters validated against JSON schemas
3. **Command Injection**: Uses spawn with array args (no shell interpretation)
4. **File Access**: Limited to project directory tree
5. **Authentication**: Instagram credentials required for scraping

## Troubleshooting

### Server Won't Start

```bash
# Check Node version
node --version  # Should be 18+

# Check dependencies
npm list @modelcontextprotocol/sdk

# Check for port conflicts
lsof -i :stdio  # Should be empty
```

### Tool Execution Fails

```bash
# Check Python environment
cd /home/user/ccm/social-scraper
python3 --version
pip3 install -r requirements.txt

# Check API keys
cat .env | grep API_KEY

# Test scraper directly
python3 main.py --test
```

### Permission Errors

```bash
# Make server executable
chmod +x /home/user/ccm/tools/shared/mcp-server.js

# Check directory permissions
ls -la /home/user/ccm/social-scraper
```

## Performance

- **generate_invoice**: < 100ms (synchronous)
- **list_tools**: < 50ms (synchronous)
- **run_scraper**: 2-30 minutes (depends on batch size)
- **analyze_content**:
  - Real-time: 3-7 sec/post
  - Batch mode: 1-24 hours (async)
- **generate_report**: 5-60 seconds (if including visualizations)

## Roadmap

- [ ] Add caching for repeated scraper runs
- [ ] Implement streaming for long-running operations
- [ ] Add progress callbacks for analysis
- [ ] Support custom invoice templates
- [ ] Add webhook notifications for batch completions
- [ ] Implement rate limiting per API key
- [ ] Add tool usage analytics

## Support

For issues or questions:
- Check `/social-scraper/CLAUDE.md` for scraper documentation
- Review `/tools/shared/README.md` for shared utilities
- See individual tool README files in `/tools/[tool-name]/`

## License

MIT - Center for Cooperative Media

## Related Documentation

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [CCM Tools Documentation](../README.md)
- [Social Scraper Guide](../../social-scraper/README.md)
