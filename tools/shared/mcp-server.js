#!/usr/bin/env node

/**
 * CCM MCP Server
 *
 * Model Context Protocol server that exposes CCM journalism tools
 * for programmatic access by AI assistants and automation systems.
 *
 * Tools exposed:
 * - generate_invoice: Create invoices programmatically
 * - list_tools: List all available CCM tools
 * - run_scraper: Execute social media scraper
 * - analyze_content: Run AI analysis on scraped data
 * - generate_report: Create reports from templates
 *
 * @see https://modelcontextprotocol.io/
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import { readFile } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = join(__dirname, '..', '..');

/**
 * Tool definitions with JSON schemas
 */
const TOOLS = [
  {
    name: 'generate_invoice',
    description: 'Create a professional invoice programmatically with client details, line items, and automatic calculations',
    inputSchema: {
      type: 'object',
      properties: {
        client: {
          type: 'object',
          description: 'Client information',
          properties: {
            name: { type: 'string', description: 'Client name' },
            email: { type: 'string', description: 'Client email address' },
            address: { type: 'string', description: 'Client billing address' }
          },
          required: ['name', 'email']
        },
        amount: {
          type: 'number',
          description: 'Total invoice amount in USD',
          minimum: 0
        },
        items: {
          type: 'array',
          description: 'Invoice line items',
          items: {
            type: 'object',
            properties: {
              description: { type: 'string', description: 'Item description' },
              quantity: { type: 'number', description: 'Quantity', minimum: 1 },
              rate: { type: 'number', description: 'Rate per unit in USD', minimum: 0 }
            },
            required: ['description', 'quantity', 'rate']
          }
        },
        invoice_number: {
          type: 'string',
          description: 'Invoice number (auto-generated if not provided)'
        },
        date: {
          type: 'string',
          description: 'Invoice date in YYYY-MM-DD format (defaults to today)'
        },
        due_date: {
          type: 'string',
          description: 'Payment due date in YYYY-MM-DD format'
        },
        notes: {
          type: 'string',
          description: 'Additional notes or payment terms'
        }
      },
      required: ['client', 'items']
    }
  },
  {
    name: 'list_tools',
    description: 'List all available CCM journalism tools from the manifest with their descriptions and capabilities',
    inputSchema: {
      type: 'object',
      properties: {
        category: {
          type: 'string',
          description: 'Filter tools by category (e.g., "financial", "content", "analysis")',
          enum: ['all', 'financial', 'content', 'analysis', 'reporting']
        }
      }
    }
  },
  {
    name: 'run_scraper',
    description: 'Execute the social media scraper to collect content from TikTok, Instagram, and YouTube accounts',
    inputSchema: {
      type: 'object',
      properties: {
        platforms: {
          type: 'array',
          description: 'Platforms to scrape (defaults to all)',
          items: {
            type: 'string',
            enum: ['tiktok', 'instagram', 'youtube']
          }
        },
        start_index: {
          type: 'number',
          description: 'Start index for batch processing (0-based)',
          minimum: 0
        },
        end_index: {
          type: 'number',
          description: 'End index for batch processing (exclusive)',
          minimum: 0
        },
        test_mode: {
          type: 'boolean',
          description: 'Run in test mode (only scrapes first influencer)',
          default: false
        },
        max_posts: {
          type: 'number',
          description: 'Maximum posts per account (defaults to 50)',
          minimum: 1,
          maximum: 100
        }
      }
    }
  },
  {
    name: 'analyze_content',
    description: 'Run AI-powered semantic and sentiment analysis on scraped social media content',
    inputSchema: {
      type: 'object',
      properties: {
        provider: {
          type: 'string',
          description: 'AI provider to use',
          enum: ['claude', 'gemini', 'openai'],
          default: 'claude'
        },
        analysis_type: {
          type: 'string',
          description: 'Type of analysis to perform',
          enum: ['semantic', 'sentiment', 'both'],
          default: 'both'
        },
        batch_size: {
          type: 'number',
          description: 'Number of posts to analyze (0 = all)',
          minimum: 0,
          default: 0
        },
        batch_mode: {
          type: 'boolean',
          description: 'Use batch API for 50% cost savings (async processing)',
          default: false
        },
        output_dir: {
          type: 'string',
          description: 'Output directory for results (relative to social-scraper/analysis/)'
        }
      },
      required: ['provider']
    }
  },
  {
    name: 'generate_report',
    description: 'Generate a formatted report from analyzed data using predefined templates',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          description: 'Report type/template',
          enum: ['web', 'research-brief', 'scraping-summary', 'news-analysis'],
          default: 'web'
        },
        title: {
          type: 'string',
          description: 'Report title'
        },
        data_source: {
          type: 'string',
          description: 'Path to data file or directory (relative to social-scraper/)',
          default: 'analysis/ai_results_merged/'
        },
        output_path: {
          type: 'string',
          description: 'Output file path (relative to social-scraper/reports/)'
        },
        include_visualizations: {
          type: 'boolean',
          description: 'Include charts and graphs',
          default: true
        }
      },
      required: ['type']
    }
  }
];

/**
 * CCM MCP Server implementation
 */
class CCMServer {
  constructor() {
    this.server = new Server(
      {
        name: 'ccm-tools-server',
        version: '1.0.0'
      },
      {
        capabilities: {
          tools: {}
        }
      }
    );

    this.setupHandlers();
    this.setupErrorHandling();
  }

  /**
   * Set up request handlers
   */
  setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: TOOLS
    }));

    // Execute tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'generate_invoice':
            return await this.generateInvoice(args);
          case 'list_tools':
            return await this.listTools(args);
          case 'run_scraper':
            return await this.runScraper(args);
          case 'analyze_content':
            return await this.analyzeContent(args);
          case 'generate_report':
            return await this.generateReport(args);
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) {
          throw error;
        }
        throw new McpError(
          ErrorCode.InternalError,
          `Tool execution failed: ${error.message}`
        );
      }
    });
  }

  /**
   * Set up error handling
   */
  setupErrorHandling() {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  /**
   * Generate invoice
   */
  async generateInvoice(args) {
    const { client, items, amount, invoice_number, date, due_date, notes } = args;

    // Validate required fields
    if (!client?.name || !client?.email) {
      throw new McpError(
        ErrorCode.InvalidParams,
        'Client name and email are required'
      );
    }

    if (!items || items.length === 0) {
      throw new McpError(
        ErrorCode.InvalidParams,
        'At least one line item is required'
      );
    }

    // Calculate totals
    const calculatedTotal = items.reduce(
      (sum, item) => sum + (item.quantity * item.rate),
      0
    );

    // Generate invoice number if not provided
    const invoiceNum = invoice_number || `INV-${Date.now()}`;
    const invoiceDate = date || new Date().toISOString().split('T')[0];

    const invoice = {
      invoice_number: invoiceNum,
      date: invoiceDate,
      due_date: due_date || null,
      client: {
        name: client.name,
        email: client.email,
        address: client.address || null
      },
      items: items.map(item => ({
        description: item.description,
        quantity: item.quantity,
        rate: item.rate,
        amount: item.quantity * item.rate
      })),
      subtotal: calculatedTotal,
      tax: 0, // Can be extended to support tax calculations
      total: amount || calculatedTotal,
      notes: notes || null,
      generated_at: new Date().toISOString()
    };

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(invoice, null, 2)
        }
      ],
      metadata: {
        invoice_number: invoiceNum,
        total: invoice.total,
        client: client.name
      }
    };
  }

  /**
   * List available CCM tools
   */
  async listTools(args) {
    const { category = 'all' } = args;

    const toolsManifest = {
      all: [
        {
          name: 'Invoicer',
          path: 'tools/invoicer',
          category: 'financial',
          description: 'Generate professional invoices for freelance journalism work'
        },
        {
          name: 'Event Budget Calculator',
          path: 'tools/event-budget-calculator',
          category: 'financial',
          description: 'Calculate costs and revenue for journalism events'
        },
        {
          name: 'Freelancer Rate Calculator',
          path: 'tools/freelancer-rate-calculator',
          category: 'financial',
          description: 'Calculate sustainable freelance journalism rates'
        },
        {
          name: 'Grant Proposal Generator',
          path: 'tools/grant-proposal-generator',
          category: 'content',
          description: 'Generate journalism grant proposals'
        },
        {
          name: 'Sponsorship Generator',
          path: 'tools/sponsorship-generator',
          category: 'content',
          description: 'Create sponsorship packages and proposals'
        },
        {
          name: 'Media Kit Builder',
          path: 'tools/media-kit-builder',
          category: 'content',
          description: 'Build media kits for journalism organizations'
        },
        {
          name: 'Chart Maker',
          path: 'tools/chart-maker',
          category: 'content',
          description: 'Create data visualizations for journalism'
        },
        {
          name: 'LLM Advisor',
          path: 'tools/llm-advisor',
          category: 'analysis',
          description: 'AI model selection advisor for journalism use cases'
        },
        {
          name: 'Collaboration Agreement Generator',
          path: 'tools/collaboration-agreement-generator',
          category: 'content',
          description: 'Generate collaboration agreements for journalism projects'
        },
        {
          name: 'Social Media Scraper',
          path: 'social-scraper',
          category: 'analysis',
          description: 'Scrape and analyze social media content from influencers'
        }
      ]
    };

    const filtered = category === 'all'
      ? toolsManifest.all
      : toolsManifest.all.filter(tool => tool.category === category);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            category,
            count: filtered.length,
            tools: filtered
          }, null, 2)
        }
      ]
    };
  }

  /**
   * Run social media scraper
   */
  async runScraper(args) {
    const {
      platforms = ['tiktok', 'instagram', 'youtube'],
      start_index,
      end_index,
      test_mode = false,
      max_posts
    } = args;

    const scraperDir = join(PROJECT_ROOT, 'social-scraper');
    const pythonCmd = 'python3';
    const scriptPath = join(scraperDir, 'main.py');

    // Build command arguments
    const cmdArgs = [scriptPath];

    if (test_mode) {
      cmdArgs.push('--test');
    }

    if (start_index !== undefined) {
      cmdArgs.push('--start', String(start_index));
    }

    if (end_index !== undefined) {
      cmdArgs.push('--end', String(end_index));
    }

    if (platforms.length > 0 && platforms.length < 3) {
      cmdArgs.push('--platforms', ...platforms);
    }

    // Set environment variables if max_posts is specified
    const env = { ...process.env };
    if (max_posts) {
      env.MAX_POSTS_PER_ACCOUNT = String(max_posts);
    }

    return await this.executeCommand(pythonCmd, cmdArgs, {
      cwd: scraperDir,
      env
    });
  }

  /**
   * Run AI content analysis
   */
  async analyzeContent(args) {
    const {
      provider,
      analysis_type = 'both',
      batch_size = 0,
      batch_mode = false,
      output_dir
    } = args;

    const scraperDir = join(PROJECT_ROOT, 'social-scraper');
    const pythonCmd = 'python3';
    const scriptPath = join(scraperDir, 'run_ai_analysis.py');

    // Build command arguments
    const cmdArgs = [
      scriptPath,
      '--provider', provider,
      '--limit', String(batch_size)
    ];

    if (output_dir) {
      cmdArgs.push('--output', output_dir);
    }

    if (analysis_type === 'semantic') {
      cmdArgs.push('--semantic-only');
    } else if (analysis_type === 'sentiment') {
      cmdArgs.push('--sentiment-only');
    }

    if (batch_mode) {
      cmdArgs.push('--batch-mode');
    }

    return await this.executeCommand(pythonCmd, cmdArgs, {
      cwd: scraperDir
    });
  }

  /**
   * Generate report
   */
  async generateReport(args) {
    const {
      type,
      title,
      data_source = 'analysis/ai_results_merged/',
      output_path,
      include_visualizations = true
    } = args;

    const scraperDir = join(PROJECT_ROOT, 'social-scraper');

    // Different report types use different generation methods
    let result;

    switch (type) {
      case 'web':
      case 'research-brief':
        // These are HTML templates that already exist
        const reportPath = join(scraperDir, 'reports', 'njinfluencers-deploy',
          type === 'web' ? 'index.html' : 'research-brief.html');

        try {
          const content = await readFile(reportPath, 'utf-8');
          result = {
            type,
            path: reportPath,
            message: 'Report template loaded. Deploy the reports/njinfluencers-deploy/ directory.',
            preview_length: content.length
          };
        } catch (error) {
          throw new McpError(
            ErrorCode.InternalError,
            `Failed to read report template: ${error.message}`
          );
        }
        break;

      case 'news-analysis':
      case 'scraping-summary':
        // Generate custom reports from data
        if (include_visualizations) {
          // First generate visualizations
          const vizCmd = 'python3';
          const vizScript = join(scraperDir, 'analysis', 'generate_visualizations.py');
          await this.executeCommand(vizCmd, [vizScript], { cwd: scraperDir });
        }

        // Read and summarize data
        const dataPath = join(scraperDir, data_source);
        result = {
          type,
          data_source: dataPath,
          message: 'Report data prepared. Use analysis results from ' + data_source,
          title: title || `${type} Report`,
          generated_at: new Date().toISOString()
        };
        break;

      default:
        throw new McpError(
          ErrorCode.InvalidParams,
          `Unknown report type: ${type}`
        );
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  }

  /**
   * Execute a command and return results
   */
  async executeCommand(command, args, options = {}) {
    return new Promise((resolve, reject) => {
      const proc = spawn(command, args, {
        ...options,
        stdio: ['ignore', 'pipe', 'pipe']
      });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      proc.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      proc.on('close', (code) => {
        const result = {
          command: `${command} ${args.join(' ')}`,
          exit_code: code,
          stdout: stdout.trim(),
          stderr: stderr.trim(),
          success: code === 0
        };

        if (code === 0) {
          resolve({
            content: [
              {
                type: 'text',
                text: JSON.stringify(result, null, 2)
              }
            ]
          });
        } else {
          reject(new McpError(
            ErrorCode.InternalError,
            `Command failed with exit code ${code}: ${stderr}`
          ));
        }
      });

      proc.on('error', (error) => {
        reject(new McpError(
          ErrorCode.InternalError,
          `Failed to execute command: ${error.message}`
        ));
      });
    });
  }

  /**
   * Start the server
   */
  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('CCM MCP Server running on stdio');
  }
}

/**
 * Start the server
 */
const server = new CCMServer();
server.start().catch((error) => {
  console.error('Failed to start server:', error);
  process.exit(1);
});
