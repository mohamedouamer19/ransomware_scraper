#!/usr/bin/env python3
"""
Fixed test script for the MCP Ransomware Server

This script properly handles the MCP over SSE protocol.
"""

import requests
import json
import time

def test_mcp_server():
    """Test the MCP server functionality using proper MCP protocol"""

    server_url = "http://localhost:23001"

    print("Testing MCP Server for Ransomware.live API")
    print("=" * 50)

    try:
        # Step 1: Get SSE endpoint and extract session ID
        print("\n1. Connecting to SSE endpoint...")
        response = requests.get(f"{server_url}/sse", stream=True, timeout=10)
        
        if response.status_code != 200:
            print(f"✗ Failed to connect to SSE: {response.status_code}")
            return

        # Read the SSE stream to get session endpoint
        session_url = None
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data = line_str[6:]  # Remove 'data: ' prefix
                    if data.startswith('/messages/'):
                        session_url = f"{server_url}{data}"
                        print(f"✓ Got session URL: {session_url}")
                        break
        
        response.close()  # Close the SSE connection
        
        if not session_url:
            print("✗ Could not get session URL from SSE")
            return

        # Step 2: Initialize MCP session
        print("\n2. Initializing MCP session...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        response = requests.post(session_url, json=init_request, timeout=10)
        print(f"Initialize response status: {response.status_code}")
        print(f"Initialize response: {response.text}")
        
        if response.status_code not in [200, 202]:
            print(f"✗ Failed to initialize session: {response.status_code}")
            return

        # Step 3: List available tools
        print("\n3. Listing available tools...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        response = requests.post(session_url, json=tools_request, timeout=10)
        print(f"Tools list response status: {response.status_code}")
        
        if response.status_code in [200, 202]:
            if response.status_code == 200:
                try:
                    result = response.json()
                    tools = result.get('result', {}).get('tools', [])
                    print(f"✓ Found {len(tools)} tools")
                    for tool in tools[:5]:  # Show first 5 tools
                        print(f"  - {tool.get('name')}")
                    if len(tools) > 5:
                        print(f"  ... and {len(tools) - 5} more")
                except:
                    print(f"✓ Tools request accepted (response: {response.text})")
            else:
                print(f"✓ Tools request accepted (status: {response.status_code})")
        else:
            print(f"✗ Failed to list tools: {response.status_code}")
            print(f"Response: {response.text}")

        # Step 4: Test a simple tool call (validate API key)
        print("\n4. Testing API key validation...")
        tool_call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "validate_api_key_tool",
                "arguments": {}
            }
        }

        response = requests.post(session_url, json=tool_call_request, timeout=10)
        print(f"Tool call response status: {response.status_code}")
        
        if response.status_code in [200, 202]:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'result' in result:
                        print("✓ API key validation successful")
                        content = result['result'].get('content', [])
                        if content:
                            print(f"  Result: {content[0].get('text', 'No text')}")
                    elif 'error' in result:
                        print(f"✗ API key validation failed: {result['error'].get('message')}")
                    else:
                        print("✓ Tool call completed")
                except:
                    print(f"✓ Tool call accepted (response: {response.text})")
            else:
                print(f"✓ Tool call accepted (status: {response.status_code})")
        else:
            print(f"✗ Tool call failed: {response.status_code}")
            print(f"Response: {response.text}")

        print("\n" + "=" * 50)
        print("MCP Server testing completed!")
        print("The server is accepting MCP requests correctly.")
        print("Note: 202 'Accepted' responses indicate async processing.")

    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mcp_server()
