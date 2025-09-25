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
from mcp_server import MCPLocalLLMServer, LocalLLMManager
from islamic_mcp_tools import IslamicMCPTools, IslamicContentGenerator, ISLAMIC_SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeenMateMCPServer(MCPLocalLLMServer):
    """Enhanced MCP Server for DeenMate with Islamic tools"""
    
    def __init__(self):
        super().__init__()
        self.islamic_tools = IslamicMCPTools()
        self.content_generator = IslamicContentGenerator()
        self.setup_deenmate_handlers()
    
    def setup_deenmate_handlers(self):
        """Setup DeenMate-specific MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List all tools including Islamic ones"""
            # Get base tools
            base_result = await super(DeenMateMCPServer, self).server.tools_handler()
            base_tools = base_result.tools
            
            # Add Islamic tools
            islamic_tools = self.islamic_tools.get_islamic_tools()
            for tool_data in islamic_tools:
                from mcp.types import Tool
                tool = Tool(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    inputSchema=tool_data["inputSchema"]
                )
                base_tools.append(tool)
            
            from mcp.types import ListToolsResult
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
            else:
                # Fall back to base tools
                return await super(DeenMateMCPServer, self).server.call_tool_handler(request)
        
        @self.server.list_resources()
        async def handle_list_resources():
            """List all resources including Islamic ones"""
            # Get base resources
            base_result = await super(DeenMateMCPServer, self).server.resources_handler()
            base_resources = base_result.resources
            
            # Add Islamic resources
            islamic_resources = self.islamic_tools.get_islamic_resources()
            for resource_data in islamic_resources:
                from mcp.types import Resource
                resource = Resource(
                    uri=resource_data["uri"],
                    name=resource_data["name"],
                    description=resource_data["description"],
                    mimeType=resource_data["mimeType"]
                )
                base_resources.append(resource)
            
            from mcp.types import ListResourcesResult
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
                # Fall back to base resources
                return await super(DeenMateMCPServer, self).server.read_resource_handler(request)
    
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
    
    # Add other Islamic tool handlers...
    async def _handle_hadith_guidance(self, arguments: Dict[str, Any]):
        """Handle Hadith guidance requests"""
        # Implementation similar to above
        pass
    
    async def _handle_prayer_guidance(self, arguments: Dict[str, Any]):
        """Handle prayer guidance requests"""
        # Implementation similar to above  
        pass
    
    async def _handle_halal_haram_guidance(self, arguments: Dict[str, Any]):
        """Handle halal/haram guidance requests"""
        # Implementation similar to above
        pass
    
    async def _handle_ramadan_fasting_guide(self, arguments: Dict[str, Any]):
        """Handle Ramadan fasting guidance requests"""
        # Implementation similar to above
        pass


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
