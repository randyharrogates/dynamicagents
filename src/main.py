# app/main.py

from fastapi import FastAPI, HTTPException
from src.models import CreateAgentRequest, CreateWorkflowRequest
from src.workflow_creator import create_dynamic_workflow
from src.agent_creator import create_agents, save_agent_to_json
from typing import Dict, Any

app = FastAPI()


@app.post("/create-agent/")
async def create_agent_endpoint(data: CreateAgentRequest) -> Dict[str, Any]:
    try:
        # Create the agent using the provided data
        agent_data = create_agents(data)

        # Save the agent to a JSON file (you can also store it in a database)
        save_agent_to_json(agent_data)

        # Return the agent data as JSON
        return agent_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/create-workflow/")
async def create_workflow_endpoint(data: CreateWorkflowRequest):
    try:
        # Create the dynamic workflow
        workflow, _ = create_dynamic_workflow(data)
        result = workflow.compile()
        conversation = result.invoke(
            workflow, {"recursion_limit": 100}, stream_mode="values", debug=True
        )
        final_output = conversation.get("final_output")

        # Return the workflow details (just a simple representation for now)
        return {"final_output": final_output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
