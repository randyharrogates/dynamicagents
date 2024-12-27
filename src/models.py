# app/models.py

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Dict, Union, Callable


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run = self.create_run_function()

    def create_run_function(self) -> Callable:
        """
        Dynamically create a run function for the agent based on the 'run' function in its functions list.
        """
        # Look for the function named "run" in the functions list and return it
        run_function = next(
            (func for func in self.functions if func.name == "run"), None
        )

        if not run_function:
            raise ValueError(f"Run function not defined for agent: {self.name}")

        # Create a callable from the code string of the function
        def dynamic_run():
            logger.info(f"Running agent: {self.name}")
            logger.info(f"Executing run function: {run_function.name}")
            logger.info(f"Description: {run_function.description}")
            # Dynamically execute the code for the 'run' function
            exec(run_function.code)  # This executes the code in the 'run' function

        return dynamic_run


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
