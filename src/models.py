# app/models.py

from pydantic import BaseModel
from typing import List, Optional, Any, Dict, Union


class AgentFunction(BaseModel):
    name: str
    description: str
    code: str

class AgentTool(BaseModel):
    name: str
    description: str
    code: str

class AgentMemory(BaseModel):
    type: str
    description: str
    code: str


class Agent(BaseModel):
    name: str
    description: str
    functions: List[AgentFunction]
    tools: List[AgentTool]
    memory: List[AgentMemory]


class CreateAgentRequest(BaseModel):
    agents: List[Agent]


# ==== Seconed endpoint ====


class GraphInitialState(BaseModel):
    # Allow any key-value pairs dynamically
    data: Dict[str, Any]

    class Config:
        extra = "allow"  # This ensures extra keys are allowed in the model


class WorkflowGraph(BaseModel):
    graph_logic: Dict[str, Any]


class CreateWorkflowRequest(BaseModel):
    agent_data: List[Agent]
    workflow_graph: WorkflowGraph
    state_info: GraphInitialState
