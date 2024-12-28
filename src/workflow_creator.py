from collections import defaultdict
from typing import Dict, Any, Callable
from models import CreateWorkflowRequest, Agent, GraphState
from langgraph.graph import StateGraph, END


class WorkflowBuilder:
    def __init__(self, stategraph: StateGraph):
        self.state_graph = stategraph

    def add_node(self, node_name: str, node_function: Callable):
        """Add a node (agent) with its function to the workflow."""
        self.state_graph.add_node(node_name, node_function)

    def set_entry_point(self, entry_point: str):
        """Set the starting point of the workflow."""
        self.state_graph.set_entry_point(entry_point)

    def set_end_point(self, end_point: str):
        """Set the end point of the workflow."""
        self.state_graph.add_edge(end_point, END)

    def add_edge(self, from_node: str, to_node: str):
        """Create an edge between two nodes in the workflow."""
        self.state_graph.add_edge(from_node, to_node)

    def add_conditional_edges(
        self, from_node: str, condition_function: Callable, to_nodes: set
    ):
        """Create conditional edges based on a condition."""
        self.state_graph.add_conditional_edges(from_node, condition_function, to_nodes)


def create_dynamic_workflow(create_request: CreateWorkflowRequest):
    """
    Create a dynamic workflow based on the provided request.

    This function takes a CreateWorkflowRequest and constructs a dynamic workflow
    by instantiating agents based on the agent data and setting up the workflow
    graph based on the provided logic.

    Parameters:
        create_request: CreateWorkflowRequest - A Pydantic model containing the
            workflow graph and agent data.

    Returns:
        A tuple containing the state graph and the WorkflowBuilder object.
    """
    state_graph = _create_dynamic_graph_state(create_request.state_info)
    builder = WorkflowBuilder(state_graph)

    # Step 1: Instantiate dynamic agents based on the agent data
    for agent in create_request.agent_data:
        # Dynamically create the agent using the provided functions and logic
        dynamic_agent = Agent(
            name=agent.name,
            description=agent.description,
            functions=agent.functions,
            tools=agent.tools,
            memory=agent.memory,
        )
        builder.add_node(
            agent.name, dynamic_agent.run_function
        )  # Add agent's run method to the workflow

    # Step 2: Set entry point and add edges based on workflow graph logic
    workflow_logic = create_request.workflow_graph.graph_logic
    conditional_edges_logic = create_request.workflow_graph.conditional_edges
    for node, next_nodes in workflow_logic.items():
        if node == "ENTRY_POINT":
            builder.set_entry_point(node)
        elif node == "END_POINT":
            builder.set_end_point(node)
        else:
            for next_node in next_nodes:
                builder.add_edge(node, next_node)
    for num, edge in conditional_edges_logic.items():
        logger.info(f"Adding conditional edge: {num}")
        builder.add_conditional_edges(
            edge.from_node, edge.condition_function, edge.to_nodes
        )

    return state_graph, builder


def _create_dynamic_graph_state(state_info: Dict[str, Any]) -> GraphState:
    """
    Create a dynamic GraphState based on the provided state information.

    This function takes a dictionary of key-value pairs and creates a dynamic GraphState
    object. The function is used by the create_dynamic_workflow function to create a
    GraphState object that is passed to the WorkflowBuilder.

    Parameters:
        state_info: Dict[str, Any] - A dictionary containing the state information

    Returns:
        GraphState - A dynamic GraphState object with the provided state information.
    """
    graph_state = GraphState()
    # You can also add additional dynamic fields that are passed in the request
    for key, value in state_info.items():
        graph_state[key] = value

    return GraphState(state=graph_state)
