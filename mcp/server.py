"""
Simplified MCP Server implementation
"""

import asyncio
import json
import sys
from typing import Any, Callable, Dict, Optional
from .types import (
    CallToolRequest, CallToolResult,
    GetResourceRequest, GetResourceResult,
    ListResourcesRequest, ListResourcesResult,
    ListToolsRequest, ListToolsResult
)


class McpServer:
    """Simplified MCP Server implementation"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools_handler = None
        self.call_tool_handler = None
        self.resources_handler = None
        self.read_resource_handler = None
    
    def list_tools(self):
        """Decorator for list tools handler"""
        def decorator(func: Callable):
            self.tools_handler = func
            return func
        return decorator
    
    def call_tool(self):
        """Decorator for call tool handler"""
        def decorator(func: Callable):
            self.call_tool_handler = func
            return func
        return decorator
    
    def list_resources(self):
        """Decorator for list resources handler"""
        def decorator(func: Callable):
            self.resources_handler = func
            return func
        return decorator
    
    def read_resource(self):
        """Decorator for read resource handler"""
        def decorator(func: Callable):
            self.read_resource_handler = func
            return func
        return decorator
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request"""
        
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "tools/list":
                if self.tools_handler:
                    result = await self.tools_handler()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result.dict()
                    }
            
            elif method == "tools/call":
                if self.call_tool_handler:
                    call_request = CallToolRequest(params=params)
                    result = await self.call_tool_handler(call_request)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result.dict()
                    }
            
            elif method == "resources/list":
                if self.resources_handler:
                    result = await self.resources_handler()
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result.dict()
                    }
            
            elif method == "resources/read":
                if self.read_resource_handler:
                    read_request = GetResourceRequest(params=params)
                    result = await self.read_resource_handler(read_request)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result.dict()
                    }
            
            # Method not found
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def run(self, read_stream, write_stream):
        """Run the MCP server with given streams"""
        
        async def read_messages():
            """Read messages from input stream"""
            buffer = ""
            while True:
                try:
                    # Read from stdin
                    line = await asyncio.get_event_loop().run_in_executor(
                        None, sys.stdin.readline
                    )
                    if not line:
                        break
                    
                    buffer += line
                    
                    # Try to parse complete JSON messages
                    while buffer:
                        try:
                            # Find the end of a JSON object
                            decoder = json.JSONDecoder()
                            obj, idx = decoder.raw_decode(buffer)
                            
                            # Process the message
                            response = await self.handle_request(obj)
                            
                            # Write response
                            response_json = json.dumps(response)
                            print(response_json, flush=True)
                            
                            # Remove processed part from buffer
                            buffer = buffer[idx:].lstrip()
                            
                        except json.JSONDecodeError:
                            # Need more data
                            break
                            
                except Exception as e:
                    print(f"Error reading message: {e}", file=sys.stderr)
                    break
        
        await read_messages()


# Simple stdio server context manager
def stdio_server():
    """Create a stdio server context manager"""
    return _StdioServer()


class _StdioServer:
    """Context manager for stdio server"""
    
    async def __aenter__(self):
        return (sys.stdin, sys.stdout)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
