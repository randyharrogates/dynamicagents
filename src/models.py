# app/models.py

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Dict, Union, Callable


class AgentFunction(BaseModel):
    name: str
    description: str

class AgentTool(BaseModel):
    name: str
    description: str

class AgentMemory(BaseModel):
    type: str
    description: str


class Agent(BaseModel):
    name: str
    description: str
    functions: List[AgentFunction]
    tools: List[AgentTool]
    memory: List[AgentMemory]
    model_name = str


class CreateAgentRequest(BaseModel):
    agents: List[Agent]


# ==== Seconed endpoint ====


class GraphState(BaseModel):
    # Allow any key-value pairs dynamically, but ensure 'required_key' is present
    data: Dict[str, Any] = Field(
        ...,
        description=(
            "A dict where the keys are the state names and the values "
            "are the state values."
            "Final output is the final output of the workflow and is a compulsory key."
        ),
    )

    @field_validator("data")
    def check_required_key(cls, v):
        # Check if the required key is in the dictionary
        if "final_output" not in v:
            raise ValueError(
                "The key 'final_output' must be present in the data dictionary."
            )
        return v

    class Config:
        extra = "allow"  # This ensures extra keys are allowed in the model


class WorkflowGraph(BaseModel):
    graph_logic: Dict[str, List[str]] = Field(
        ...,
        description="A dictionary that maps each node to its next nodes. E.g., { 'start': ['node1', 'node2'] }",
    )
    conditional_edges: Dict[int, Dict[str, List[Any]]] = Field(
        ...,
        description=(
            "A dictionary that maps a condition index to "
            "its corresponding condition information. "
            "The 'from_node' is the node that is evaluated, "
            "'condition_function' is the function/callable used to evaluate "
            "the condition, and 'to_nodes' are the nodes that the "
            "workflow can transition to based on the condition."
        ),
    )


class CreateWorkflowRequest(BaseModel):
    agent_data: List[Agent]
    workflow_graph: WorkflowGraph
    state_info: GraphState
