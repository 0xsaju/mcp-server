"""
MCP Protocol Types
"""

from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@dataclass
class Resource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mimeType: str


class TextContent(BaseModel):
    """Text content type"""
    type: Literal["text"] = "text"
    text: str


class ImageContent(BaseModel):
    """Image content type"""
    type: Literal["image"] = "image"
    data: str
    mimeType: str


class JSONContent(BaseModel):
    """JSON content type"""
    type: Literal["json"] = "json"
    json: Any


# Request types
class CallToolParams(BaseModel):
    name: str
    arguments: Dict[str, Any]


class CallToolRequest(BaseModel):
    params: CallToolParams


class GetResourceParams(BaseModel):
    uri: str


class GetResourceRequest(BaseModel):
    params: GetResourceParams


class ListResourcesRequest(BaseModel):
    pass


class ListToolsRequest(BaseModel):
    pass


# Result types
class CallToolResult(BaseModel):
    content: List[Union[TextContent, ImageContent, JSONContent]]
    isError: Optional[bool] = False


class GetResourceResult(BaseModel):
    contents: List[Union[TextContent, ImageContent, JSONContent]]


class ListResourcesResult(BaseModel):
    resources: List[Resource]


class ListToolsResult(BaseModel):
    tools: List[Tool]
