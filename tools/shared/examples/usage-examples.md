# CCM MCP Server Usage Examples

This document provides practical examples of using the CCM MCP Server tools.

## Setup

First, ensure the server is configured in your MCP client (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "ccm-tools": {
      "command": "node",
      "args": ["/home/user/ccm/tools/shared/mcp-server.js"]
    }
  }
}
```

## Example Workflows

### 1. Invoice Generation Workflow

#### Simple Invoice
```
Generate an invoice for "Local Tribune" (editor@localtribune.com) for:
- 1 feature article at $750
- 2 photos at $150 each
Due in 30 days
```

This will use the `generate_invoice` tool with:
```json
{
  "client": {
    "name": "Local Tribune",
    "email": "editor@localtribune.com"
  },
  "items": [
    {
      "description": "Feature article - Community Impact Story",
      "quantity": 1,
      "rate": 750
    },
    {
      "description": "Photo editing and licensing",
      "quantity": 2,
      "rate": 150
    }
  ],
  "due_date": "2026-02-09",
  "notes": "Payment terms: Net 30"
}
```

#### Invoice with Custom Details
```
Create invoice #2026-001 dated today for:
Client: Jersey City Journal (accounts@jcjournal.com, 456 Grove St, Jersey City, NJ 07302)
Items:
- Investigative reporting (40 hours @ $85/hr)
- Travel expenses (1 @ $120)
Invoice notes: "Includes interviews, research, and fact-checking. Please reference story ID #JC-789"
```

### 2. Content Research Workflow

#### Step 1: Discover Available Tools
```
Show me all analysis tools available in CCM
```

Uses `list_tools`:
```json
{
  "category": "analysis"
}
```

#### Step 2: Scrape Social Media Content
```
Run a test scrape of TikTok content (first influencer only, max 20 posts)
```

Uses `run_scraper`:
```json
{
  "platforms": ["tiktok"],
  "test_mode": true,
  "max_posts": 20
}
```

#### Step 3: Analyze Content
```
Analyze the scraped content using Gemini for sentiment analysis on the first 100 posts
```

Uses `analyze_content`:
```json
{
  "provider": "gemini",
  "analysis_type": "sentiment",
  "batch_size": 100
}
```

#### Step 4: Generate Report
```
Create a web report with visualizations from the analysis results
```

Uses `generate_report`:
```json
{
  "type": "web",
  "include_visualizations": true
}
```

### 3. Full Research Pipeline

```
I need to research NJ influencer content on Instagram and YouTube:
1. First, list all available tools
2. Scrape the first 5 influencers from Instagram and YouTube (30 posts each)
3. Run semantic analysis using Claude on all collected posts
4. Generate a research brief report
```

This will execute:
1. `list_tools` with `category: "all"`
2. `run_scraper` with:
   ```json
   {
     "platforms": ["instagram", "youtube"],
     "start_index": 0,
     "end_index": 5,
     "max_posts": 30
   }
   ```
3. `analyze_content` with:
   ```json
   {
     "provider": "claude",
     "analysis_type": "semantic",
     "batch_size": 0
   }
   ```
4. `generate_report` with:
   ```json
   {
     "type": "research-brief"
   }
   ```

### 4. Batch Analysis Workflow (Cost-Optimized)

```
Run a cost-optimized analysis of all scraped content:
1. Scrape all influencers (test mode off, all platforms)
2. Use Claude's batch API for both semantic and sentiment analysis
3. Generate a comprehensive report with visualizations
```

Executes:
1. `run_scraper`:
   ```json
   {
     "platforms": ["tiktok", "instagram", "youtube"],
     "test_mode": false
   }
   ```

2. `analyze_content` (50% cheaper with batch mode):
   ```json
   {
     "provider": "claude",
     "analysis_type": "both",
     "batch_size": 0,
     "batch_mode": true
   }
   ```

3. `generate_report`:
   ```json
   {
     "type": "web",
     "title": "Comprehensive NJ Influencer Analysis 2026",
     "include_visualizations": true
   }
   ```

**Note:** Batch mode takes 1-24 hours but saves 50% on API costs.

### 5. Financial Tools Workflow

```
Show me all financial tools available, then create an invoice for my recent work.
```

Uses:
1. `list_tools`:
   ```json
   {
     "category": "financial"
   }
   ```

2. `generate_invoice` (with your details)

### 6. Multi-Provider Analysis Comparison

```
Compare analysis results from different AI providers:
1. Analyze 200 posts with Claude
2. Analyze the same 200 posts with Gemini
3. Analyze the same 200 posts with OpenAI
Then generate a comparison report
```

Executes three `analyze_content` calls with different providers:

**Claude:**
```json
{
  "provider": "claude",
  "batch_size": 200,
  "output_dir": "ai_results_claude"
}
```

**Gemini:**
```json
{
  "provider": "gemini",
  "batch_size": 200,
  "output_dir": "ai_results_gemini"
}
```

**OpenAI:**
```json
{
  "provider": "openai",
  "batch_size": 200,
  "output_dir": "ai_results_openai"
}
```

Finally: `generate_report` to compare results

### 7. News-Focused Analysis

```
Scrape content and filter for news/informational posts only:
1. Scrape TikTok and YouTube (all influencers)
2. Run semantic analysis to identify content types
3. Generate a news-analysis report focusing on journalism content
```

Uses:
1. `run_scraper` for TikTok/YouTube
2. `analyze_content` with semantic analysis
3. `generate_report`:
   ```json
   {
     "type": "news-analysis",
     "title": "NJ Influencer News Content Analysis",
     "data_source": "analysis/ai_results_merged/"
   }
   ```

## Prompt Templates

### Invoice Generation
```
Create an invoice for [CLIENT_NAME] ([EMAIL]) for:
- [DESCRIPTION] ([QUANTITY] × $[RATE])
- [DESCRIPTION] ([QUANTITY] × $[RATE])
Due: [DATE]
Notes: [PAYMENT_TERMS]
```

### Content Scraping
```
Scrape [PLATFORMS] content from [TEST_MODE ? "first influencer" : "all influencers"]
Collect up to [MAX_POSTS] posts per account
[START_INDEX ? "Start from influencer #" + START_INDEX : ""]
[END_INDEX ? "End at influencer #" + END_INDEX : ""]
```

### Content Analysis
```
Analyze scraped content using [PROVIDER]
Perform [ANALYSIS_TYPE] analysis
[BATCH_SIZE > 0 ? "Analyze first " + BATCH_SIZE + " posts" : "Analyze all posts"]
[BATCH_MODE ? "Use batch mode for cost savings (50% off)" : "Use real-time analysis"]
Save results to [OUTPUT_DIR]
```

### Report Generation
```
Generate a [TYPE] report
[TITLE ? "Title: " + TITLE : ""]
[DATA_SOURCE ? "Using data from: " + DATA_SOURCE : ""]
[INCLUDE_VISUALIZATIONS ? "Include charts and visualizations" : ""]
```

## Error Handling Examples

### Missing API Keys
```
Run analysis using Claude
```

If `ANTHROPIC_API_KEY` is not set, you'll get:
```
Error: ANTHROPIC_API_KEY not found in environment variables
```

**Solution:** Set API keys in social-scraper/.env

### Invalid Parameters
```
Create an invoice with no line items
```

Returns:
```
Error: At least one line item is required
```

### Command Failures
```
Scrape with invalid platform name
```

Returns:
```
Error: Invalid platform: "facebook". Must be one of: tiktok, instagram, youtube
```

## Best Practices

1. **Start with test mode** when scraping to verify setup
2. **Use batch mode** for large analysis jobs to save 50% on costs
3. **Check tool availability** with `list_tools` before complex workflows
4. **Set realistic batch sizes** to avoid rate limits
5. **Use descriptive invoice notes** for clear payment terms
6. **Generate reports after analysis** to visualize results

## Cost Estimates

### Scraping (No API costs)
- Time: 2-5 minutes per influencer per platform
- Storage: ~100MB per influencer

### Analysis (Real-time)
- **Claude Sonnet:** ~$10-15 per 1000 posts
- **Gemini 3 Flash:** ~$1-2 per 1000 posts
- **OpenAI GPT-5:** ~$5-8 per 1000 posts

### Analysis (Batch mode - 50% off)
- **Claude Haiku:** ~$1-2 per 1000 posts
- **Gemini:** ~$0.50-1 per 1000 posts
- **OpenAI:** ~$2.50-4 per 1000 posts

## Troubleshooting

### Tools not appearing in Claude Desktop
1. Check configuration file location
2. Restart Claude Desktop after config changes
3. Verify server path is absolute

### Scraper fails
1. Check Python dependencies: `pip3 install -r requirements.txt`
2. Verify Instagram credentials in .env
3. Test directly: `python3 main.py --test`

### Analysis fails
1. Verify API keys in social-scraper/.env
2. Check that consolidate.py has been run first
3. Ensure output directory exists

### Report generation fails
1. Run `generate_visualizations.py` first if needed
2. Check data_source path exists
3. Verify write permissions in reports/ directory

## Next Steps

- Read [MCP-SERVER-README.md](../MCP-SERVER-README.md) for detailed documentation
- Run `test-mcp-server.js` to verify installation
- Use MCP Inspector for interactive testing:
  ```bash
  npx @modelcontextprotocol/inspector node mcp-server.js
  ```
- Check `/social-scraper/CLAUDE.md` for scraper details
- See `/tools/invoicer/README.md` for invoice tool details
