# app/agent_creator.py

from pydantic.utils import model_dump
import json
from typing import Dict, Any
from .models import CreateAgentRequest, Agent, AgentFunction, AgentTool, AgentMemory


def create_agents(data: CreateAgentRequest) -> Dict[str, Agent]:
    """
    Create multiple agents based on the incoming data
    and return a dictionary of agent objects.

    Parameters:
    - data: CreateAgentRequest - A Pydantic model containing the list of agents.

    Returns:
    - agents_dict: Dict[str, Agent] - A dictionary where the key is the agent name
        and the value is the agent object.
    """

    agents_dict = {}

    for agent in data.agents:
        # Create the agent functions, tools, and memory by instantiating the respective models
        functions = [
            AgentFunction(
                name=function.name,
                description=function.description,
                code=function.code,
            )
            for function in agent.functions
        ]
        tools = [
            AgentTool(name=tool.name, description=tool.description, code=tool.code)
            for tool in agent.tools
        ]
        memory = [
            AgentMemory(type=mem.type, description=mem.description, code=mem.code)
            for mem in agent.memory
        ]

        # Create an Agent object by passing the fields to the Agent constructor
        agent_obj = Agent(
            name=agent.name,
            description=agent.description,
            functions=functions,
            tools=tools,
            memory=memory,
        )

        # Add the created agent object to the dictionary using the agent's name as the key
        agents_dict[agent.name] = agent_obj

    # Return the dictionary of agent objects
    return agents_dict


def save_agent_to_json(agent_data: Dict[str, Any], file_path: str = "agents.json"):
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
