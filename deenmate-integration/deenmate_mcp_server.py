#!/usr/bin/env python3
"""
DeenMate-specific MCP Server

Enhanced MCP server with Islamic tools and content generation
specifically designed for the DeenMate project.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime

# Import base MCP server
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server import MCPLocalLLMServer, LocalLLMManager
from islamic_mcp_tools import IslamicMCPTools, IslamicContentGenerator, ISLAMIC_SYSTEM_PROMPT
from deenmate_code_generator import DeenMateCodeGenerator, DEENMATE_TEMPLATES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeenMateMCPServer(MCPLocalLLMServer):
    """Enhanced MCP Server for DeenMate with Islamic tools"""
    
    def __init__(self):
        super().__init__()
        self.islamic_tools = IslamicMCPTools()
        self.content_generator = IslamicContentGenerator()
        self.code_generator = DeenMateCodeGenerator()
        self.setup_deenmate_handlers()
    
    def setup_deenmate_handlers(self):
        """Setup DeenMate-specific MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List all tools including Islamic ones"""
            # Get base tools - import here to avoid circular imports
            from mcp.types import Tool, ListToolsResult
            
            # Create base tools manually (since we're overriding)
            base_tools = [
                Tool(
                    name="chat_with_llm",
                    description="Chat with the local LLM model",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "The message to send to the LLM"},
                            "system_prompt": {"type": "string", "description": "Optional system prompt"},
                            "temperature": {"type": "number", "description": "Temperature (0-1)", "default": 0.7},
                            "max_tokens": {"type": "integer", "description": "Max tokens", "default": 512}
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
                            "code": {"type": "string", "description": "The code to analyze"},
                            "language": {"type": "string", "description": "Programming language"},
                            "analysis_type": {"type": "string", "description": "Type of analysis", "default": "review"}
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
                            "prompt": {"type": "string", "description": "Prompt for generation"},
                            "style": {"type": "string", "description": "Writing style", "default": "formal"},
                            "length": {"type": "string", "description": "Length", "default": "medium"}
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
                            "text": {"type": "string", "description": "Text to translate"},
                            "target_language": {"type": "string", "description": "Target language"},
                            "source_language": {"type": "string", "description": "Source language"}
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
                            "content": {"type": "string", "description": "Content to summarize"},
                            "summary_type": {"type": "string", "description": "Summary type", "default": "brief"},
                            "max_length": {"type": "integer", "description": "Max length", "default": 150}
                        },
                        "required": ["content"]
                    }
                )
            ]
            
            # Add Islamic tools
            islamic_tools = self.islamic_tools.get_islamic_tools()
            for tool_data in islamic_tools:
                tool = Tool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    inputSchema=tool_data["inputSchema"]
                )
                base_tools.append(tool)
            
            # Add DeenMate code generation tools
            code_tools = self.code_generator.get_deenmate_tools()
            for tool_data in code_tools:
                tool = Tool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    inputSchema=tool_data["inputSchema"]
                )
                base_tools.append(tool)
            
            return ListToolsResult(tools=base_tools)
        
        @self.server.call_tool()
        async def handle_call_tool(request):
            """Handle tool calls including Islamic tools"""
            
            tool_name = request.params.name
            arguments = request.params.arguments
            
            # Handle Islamic tools
            if tool_name == "islamic_guidance":
                return await self._handle_islamic_guidance(arguments)
            elif tool_name == "quran_explanation":
                return await self._handle_quran_explanation(arguments)
            elif tool_name == "hadith_guidance":
                return await self._handle_hadith_guidance(arguments)
            elif tool_name == "prayer_guidance":
                return await self._handle_prayer_guidance(arguments)
            elif tool_name == "zakat_calculator":
                return await self._handle_zakat_calculator(arguments)
            elif tool_name == "islamic_content_generator":
                return await self._handle_islamic_content_generator(arguments)
            elif tool_name == "halal_haram_guidance":
                return await self._handle_halal_haram_guidance(arguments)
            elif tool_name == "ramadan_fasting_guide":
                return await self._handle_ramadan_fasting_guide(arguments)
            
            # Handle DeenMate code generation tools
            elif tool_name == "generate_flutter_feature":
                return await self._handle_generate_flutter_feature(arguments)
            elif tool_name == "generate_backend_api":
                return await self._handle_generate_backend_api(arguments)
            elif tool_name == "generate_web_component":
                return await self._handle_generate_web_component(arguments)
            elif tool_name == "generate_islamic_ui_components":
                return await self._handle_generate_islamic_ui_components(arguments)
            elif tool_name == "generate_database_schema":
                return await self._handle_generate_database_schema(arguments)
            elif tool_name == "generate_test_suite":
                return await self._handle_generate_test_suite(arguments)
            elif tool_name == "generate_documentation":
                return await self._handle_generate_documentation(arguments)
            else:
                # Handle base tools directly
                if tool_name == "chat_with_llm":
                    return await self._handle_chat_with_llm(arguments)
                elif tool_name == "analyze_code":
                    return await self._handle_analyze_code(arguments)
                elif tool_name == "generate_text":
                    return await self._handle_generate_text(arguments)
                elif tool_name == "translate_text":
                    return await self._handle_translate_text(arguments)
                elif tool_name == "summarize_content":
                    return await self._handle_summarize_content(arguments)
                else:
                    from mcp.types import CallToolResult, TextContent
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {tool_name}")],
                        isError=True
                    )
        
        @self.server.list_resources()
        async def handle_list_resources():
            """List all resources including Islamic ones"""
            # Create base resources manually
            from mcp.types import Resource, ListResourcesResult
            
            base_resources = [
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
            
            # Add Islamic resources
            islamic_resources = self.islamic_tools.get_islamic_resources()
            for resource_data in islamic_resources:
                resource = Resource(
                    uri=resource_data["uri"],
                    name=resource_data["name"],
                    description=resource_data["description"],
                    mimeType=resource_data["mimeType"]
                )
                base_resources.append(resource)
            
            return ListResourcesResult(resources=base_resources)
        
        @self.server.read_resource()
        async def handle_read_resource(request):
            """Handle resource reads including Islamic resources"""
            
            uri = request.params.uri
            
            if uri == "islamic://daily/content":
                content = self.content_generator.generate_daily_content()
                from mcp.types import GetResourceResult, JSONContent
                return GetResourceResult(
                    contents=[JSONContent(type="json", json=content)]
                )
            
            elif uri == "islamic://prayer/times":
                # This would integrate with actual prayer time API
                prayer_times = {
                    "date": datetime.now().isoformat(),
                    "location": "Default Location",
                    "times": {
                        "fajr": "05:30",
                        "dhuhr": "12:15", 
                        "asr": "15:45",
                        "maghrib": "18:20",
                        "isha": "19:45"
                    },
                    "qibla_direction": "Northeast (45°)"
                }
                from mcp.types import GetResourceResult, JSONContent
                return GetResourceResult(
                    contents=[JSONContent(type="json", json=prayer_times)]
                )
            
            elif uri == "islamic://calendar/events":
                # Islamic calendar events
                events = {
                    "current_month": "Rabi' al-Awwal 1446",
                    "upcoming_events": [
                        {
                            "name": "Mawlid an-Nabi",
                            "date": "2024-09-27",
                            "description": "Birthday of Prophet Muhammad (SAW)"
                        }
                    ]
                }
                from mcp.types import GetResourceResult, JSONContent
                return GetResourceResult(
                    contents=[JSONContent(type="json", json=events)]
                )
            
            elif uri == "islamic://content/library":
                # Content library for DeenMate
                library = {
                    "categories": [
                        "Quran & Tafsir",
                        "Hadith & Sunnah", 
                        "Fiqh & Jurisprudence",
                        "Islamic History",
                        "Spiritual Development",
                        "Daily Practices"
                    ],
                    "latest_content": [
                        {
                            "title": "Understanding Prayer in Islam",
                            "category": "Daily Practices",
                            "summary": "Complete guide to Islamic prayer"
                        }
                    ]
                }
                from mcp.types import GetResourceResult, JSONContent
                return GetResourceResult(
                    contents=[JSONContent(type="json", json=library)]
                )
            
            else:
                # Handle base resources
                if uri == "llm://model/info":
                    info = {
                        "model_name": self.llm_manager.model_name,
                        "device": str(self.llm_manager.device),
                        "model_loaded": self.llm_manager.model is not None,
                        "tokenizer_loaded": self.llm_manager.tokenizer is not None
                    }
                    from mcp.types import GetResourceResult, JSONContent
                    return GetResourceResult(
                        contents=[JSONContent(type="json", json=info)]
                    )
                
                elif uri == "llm://conversations/history":
                    from mcp.types import GetResourceResult, JSONContent
                    return GetResourceResult(
                        contents=[JSONContent(type="json", json=self.conversation_history)]
                    )
                
                elif uri == "llm://system/status":
                    import torch
                    status = {
                        "timestamp": datetime.now().isoformat(),
                        "gpu_available": torch.cuda.is_available(),
                        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
                        "memory_allocated": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0,
                        "memory_reserved": torch.cuda.memory_reserved() if torch.cuda.is_available() else 0
                    }
                    from mcp.types import GetResourceResult, JSONContent
                    return GetResourceResult(
                        contents=[JSONContent(type="json", json=status)]
                    )
                
                else:
                    raise ValueError(f"Unknown resource: {uri}")
    
    # Islamic tool handlers
    async def _handle_islamic_guidance(self, arguments: Dict[str, Any]):
        """Handle Islamic guidance requests"""
        question = arguments["question"]
        context = arguments.get("context", "")
        madhab = arguments.get("madhab", "General")
        
        prompt = f"""
Islamic Question: {question}

Context: {context}
School of Thought: {madhab}

Please provide Islamic guidance based on Quran and authentic Hadith. Include:
1. Direct answer to the question
2. Relevant Quranic verses or Hadith (with references)
3. Scholarly consensus or differences if any
4. Practical application
5. Recommendation to consult local scholars for complex matters
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=800,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_quran_explanation(self, arguments: Dict[str, Any]):
        """Handle Quran explanation requests"""
        verse_ref = arguments["verse_reference"]
        verse_text = arguments.get("verse_text", "")
        explanation_type = arguments.get("explanation_type", "practical")
        
        prompt = f"""
Explain this Quranic verse: {verse_ref}

Verse Text: {verse_text}
Explanation Type: {explanation_type}

Please provide:
1. Context of revelation (if known)
2. Word-by-word meaning (if linguistic)
3. Classical tafsir interpretation
4. Practical lessons for modern Muslims
5. Related verses or Hadith
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=1000,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_zakat_calculator(self, arguments: Dict[str, Any]):
        """Handle Zakat calculation requests"""
        wealth_type = arguments["wealth_type"]
        amount = arguments["amount"]
        currency = arguments.get("currency", "USD")
        
        # Basic Zakat calculations (2.5% for most wealth types)
        if wealth_type in ["cash", "business"]:
            nisab = 595  # Approximate nisab in USD (based on silver)
            zakat_rate = 0.025
        elif wealth_type == "gold":
            nisab = 87.5  # grams of gold
            zakat_rate = 0.025
        elif wealth_type == "agriculture":
            zakat_rate = 0.10 if "irrigated" else 0.05
        else:
            zakat_rate = 0.025
        
        if amount >= nisab:
            zakat_due = amount * zakat_rate
            calculation_result = f"""
Zakat Calculation Results:

Wealth Type: {wealth_type.title()}
Amount: {amount:,.2f} {currency}
Nisab Threshold: {nisab:,.2f} {currency}
Zakat Rate: {zakat_rate*100}%

✅ Zakat is DUE
Amount Due: {zakat_due:,.2f} {currency}

Note: This is a basic calculation. For complex wealth situations, 
please consult a qualified Islamic scholar or use detailed Zakat calculators.
"""
        else:
            calculation_result = f"""
Zakat Calculation Results:

Wealth Type: {wealth_type.title()}
Amount: {amount:,.2f} {currency}
Nisab Threshold: {nisab:,.2f} {currency}

❌ No Zakat Due
Your wealth is below the nisab threshold.

Continue saving and may Allah bless your wealth!
"""
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=calculation_result)]
        )
    
    async def _handle_islamic_content_generator(self, arguments: Dict[str, Any]):
        """Handle Islamic content generation for DeenMate"""
        content_type = arguments["content_type"]
        topic = arguments.get("topic", "General Islamic guidance")
        target_audience = arguments.get("target_audience", "general")
        length = arguments.get("length", "medium")
        
        length_tokens = {"short": 200, "medium": 400, "long": 600}
        
        prompt = f"""
Generate {content_type} content for the DeenMate app:

Topic: {topic}
Target Audience: {target_audience}
Length: {length}

Create engaging, authentic Islamic content that:
1. Is appropriate for {target_audience}
2. Includes relevant Quranic verses or Hadith
3. Provides practical Islamic guidance
4. Is formatted for mobile app display
5. Encourages positive Islamic practice

Content Type: {content_type}
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=length_tokens.get(length, 400),
            temperature=0.6
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    # Base tool handlers (inherited from parent class methods)
    async def _handle_chat_with_llm(self, arguments: Dict[str, Any]):
        """Handle chat with LLM tool"""
        message = arguments["message"]
        system_prompt = arguments.get("system_prompt", ISLAMIC_SYSTEM_PROMPT)
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
            "parameters": {"temperature": temperature, "max_tokens": max_tokens}
        }
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_analyze_code(self, arguments: Dict[str, Any]):
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
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_generate_text(self, arguments: Dict[str, Any]):
        """Handle text generation tool"""
        prompt = arguments["prompt"]
        style = arguments.get("style", "formal")
        length = arguments.get("length", "medium")
        
        length_tokens = {"short": 256, "medium": 512, "long": 1024}
        
        system_prompt = f"""You are a skilled writer. Generate text in a {style} style.
        The response should be {length} in length. Be creative, engaging, and appropriate
        for the requested style and length."""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=length_tokens.get(length, 512),
            temperature=0.8
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_translate_text(self, arguments: Dict[str, Any]):
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
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_summarize_content(self, arguments: Dict[str, Any]):
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
            max_tokens=max_length * 2,
            temperature=0.5
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    # Additional Islamic tool handlers
    async def _handle_hadith_guidance(self, arguments: Dict[str, Any]):
        """Handle Hadith guidance requests"""
        topic = arguments["topic"]
        hadith_text = arguments.get("hadith_text", "")
        collection = arguments.get("collection", "Any")
        
        prompt = f"""
Topic: {topic}
Hadith Text: {hadith_text}
Preferred Collection: {collection}

Please provide guidance based on authentic Hadith literature. Include:
1. Relevant Hadith with proper attribution
2. Explanation of the teaching
3. Practical application in modern life
4. Grade/authenticity if known
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=800,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_prayer_guidance(self, arguments: Dict[str, Any]):
        """Handle prayer guidance requests"""
        prayer_question = arguments["prayer_question"]
        prayer_type = arguments.get("prayer_type", "General")
        situation = arguments.get("situation", "")
        
        prompt = f"""
Prayer Question: {prayer_question}
Prayer Type: {prayer_type}
Special Situation: {situation}

Please provide guidance on prayer (Salah) based on Islamic jurisprudence. Include:
1. Clear answer to the question
2. Relevant Quranic verses or Hadith
3. Different scholarly opinions if applicable
4. Practical steps for implementation
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=800,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_halal_haram_guidance(self, arguments: Dict[str, Any]):
        """Handle halal/haram guidance requests"""
        item_or_action = arguments["item_or_action"]
        context = arguments.get("context", "")
        evidence_level = arguments.get("evidence_level", "basic")
        
        prompt = f"""
Item/Action: {item_or_action}
Context: {context}
Evidence Level: {evidence_level}

Please provide Islamic ruling on the permissibility of this item/action. Include:
1. Clear ruling (Halal, Haram, Makruh, Mustahab, etc.)
2. Evidence from Quran and Sunnah
3. Scholarly consensus or differences
4. Practical implications and alternatives if needed
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=800,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )
    
    async def _handle_ramadan_fasting_guide(self, arguments: Dict[str, Any]):
        """Handle Ramadan fasting guidance requests"""
        fasting_question = arguments["fasting_question"]
        fasting_type = arguments.get("fasting_type", "Ramadan")
        personal_situation = arguments.get("personal_situation", "")
        
        prompt = f"""
Fasting Question: {fasting_question}
Fasting Type: {fasting_type}
Personal Situation: {personal_situation}

Please provide comprehensive guidance on fasting based on Islamic teachings. Include:
1. Answer to the specific question
2. Relevant Quranic verses and Hadith
3. Conditions and exemptions if applicable
4. Make-up requirements if needed
5. Spiritual benefits and recommendations
"""
        
        response = await self.llm_manager.generate_response(
            prompt=prompt,
            system_prompt=ISLAMIC_SYSTEM_PROMPT,
            max_tokens=1000,
            temperature=0.3
        )
        
        from mcp.types import CallToolResult, TextContent
        return CallToolResult(
            content=[TextContent(type="text", text=response)]
        )


async def main():
    """Main entry point for DeenMate MCP Server"""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("DeenMate MCP Server v1.0.0")
        return
    
    logger.info("🕌 Starting DeenMate MCP Server with Islamic AI Assistant...")
    server = DeenMateMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
