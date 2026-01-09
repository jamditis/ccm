#!/usr/bin/env node

/**
 * Test script for CCM MCP Server
 *
 * Verifies that the server can start and tools are properly registered.
 * Does not test actual tool execution (use MCP Inspector for that).
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const TIMEOUT = 5000;

/**
 * Test server startup and tool registration
 */
async function testServer() {
  console.log('Testing CCM MCP Server...\n');

  const serverPath = join(__dirname, 'mcp-server.js');
  const server = spawn('node', [serverPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  let stdout = '';
  let stderr = '';
  let passed = 0;
  let failed = 0;

  server.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  server.stderr.on('data', (data) => {
    stderr += data.toString();
  });

  // Test 1: Server starts without errors
  await new Promise((resolve) => setTimeout(resolve, 2000));

  if (server.exitCode === null) {
    console.log('✓ Server started successfully');
    passed++;
  } else {
    console.log('✗ Server failed to start');
    console.log('Exit code:', server.exitCode);
    failed++;
  }

  // Test 2: Check stderr for startup message
  if (stderr.includes('CCM MCP Server running')) {
    console.log('✓ Server initialization message found');
    passed++;
  } else {
    console.log('✗ Server initialization message not found');
    console.log('stderr:', stderr);
    failed++;
  }

  // Test 3: Send list tools request
  const listToolsRequest = JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/list',
    params: {}
  }) + '\n';

  server.stdin.write(listToolsRequest);

  await new Promise((resolve) => setTimeout(resolve, 1000));

  if (stdout.includes('generate_invoice') &&
      stdout.includes('list_tools') &&
      stdout.includes('run_scraper')) {
    console.log('✓ Tools registered correctly');
    passed++;
  } else {
    console.log('✗ Tools not found in response');
    console.log('stdout:', stdout);
    failed++;
  }

  // Test 4: Tool schemas are valid
  try {
    const toolSchemas = [
      'generate_invoice',
      'list_tools',
      'run_scraper',
      'analyze_content',
      'generate_report'
    ];

    let schemasValid = true;
    for (const toolName of toolSchemas) {
      if (!stdout.includes(toolName)) {
        schemasValid = false;
        console.log(`✗ Tool schema missing: ${toolName}`);
        failed++;
        break;
      }
    }

    if (schemasValid) {
      console.log('✓ All tool schemas present');
      passed++;
    }
  } catch (error) {
    console.log('✗ Tool schema validation failed');
    console.log('Error:', error.message);
    failed++;
  }

  // Cleanup
  server.kill();

  // Summary
  console.log('\n' + '='.repeat(40));
  console.log('Test Summary');
  console.log('='.repeat(40));
  console.log(`Passed: ${passed}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total:  ${passed + failed}`);
  console.log('='.repeat(40));

  if (failed > 0) {
    console.log('\nSome tests failed. Check the output above.');
    process.exit(1);
  } else {
    console.log('\nAll tests passed! Server is ready to use.');
    console.log('\nNext steps:');
    console.log('1. Configure your MCP client (see MCP-SERVER-README.md)');
    console.log('2. Test with MCP Inspector:');
    console.log('   npx @modelcontextprotocol/inspector node mcp-server.js');
    process.exit(0);
  }
}

// Run tests
testServer().catch((error) => {
  console.error('Test failed with error:', error);
  process.exit(1);
});
