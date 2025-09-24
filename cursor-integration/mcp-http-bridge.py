#!/usr/bin/env python3
"""
HTTP Bridge for MCP Server - Cursor Integration

This bridge allows Cursor to connect to a remote MCP server via HTTP.
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any
import aiohttp
from aiohttp import web, ClientSession
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPHTTPBridge:
    """HTTP bridge that forwards MCP requests to remote server"""
    
    def __init__(self, gpu_server_url: str):
        self.gpu_server_url = gpu_server_url.rstrip('/')
        self.session = None
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = ClientSession()
    
    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
    
    async def forward_request(self, mcp_request: Dict[str, Any]) -> Dict[str, Any]:
        """Forward MCP request to GPU server"""
        
        try:
            # Send request to GPU server MCP endpoint
            async with self.session.post(
                f"{self.gpu_server_url}/mcp",
                json=mcp_request,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": mcp_request.get("id"),
                        "error": {
                            "code": -32603,
                            "message": f"HTTP Error: {response.status}"
                        }
                    }
                    
        except asyncio.TimeoutError:
            return {
                "jsonrpc": "2.0",
                "id": mcp_request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Request timeout"
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": mcp_request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Bridge error: {str(e)}"
                }
            }
    
    async def handle_stdio(self):
        """Handle stdio-based MCP communication"""
        
        logger.info(f"🌉 MCP HTTP Bridge starting...")
        logger.info(f"🎯 Forwarding to: {self.gpu_server_url}")
        
        await self.initialize()
        
        try:
            # Read from stdin and forward to HTTP server
            async def read_requests():
                buffer = ""
                while True:
                    try:
                        line = await asyncio.get_event_loop().run_in_executor(
                            None, sys.stdin.readline
                        )
                        if not line:
                            break
                        
                        buffer += line
                        
                        # Try to parse complete JSON messages
                        while buffer:
                            try:
                                decoder = json.JSONDecoder()
                                request, idx = decoder.raw_decode(buffer)
                                
                                # Forward request and get response
                                response = await self.forward_request(request)
                                
                                # Send response to stdout
                                print(json.dumps(response), flush=True)
                                
                                # Remove processed part from buffer
                                buffer = buffer[idx:].lstrip()
                                
                            except json.JSONDecodeError:
                                # Need more data
                                break
                                
                    except Exception as e:
                        logger.error(f"Error processing request: {e}")
                        break
            
            await read_requests()
            
        finally:
            await self.cleanup()


async def main():
    """Main entry point"""
    
    # Get GPU server URL from environment
    gpu_server_url = os.getenv('GPU_SERVER_URL', 'http://localhost:8080')
    
    if len(sys.argv) > 1:
        gpu_server_url = sys.argv[1]
    
    # Create and run bridge
    bridge = MCPHTTPBridge(gpu_server_url)
    await bridge.handle_stdio()


if __name__ == "__main__":
    asyncio.run(main())
