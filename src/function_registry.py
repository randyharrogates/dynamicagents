"""
Module is used as a function registry to initialize the available functions 
for the agent to execute. In a sense, this is also an agent class.
"""

from llm import LLM
from typing import List, Dict
from models import GraphState, Callable, Agent


class FunctionRegistry:
    """
    A registry that holds available functions for agents to execute.
    Used to create a single agent
    """

    def __init__(self, agent_data: Agent):
        self.state_variables = agent_data.state_variables
        self.llm_caller = LLM(agent_data.model_name)
        self.initial_query = agent_data.initial_query
        self.parse_query_output = ""
        self.functions = {"_parse_query": self.initial_query}
        self._get_initial_state()

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

    def _get_initial_state(self):
        """
        Dynamically creates instance variables based on the keys in the state.data dictionary.
        """
        # Iterate through the state data and create dynamic variables
        for key, _ in self.state_variables:
            # Dynamically create instance variables on 'self'
            setattr(self, key, getattr(self, key))

    def _get_current_state(self) -> Dict[str, Any]:
        """
        Retrieve the current state of the agent before any actions are performed.
        This method collects all dynamically created instance variables as part of the state.
        """
        current_state = {
            key: getattr(self, key, None) for key in self.state_variables.keys()
        }
        return current_state

    def _update_agent_state(self, state_updates: Dict[str, Any]) -> None:
        """
        Update the agent's state after performing an operation.
        This method updates the instance variables (self.<key>) based on the provided state_updates.
        """
        for key, value in state_updates.items():
            setattr(self, key, value)  # Update the state dynamically on 'self'

        # Log the updated state for debugging purposes
        logger.info(f"Updated agent state: {state_updates}")

    def _parse_query(self, query: str) -> str:
        """Create first query"""
        self.parse_query_output = self.llm_caller.get_llm_response(query)

    def run(self) -> Dict:
        """
        Run a dict of functions based on the function names provided.
        Each function in the list will be executed in order.
        """
        for function_name, params in self.functions.items():
            # Retrieve the function from the registry
            function = self.get_function(function_name)
            logger.info(f"Running function: {function_name}")
            # Execute the function
            function(params)  # Just call the function without capturing the result

        # After executing the function, update the state based on the current function's output
        updated_state = self._get_current_state()
        self._update_agent_state(updated_state)

        return self._get_current_state()
