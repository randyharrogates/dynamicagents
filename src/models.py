# app/models.py

from pydantic import BaseModel
from typing import List, Optional


class AgentFunction(BaseModel):
    name: str
    description: str
    logic: str


class AgentTool(BaseModel):
    name: str
    description: str
    tool_logic: str


class AgentMemory(BaseModel):
    memory_type: str
    memory_logic: str


class CreateAgentRequest(BaseModel):
    name: str
    description: str
    functions: List[AgentFunction]
    tools: List[AgentTool]
    memory: List[AgentMemory]
