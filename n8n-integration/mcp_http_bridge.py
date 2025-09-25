#!/usr/bin/env python3
"""
HTTP Bridge for DeenMate MCP Server - n8n Integration

This bridge exposes the MCP server via HTTP REST API that n8n can easily consume.
Provides endpoints for all Islamic tools and code generation capabilities.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from the deenmate-integration directory
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'deenmate-integration'))

from deenmate_mcp_server import DeenMateMCPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DeenMate MCP HTTP Bridge",
    description="HTTP API bridge for DeenMate MCP server - n8n integration",
    version="1.0.0"
)

# Enable CORS for n8n integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global MCP server instance
mcp_server: Optional[DeenMateMCPServer] = None

# Pydantic models for API
class MCPToolRequest(BaseModel):
    tool_name: str = Field(..., description="Name of the MCP tool to call")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the tool")

class MCPResourceRequest(BaseModel):
    resource_uri: str = Field(..., description="URI of the resource to read")

class APIResponse(BaseModel):
    success: bool
    data: Any = None
    message: str = ""
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

# Islamic content generation models
class IslamicGuidanceRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    context: Optional[str] = None
    madhab: str = Field(default="General", pattern="^(Hanafi|Shafi|Maliki|Hanbali|General)$")

class ZakatCalculationRequest(BaseModel):
    wealth_type: str = Field(..., pattern="^(cash|gold|silver|business|agriculture)$")
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD")

class ContentGenerationRequest(BaseModel):
    content_type: str = Field(..., pattern="^(daily_reminder|educational_article|dua|dhikr|reflection|tip)$")
    topic: Optional[str] = None
    target_audience: str = Field(default="general", pattern="^(general|youth|adults|families|converts)$")
    length: str = Field(default="medium", pattern="^(short|medium|long)$")

# Code generation models
class FlutterFeatureRequest(BaseModel):
    feature_name: str = Field(..., min_length=1)
    feature_type: str = Field(default="custom")
    components: list[str] = Field(default=["widget", "screen"])
    islamic_context: bool = Field(default=True)

class BackendAPIRequest(BaseModel):
    api_name: str = Field(..., min_length=1)
    api_type: str = Field(default="custom")
    http_methods: list[str] = Field(default=["GET", "POST"])
    include_auth: bool = Field(default=True)
    include_validation: bool = Field(default=True)

class WebComponentRequest(BaseModel):
    component_name: str = Field(..., min_length=1)
    component_type: str = Field(default="custom")
    styling: str = Field(default="vanilla_css")
    interactive: bool = Field(default=True)

async def get_mcp_server() -> DeenMateMCPServer:
    """Get or initialize MCP server instance"""
    global mcp_server
    if mcp_server is None:
        logger.info("Initializing DeenMate MCP Server...")
        mcp_server = DeenMateMCPServer()
        await mcp_server.llm_manager.initialize()
        logger.info("✅ DeenMate MCP Server initialized")
    return mcp_server

@app.on_event("startup")
async def startup_event():
    """Initialize MCP server on startup"""
    await get_mcp_server()

@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint with API information"""
    return APIResponse(
        success=True,
        data={
            "name": "DeenMate MCP HTTP Bridge",
            "version": "1.0.0",
            "description": "HTTP API bridge for n8n integration",
            "endpoints": {
                "tools": "/tools",
                "resources": "/resources", 
                "islamic": "/islamic/*",
                "code": "/code/*",
                "workflows": "/workflows/*"
            }
        },
        message="DeenMate MCP HTTP Bridge is running"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    server = await get_mcp_server()
    return {
        "status": "healthy",
        "mcp_server": "initialized" if server else "not_initialized",
        "model_loaded": server.llm_manager.model is not None if server else False,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/tools", response_model=APIResponse)
async def list_tools():
    """List all available MCP tools"""
    try:
        server = await get_mcp_server()
        
        # Create a mock request for list_tools
        from mcp.types import ListToolsRequest
        
        # Call the tools handler directly
        result = await server.server.tools_handler()
        
        tools_data = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in result.tools
        ]
        
        return APIResponse(
            success=True,
            data={
                "tools": tools_data,
                "count": len(tools_data)
            },
            message=f"Found {len(tools_data)} available tools"
        )
        
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/call", response_model=APIResponse)
async def call_tool(request: MCPToolRequest):
    """Call any MCP tool"""
    try:
        server = await get_mcp_server()
        
        # Create MCP request
        from mcp.types import CallToolRequest, CallToolParams
        
        mcp_request = CallToolRequest(
            params=CallToolParams(
                name=request.tool_name,
                arguments=request.arguments
            )
        )
        
        # Call the tool
        result = await server.server.call_tool_handler(mcp_request)
        
        return APIResponse(
            success=True,
            data={
                "tool_name": request.tool_name,
                "result": result.content[0].text if result.content else "No content",
                "is_error": result.isError or False
            },
            message=f"Tool '{request.tool_name}' executed successfully"
        )
        
    except Exception as e:
        logger.error(f"Error calling tool {request.tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resources", response_model=APIResponse)
async def list_resources():
    """List all available MCP resources"""
    try:
        server = await get_mcp_server()
        
        result = await server.server.resources_handler()
        
        resources_data = [
            {
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mime_type": resource.mimeType
            }
            for resource in result.resources
        ]
        
        return APIResponse(
            success=True,
            data={
                "resources": resources_data,
                "count": len(resources_data)
            },
            message=f"Found {len(resources_data)} available resources"
        )
        
    except Exception as e:
        logger.error(f"Error listing resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resources/read", response_model=APIResponse)
async def read_resource(request: MCPResourceRequest):
    """Read an MCP resource"""
    try:
        server = await get_mcp_server()
        
        from mcp.types import GetResourceRequest, GetResourceParams
        
        mcp_request = GetResourceRequest(
            params=GetResourceParams(uri=request.resource_uri)
        )
        
        result = await server.server.read_resource_handler(mcp_request)
        
        return APIResponse(
            success=True,
            data={
                "uri": request.resource_uri,
                "content": result.contents[0].json if result.contents else None
            },
            message=f"Resource '{request.resource_uri}' read successfully"
        )
        
    except Exception as e:
        logger.error(f"Error reading resource {request.resource_uri}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Islamic-specific endpoints for easier n8n integration
@app.post("/islamic/guidance", response_model=APIResponse)
async def get_islamic_guidance(request: IslamicGuidanceRequest):
    """Get Islamic guidance - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="islamic_guidance",
        arguments={
            "question": request.question,
            "context": request.context,
            "madhab": request.madhab
        }
    )
    return await call_tool(tool_request)

@app.post("/islamic/zakat", response_model=APIResponse)
async def calculate_zakat(request: ZakatCalculationRequest):
    """Calculate Zakat - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="zakat_calculator",
        arguments={
            "wealth_type": request.wealth_type,
            "amount": request.amount,
            "currency": request.currency
        }
    )
    return await call_tool(tool_request)

@app.post("/islamic/content", response_model=APIResponse)
async def generate_islamic_content(request: ContentGenerationRequest):
    """Generate Islamic content - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="islamic_content_generator",
        arguments={
            "content_type": request.content_type,
            "topic": request.topic,
            "target_audience": request.target_audience,
            "length": request.length
        }
    )
    return await call_tool(tool_request)

@app.get("/islamic/daily", response_model=APIResponse)
async def get_daily_islamic_content():
    """Get daily Islamic content - simplified endpoint for n8n"""
    try:
        server = await get_mcp_server()
        
        from mcp.types import GetResourceRequest, GetResourceParams
        
        mcp_request = GetResourceRequest(
            params=GetResourceParams(uri="islamic://daily/content")
        )
        
        result = await server.server.read_resource_handler(mcp_request)
        
        return APIResponse(
            success=True,
            data=result.contents[0].json if result.contents else {},
            message="Daily Islamic content retrieved"
        )
        
    except Exception as e:
        logger.error(f"Error getting daily content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Code generation endpoints for n8n
@app.post("/code/flutter", response_model=APIResponse)
async def generate_flutter_code(request: FlutterFeatureRequest):
    """Generate Flutter code - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="generate_flutter_feature",
        arguments={
            "feature_name": request.feature_name,
            "feature_type": request.feature_type,
            "components": request.components,
            "islamic_context": request.islamic_context
        }
    )
    return await call_tool(tool_request)

@app.post("/code/backend", response_model=APIResponse)
async def generate_backend_code(request: BackendAPIRequest):
    """Generate backend API code - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="generate_backend_api",
        arguments={
            "api_name": request.api_name,
            "api_type": request.api_type,
            "http_methods": request.http_methods,
            "include_auth": request.include_auth,
            "include_validation": request.include_validation
        }
    )
    return await call_tool(tool_request)

@app.post("/code/web", response_model=APIResponse)
async def generate_web_code(request: WebComponentRequest):
    """Generate web component code - simplified endpoint for n8n"""
    tool_request = MCPToolRequest(
        tool_name="generate_web_component",
        arguments={
            "component_name": request.component_name,
            "component_type": request.component_type,
            "styling": request.styling,
            "interactive": request.interactive
        }
    )
    return await call_tool(tool_request)

# Workflow management endpoints
@app.get("/workflows/status", response_model=APIResponse)
async def get_workflow_status():
    """Get workflow execution status"""
    return APIResponse(
        success=True,
        data={
            "active_workflows": 0,
            "completed_today": 0,
            "failed_today": 0,
            "last_execution": None
        },
        message="Workflow status retrieved"
    )

@app.post("/workflows/trigger")
async def trigger_workflow(workflow_name: str, background_tasks: BackgroundTasks):
    """Trigger a workflow execution"""
    background_tasks.add_task(execute_workflow, workflow_name)
    
    return APIResponse(
        success=True,
        data={"workflow_name": workflow_name, "status": "triggered"},
        message=f"Workflow '{workflow_name}' triggered successfully"
    )

async def execute_workflow(workflow_name: str):
    """Execute workflow in background"""
    logger.info(f"Executing workflow: {workflow_name}")
    # Implement workflow execution logic here
    pass

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DeenMate MCP HTTP Bridge")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting DeenMate MCP HTTP Bridge on {args.host}:{args.port}")
    
    uvicorn.run(
        "mcp_http_bridge:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )
