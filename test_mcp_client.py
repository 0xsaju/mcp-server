#!/usr/bin/env python3
"""
Simple MCP client to test the server
"""

import json
import subprocess
import sys

def test_mcp_server():
    """Test the MCP server with sample requests"""
    
    # Test requests
    test_requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        },
        {
            "jsonrpc": "2.0", 
            "id": 2,
            "method": "resources/list",
            "params": {}
        },
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "chat_with_llm",
                "arguments": {
                    "message": "Hello! Can you tell me about yourself?",
                    "max_tokens": 100
                }
            }
        }
    ]
    
    print("🧪 Testing MCP Server...")
    print("=" * 50)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📤 Test {i}: {request['method']}")
        print(f"Request: {json.dumps(request)}")
        
        try:
            # Start the server process
            proc = subprocess.Popen(
                ["python", "mcp_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send request and get response
            stdout, stderr = proc.communicate(
                input=json.dumps(request) + "\n",
                timeout=60
            )
            
            print(f"📥 Response: {stdout}")
            if stderr:
                print(f"⚠️  Stderr: {stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏱️  Test timed out (normal for model loading)")
            proc.kill()
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_mcp_server()
