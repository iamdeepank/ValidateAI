# app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

from src.agents import graph
from src.schemas import RunAgentRequest, RunAgentResponse


# ---------------------------
# Logging Setup
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------
# App Init
# ---------------------------
app = FastAPI(
    title="Report Validation Agent",
    version="0.1.1"
)


# ---------------------------
# Health Check
# ---------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------
# Main Endpoint
# ---------------------------
@app.post("/run", response_model=RunAgentResponse)
def run_agent(request: RunAgentRequest):
    """
    Main API to process user input via LangGraph agent
    """

    try:
        logger.info(f"Received request: {request.user_input}")

        # Initial graph state
        initial_state = {
            "user_input": request.user_input,
            "parsed_input": None,
            "execution_plan": None,
            "validation_error": None,
            "raw_llm_output": None
        }

        # Invoke LangGraph
        result = graph.invoke(initial_state)
        logger.info("Graph execution completed")

        # ---------------------------
        # Safe Serialization
        # ---------------------------
        parsed_input = (
            result["parsed_input"].model_dump()
            if result.get("parsed_input")
            else None
        )

        execution_plan = (
            result["execution_plan"].model_dump()
            if result.get("execution_plan")
            else None
        )

        ui_data = (
            result["ui_data"]
            if result.get("ui_data")
            else None
        )


        response = {
            "parsed_input": parsed_input,
            "execution_plan": execution_plan,
            "raw_llm_output": result.get("raw_llm_output"),
            "validation_error": result.get("validation_error"),
            "ui_data": ui_data
        }

        return response

    except Exception as e:
        logger.exception("Error during agent execution")

        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
