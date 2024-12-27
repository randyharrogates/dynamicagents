# app/main.py

from fastapi import FastAPI, HTTPException
from src.models import CreateAgentRequest
from src.agent_creator import create_agent, save_agent_to_json
from typing import Dict, Any

app = FastAPI()


@app.post("/create-agent/")
async def create_agent_endpoint(data: CreateAgentRequest) -> Dict[str, Any]:
    try:
        # Create the agent using the provided data
        agent_data = create_agent(data)

        # Save the agent to a JSON file (you can also store it in a database)
        save_agent_to_json(agent_data)

        # Return the agent data as JSON
        return agent_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
