#!/usr/bin/env python3
"""
Test script for the MCP Local LLM Server
"""

import asyncio
import json
import sys
from mcp_server import MCPLocalLLMServer


async def test_server():
    """Test the MCP server functionality"""
    
    print("🧪 Testing MCP Local LLM Server...")
    
    server = MCPLocalLLMServer()
    
    # Test list tools
    print("\n📋 Testing list_tools...")
    try:
        if server.server.tools_handler:
            tools_result = await server.server.tools_handler()
            print(f"✅ Found {len(tools_result.tools)} tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
    
    # Test list resources
    print("\n📚 Testing list_resources...")
    try:
        if server.server.resources_handler:
            resources_result = await server.server.resources_handler()
            print(f"✅ Found {len(resources_result.resources)} resources:")
            for resource in resources_result.resources:
                print(f"  - {resource.uri}: {resource.name}")
    except Exception as e:
        print(f"❌ Error testing resources: {e}")
    
    print("\n🎉 Basic server tests completed!")
    print("\nTo test with actual LLM:")
    print("1. Run: python mcp_server.py")
    print("2. Send JSON-RPC requests via stdin")
    print("3. Or integrate with Claude Desktop using the provided config")


if __name__ == "__main__":
    asyncio.run(test_server())
