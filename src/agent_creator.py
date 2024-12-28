# app/agent_creator.py

from pydantic.utils import model_dump
import json
from typing import Dict, Any, List
from .models import CreateAgentRequest, Agent, AgentFunction, AgentTool, AgentMemory
from .function_registry import FunctionRegistry


class AgentCreator:

    def __init__(self, data: CreateAgentRequest):
        self.data = data
        self.function_registry = FunctionRegistry()

    def create_agents(self) -> Dict[str, Agent]:
        """
        Create multiple agents based on the incoming data
        and return a dictionary of agent objects.

        Returns:
        - agents_dict: Dict[str, Agent] - A dictionary where the key is the agent name
            and the value is the agent object.
        """

        agents_dict = {}

        for agent in self.data.agents:
            # Create the agent functions, tools, and memory by instantiating the respective models
            functions = [
                AgentFunction(
                    name=function.name,
                    description=function.description,
                )
                for function in agent.functions
                if function.name != "run"
            ]
            tools = [
                AgentTool(name=tool.name, description=tool.description, code=tool.code)
                for tool in agent.tools
            ]
            memory = [
                AgentMemory(type=mem.type, description=mem.description, code=mem.code)
                for mem in agent.memory
            ]

            for function in agent.functions:
                if function.name == "run":
                    run_function = function
            if not run_function:
                raise ValueError(f"Run function not defined for agent: {agent.name}")

            # Create an Agent object by passing the fields to the Agent constructor
            agent_obj = Agent(
                name=agent.name,
                description=agent.description,
                functions=functions,
                tools=tools,
                memory=memory,
                model_name=agent.model_name,
            )

            # Add the created agent object to the dictionary using the agent's name as the key
            agents_dict[agent.name] = agent_obj

        # Return the dictionary of agent objects
        return agents_dict

    def _create_functions(self, agent_functions: List[AgentFunction]):
        pass

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
