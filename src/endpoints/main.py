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
        initial_state=RunAgentRequest(
            user_input=request.user_input
        )

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

        sql_generate = (
            result["generated_sql"]
            if result.get("generated_sql")
            else None
        )

        response=RunAgentResponse(
            parsed_input=parsed_input,
            execution_plan=execution_plan,
            raw_llm_output=result.get("raw_llm_output"),
            validation_error=result.get("validation_error"),
            ui_data=ui_data,
            sql_generation=sql_generate,
            db_data=result.get("db_data"),
            comparison_result=result.get("comparison_result"),
            final_report=result.get("final_report")

        )

        return response

    except Exception as e:
        logger.exception("Error during agent execution")

        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
