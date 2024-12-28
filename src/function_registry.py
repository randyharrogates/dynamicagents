"""
Module is used as a function registry to initialize the available functions 
for the agent to execute. In a sense, this is also an agent class.
"""

from llm import LLM
from typing import List
from models import AgentMemory, AgentTool, GraphState, Callable


class FunctionRegistry:
    """
    A registry that holds available functions for agents to execute.
    """

    def __init__(
        self, memories: List[AgentMemory], tools: List[AgentTool], state: GraphState
    ):
        self.state = state
        self.memory = memories
        self.tools = tools
        self.llm_caller = LLM()
        self.functions = {
            "_parse_query": self._parse_query,
            "_summarize_query": self._summarize_query,
            "_augment_query": self._augment_query,
            "_generate_final_query": self._generate_final_query,
        }
        self._get_current_state(self.state)

    def register(self, function_name: str, function: Callable):
        """
        Register a new function in the registry.
        """
        self.functions[function_name] = function

    def get_function(self, function_name: str) -> Callable:
        """
        Retrieve a function by its name from the registry.
        """
        if function_name not in self.functions:
            raise ValueError(f"Function '{function_name}' is not registered.")
        return self.functions[function_name]

    def _get_current_state(self, state: GraphState):
        """
        Dynamically creates instance variables based on the keys in the state.data dictionary.
        """
        # Iterate through the state data and create dynamic variables
        for key, value in state.data.items():
            # Dynamically create instance variables on 'self'
            setattr(self, key, value)

    def _parse_query(self, query: str, kwargs) -> str:
        """Create first query"""
        agent_feedback = self.llm_caller.get_llm_response(query.format(**kwargs))
        return agent_feedback

    def _summarize_query(self, query: str, kwargs) -> str:
        """Summarize the user's query using the chosen LLM."""
        summary_feedback = self._parse_query(query, kwargs)
        return summary_feedback

    def _augment_query(self, query: str, documents: list[str]) -> str:
        """Combine the query with retrieved documents."""
        context = "\n".join(documents)
        return f"Query: {query}\nContext:\n{context}\nAnswer:"

    def _generate_final_query(self, original_query: str, augmented_query: str) -> str:
        """Generate a response using the chosen LLM."""
        final_query = "\n".join([original_query, augmented_query])
        return final_query

    def run(self, function_names: List[str], agent: "Agent") -> dict:
        """
        Run a list of functions based on the function names provided.
        Each function in the list will be executed in order.
        """
        result = self._parse_query(self._get_current_state.initial_output, self.state)
        results = {}
        for function_name in function_names:
            function = self.get_function(function_name)
            results[function_name] = function(agent, state)
        return results


# # Example functions that can be dynamically assigned to agents
# def run_example_function(input_data: str) -> str:
#     """
#     A simple function that simulates an agent's 'run' function.
#     """
#     return f"Processed input: {input_data}"
