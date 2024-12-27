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


class WorkflowInput(BaseModel):
    start_time: Optional[str] = "No start time yet"
    end_time: Optional[str] = "No end time yet"
    indoor_outdoor: Optional[str] = "No indoor/outdoor preference yet"
    country: Optional[str] = "No country preference yet"
    budget: Optional[str] = "No budget yet"
    food_preference: Optional[str] = "No food preference yet"
    activity_preference: Optional[str] = "No activity preference yet"
    other_requirements: Optional[str] = "No other requirements yet"


class WorkflowGraph(BaseModel):
    graph_logic: Dict[str, Any]


class AgentData(BaseModel):
    name: str
    description: str
    functions: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    memory: List[Dict[str, Any]]


class CreateWorkflowRequest(BaseModel):
    agent_data: List[AgentData]
    workflow_graph: WorkflowGraph
    state_info: WorkflowInput
