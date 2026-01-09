#!/bin/bash

# CCM MCP Server Setup Script
# Installs dependencies and configures the MCP server

set -e

echo "=========================================="
echo "CCM MCP Server Setup"
echo "=========================================="
echo ""

# Check Node.js version
echo "Checking Node.js version..."
NODE_VERSION=$(node --version)
echo "Node.js version: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v(1[8-9]|[2-9][0-9]) ]]; then
    echo "Error: Node.js 18 or higher required"
    exit 1
fi

# Navigate to the shared tools directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install dependencies
echo ""
echo "Installing MCP SDK dependencies..."
npm install --save @modelcontextprotocol/sdk

# Make the server executable
echo ""
echo "Making server executable..."
chmod +x mcp-server.js

# Check if Python is available for scraper integration
echo ""
echo "Checking Python installation for scraper..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "Python version: $PYTHON_VERSION"
else
    echo "Warning: Python3 not found. Scraper tools will not work."
fi

# Check if social-scraper requirements are installed
SCRAPER_DIR="$SCRIPT_DIR/../../social-scraper"
if [ -d "$SCRAPER_DIR" ]; then
    echo ""
    echo "Checking social-scraper setup..."
    if [ -f "$SCRAPER_DIR/requirements.txt" ]; then
        echo "Requirements file found. Install with:"
        echo "  cd $SCRAPER_DIR"
        echo "  pip3 install -r requirements.txt"
    fi

    if [ ! -f "$SCRAPER_DIR/.env" ]; then
        echo ""
        echo "Warning: No .env file found in social-scraper/"
        echo "Copy .env.example to .env and add your API keys:"
        echo "  cp $SCRAPER_DIR/.env.example $SCRAPER_DIR/.env"
    fi
fi

# Test the server
echo ""
echo "Testing MCP server startup..."
timeout 3 node mcp-server.js &> /dev/null || true
echo "Server test complete"

# Print configuration instructions
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your MCP client (e.g., Claude Desktop)"
echo "   Add this to your claude_desktop_config.json:"
echo ""
echo "   {"
echo "     \"mcpServers\": {"
echo "       \"ccm-tools\": {"
echo "         \"command\": \"node\","
echo "         \"args\": [\"$SCRIPT_DIR/mcp-server.js\"],"
echo "         \"env\": {"
echo "           \"ANTHROPIC_API_KEY\": \"your-key\","
echo "           \"GEMINI_API_KEY\": \"your-key\","
echo "           \"OPENAI_API_KEY\": \"your-key\""
echo "         }"
echo "       }"
echo "     }"
echo "   }"
echo ""
echo "2. Install social-scraper dependencies:"
echo "   cd $SCRAPER_DIR"
echo "   pip3 install -r requirements.txt"
echo ""
echo "3. Set up API keys in social-scraper/.env"
echo ""
echo "4. Test the server:"
echo "   node $SCRIPT_DIR/mcp-server.js"
echo ""
echo "5. Use MCP Inspector for interactive testing:"
echo "   npx @modelcontextprotocol/inspector node $SCRIPT_DIR/mcp-server.js"
echo ""
echo "See MCP-SERVER-README.md for full documentation"
echo ""
