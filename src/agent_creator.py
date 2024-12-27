# app/agent_creator.py

import json
from typing import Dict, Any
from .models import CreateAgentRequest


def create_agent(data: CreateAgentRequest) -> Dict[str, Any]:
    # Convert the Pydantic model to a dictionary
    agent_data = data.dict()

    # For demonstration, we're just returning the same data. In real use,
    # you can integrate logic to instantiate agents dynamically.
    return agent_data


def save_agent_to_json(agent_data: Dict[str, Any], file_path: str = "agents.json"):
    # Save the agent data to a JSON file
    with open(file_path, "a") as f:
        json.dump(agent_data, f, indent=4)
        f.write("\n")  # Add a newline between different agents
