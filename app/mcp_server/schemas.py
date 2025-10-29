from pydantic import BaseModel, Field
from typing import Any, Literal


class MCPToolParameter(BaseModel):
    type: str
    description: str
    required: bool = False


class MCPTool(BaseModel):
    name: str
    description: str
    parameters: dict[str, MCPToolParameter] = Field(default_factory=dict)


class MCPResource(BaseModel):
    name: str
    type: str
    description: str | None = None


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict[str, object]


class ToolCallResponse(BaseModel):
    result: object
    is_error: bool = False
    error_message: str | None = None