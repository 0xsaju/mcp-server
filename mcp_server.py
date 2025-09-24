#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Server with Local LLM Integration

This server implements the MCP specification to provide tools and resources
that can be used by MCP-compatible clients (like Claude Desktop, IDEs, etc.)
while leveraging a local LLM for various operations.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

# Core MCP imports - we'll implement these
from mcp import McpServer, Tool, Resource
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    GetResourceRequest,
    GetResourceResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    ImageContent,
    JSONContent,
)

# Local LLM imports
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LocalLLMManager:
    """Manages the local LLM for the MCP server"""
    
    def __init__(self):
        self.model_name = os.getenv("MODEL_NAME", "Qwen/Qwen3-8B")
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def initialize(self):
        """Initialize the local LLM"""
        logger.info(f"🧠 Loading {self.model_name}...")
        
        # Configure quantization for efficient memory usage
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, 
            trust_remote_code=True
        )
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )
        
        logger.info(f"✅ {self.model_name} Model Loaded on {self.device}")
    
    async def generate_response(
        self, 
        prompt: str, 
        max_tokens: int = 512,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate a response using the local LLM"""
        
        # Format the conversation
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Apply chat template
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Tokenize
        inputs = self.tokenizer([formatted_prompt], return_tensors="pt").to(self.model.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True if temperature > 0 else False,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:], 
            skip_special_tokens=True
        )
        
        return response.strip()


class MCPLocalLLMServer:
    """MCP Server with Local LLM integration"""
    
    def __init__(self):
        self.llm_manager = LocalLLMManager()
        self.server = McpServer("local-llm-mcp-server")
        self.conversation_history = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup MCP request handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools"""
            tools = [
                Tool(
                    name="chat_with_llm",
                    description="Chat with the local LLM model",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "The message to send to the LLM"
                            },
                            "system_prompt": {
                                "type": "string",
                                "description": "Optional system prompt to guide the LLM's behavior"
                            },
                            "temperature": {
                                "type": "number",
                                "description": "Temperature for response generation (0-1)",
                                "default": 0.7
                            },
                            "max_tokens": {
                                "type": "integer",
                                "description": "Maximum tokens to generate",
                                "default": 512
                            }
                        },
                        "required": ["message"]
                    }
                ),
                Tool(
                    name="analyze_code",
                    description="Analyze code using the local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to analyze"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language of the code"
                            },
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of analysis (review, explain, optimize, debug)",
                                "default": "review"
                            }
                        },
                        "required": ["code"]
                    }
                ),
                Tool(
                    name="generate_text",
                    description="Generate text content using the local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt for text generation"
                            },
                            "style": {
                                "type": "string",
                                "description": "Writing style (formal, casual, technical, creative)",
                                "default": "formal"
                            },
                            "length": {
                                "type": "string",
                                "description": "Desired length (short, medium, long)",
                                "default": "medium"
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="translate_text",
                    description="Translate text using the local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to translate"
                            },
                            "target_language": {
                                "type": "string",
                                "description": "Target language for translation"
                            },
                            "source_language": {
                                "type": "string",
                                "description": "Source language (optional, auto-detect if not provided)"
                            }
                        },
                        "required": ["text", "target_language"]
                    }
                ),
                Tool(
                    name="summarize_content",
                    description="Summarize content using the local LLM",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to summarize"
                            },
                            "summary_type": {
                                "type": "string",
                                "description": "Type of summary (brief, detailed, bullet_points)",
                                "default": "brief"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum length of summary in words",
                                "default": 150
                            }
                        },
                        "required": ["content"]
                    }
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            """Handle tool calls"""
            
            try:
                if request.params.name == "chat_with_llm":
                    return await self._handle_chat_with_llm(request.params.arguments)
                
                elif request.params.name == "analyze_code":
                    return await self._handle_analyze_code(request.params.arguments)
                
                elif request.params.name == "generate_text":
                    return await self._handle_generate_text(request.params.arguments)
                
                elif request.params.name == "translate_text":
                    return await self._handle_translate_text(request.params.arguments)
                
                elif request.params.name == "summarize_content":
                    return await self._handle_summarize_content(request.params.arguments)
                
                else:
                    raise ValueError(f"Unknown tool: {request.params.name}")
                    
            except Exception as e:
                logger.error(f"Error in tool call {request.params.name}: {e}")
                return CallToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Error: {str(e)}"
                    )],
                    isError=True
                )
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """List available resources"""
            resources = [
                Resource(
                    uri="llm://model/info",
                    name="LLM Model Information",
                    description="Information about the loaded local LLM model",
                    mimeType="application/json"
                ),
                Resource(
                    uri="llm://conversations/history",
                    name="Conversation History",
                    description="History of conversations with the LLM",
                    mimeType="application/json"
                ),
                Resource(
                    uri="llm://system/status",
                    name="System Status",
                    description="Current system status and resource usage",
                    mimeType="application/json"
                )
            ]
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def handle_read_resource(request: GetResourceRequest) -> GetResourceResult:
            """Handle resource read requests"""
            
            if request.params.uri == "llm://model/info":
                info = {
                    "model_name": self.llm_manager.model_name,
                    "device": str(self.llm_manager.device),
                    "model_loaded": self.llm_manager.model is not None,
                    "tokenizer_loaded": self.llm_manager.tokenizer is not None
                }
                return GetResourceResult(
                    contents=[JSONContent(
                        type="json",
                        json=info
                    )]
                )
            
            elif request.params.uri == "llm://conversations/history":
                return GetResourceResult(
                    contents=[JSONContent(
                        type="json",
                        json=self.conversation_history
                    )]
                )
            
            elif request.params.uri == "llm://system/status":
                status = {
                    "timestamp": datetime.now().isoformat(),
                    "gpu_available": torch.cuda.is_available(),
                    "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
                    "memory_allocated": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
                    "memory_reserved": torch.cuda.memory_reserved() if torch.cuda.is_available() else 0
                }
                return GetResourceResult(
                    contents=[JSONContent(
                        type="json",
                        json=status
                    )]
                )
            
            else:
                raise ValueError(f"Unknown resource: {request.params.uri}")
    
    async def _handle_chat_with_llm(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle chat with LLM tool"""
        message = arguments["message"]
        system_prompt = arguments.get("system_prompt")
        temperature = arguments.get("temperature", 0.7)
        max_tokens = arguments.get("max_tokens", 512)
        
        response = await self.llm_manager.generate_response(
            prompt=message,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt
        )
        
        # Store conversation
        conversation_id = f"chat_{len(self.conversation_history)}"
        self.conversation_history[conversation_id] = {
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "system_prompt": system_prompt,
            "llm_response": response,
            "parameters": {
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=response
            )]
        )
    
    async def _handle_analyze_code(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle code analysis tool"""
        code = arguments["code"]
        language = arguments.get("language", "unknown")
        analysis_type = arguments.get("analysis_type", "review")
        
        system_prompt = f"""You are an expert code reviewer and software engineer. 
        Analyze the following {language} code and provide a {analysis_type}.
        Be specific, constructive, and helpful in your analysis."""
        
        prompt = f"""Please {analysis_type} this {language} code:

```{language}
{code}
```

Provide detailed feedback including:
1. Code quality and best practices
2. Potential issues or bugs
3. Performance considerations
4. Suggestions for improvement
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=1024,
            temperature=0.3
        )
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=response
            )]
        )
    
    async def _handle_generate_text(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle text generation tool"""
        prompt = arguments["prompt"]
        style = arguments.get("style", "formal")
        length = arguments.get("length", "medium")
        
        length_tokens = {
            "short": 256,
            "medium": 512,
            "long": 1024
        }
        
        system_prompt = f"""You are a skilled writer. Generate text in a {style} style.
        The response should be {length} in length. Be creative, engaging, and appropriate
        for the requested style and length."""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=length_tokens.get(length, 512),
            temperature=0.8
        )
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=response
            )]
        )
    
    async def _handle_translate_text(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle text translation tool"""
        text = arguments["text"]
        target_language = arguments["target_language"]
        source_language = arguments.get("source_language", "auto-detect")
        
        system_prompt = """You are a professional translator. Provide accurate, 
        natural translations while preserving the original meaning, tone, and context."""
        
        if source_language == "auto-detect":
            prompt = f"""Translate the following text to {target_language}:

"{text}"

Provide only the translation, maintaining the original tone and meaning."""
        else:
            prompt = f"""Translate the following {source_language} text to {target_language}:

"{text}"

Provide only the translation, maintaining the original tone and meaning."""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=512,
            temperature=0.3
        )
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=response
            )]
        )
    
    async def _handle_summarize_content(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle content summarization tool"""
        content = arguments["content"]
        summary_type = arguments.get("summary_type", "brief")
        max_length = arguments.get("max_length", 150)
        
        system_prompt = """You are an expert at creating clear, concise summaries.
        Focus on the key points and main ideas while maintaining accuracy."""
        
        format_instructions = {
            "brief": "Provide a brief, one-paragraph summary",
            "detailed": "Provide a detailed summary with multiple paragraphs covering all important points",
            "bullet_points": "Provide a summary in bullet point format"
        }
        
        prompt = f"""Summarize the following content in approximately {max_length} words.
        {format_instructions.get(summary_type, "Provide a clear summary")}:

{content}

Summary:"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=max_length * 2,  # Rough estimate for token count
            temperature=0.5
        )
        
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=response
            )]
        )
    
    async def run(self, transport_type: str = "stdio"):
        """Run the MCP server"""
        logger.info("🚀 Starting MCP Server with Local LLM...")
        
        # Initialize the LLM
        await self.llm_manager.initialize()
        
        # Run the server
        if transport_type == "stdio":
            from mcp.server.stdio import stdio_server
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(read_stream, write_stream)
        else:
            raise ValueError(f"Unsupported transport type: {transport_type}")


async def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("MCP Local LLM Server v1.0.0")
        return
    
    server = MCPLocalLLMServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
