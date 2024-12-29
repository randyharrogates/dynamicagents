# app/agent_creator.py

from pydantic.utils import model_dump
import json
from typing import Dict, Any, List
from .models import CreateAgentRequest, Agent, AgentFunction, AgentTool, AgentMemory
from .function_registry import FunctionRegistry


class AgentCreator:
    """
    Agent creator to create all agents from the CreateAgentRequest.
    """
    def __init__(self, data: CreateAgentRequest):
        self.data = data

    def create_agents(self) -> Dict[str, Agent]:
        """
        Creates agents based on the CreateAgentRequest and initializes them with functions from FunctionRegistry.
        """
        agents_dict = {}

        # Register extra functions if needed
        for agent_data in self.data.agents:
            # Initialize the agent with the functions from the function registry
            dynamic_agent = FunctionRegistry(agent_data=agent_data)
            # agent_functions = [
            #     function_registry.register(func.name, func.function)
            #     for func in agent_data.functions
            #     if func.name not in function_registry.functions
            # ]

            agents_dict[agent_data.name] = dynamic_agent

        return agents_dict

    def save_agent_to_json(
        self, agent_data: Dict[str, Any], file_path: str = "agents.json"
    ):
        # Save the agent data to a JSON file
        """
        Save the agent data to a JSON file.

        Parameters:
        - agent_data: Dict[str, Any] - A dictionary containing the agent's data.
        - file_path: str - The path of the file to write the data to. Default is "agents.json".

        Returns:
        - None
        """
        with open(file_path, "a") as f:
            json.dump(agent_data, f, indent=4)
            f.write("\n")  # Add a newline between different agents
