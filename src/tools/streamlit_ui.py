import streamlit as st

from src.agents import graph
from src.schemas import AgentState

st.set_page_config(page_title="ValidateAI", layout="wide")
st.title("🤖 ValidateAI")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Render History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.write(msg["content"])
        else:
            st.json(msg["output"])


# -----------------------------
# Input
# -----------------------------
user_input = st.chat_input("Ask your query...")

if user_input:
    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # -----------------------------
    # Run LangGraph (stream mode)
    # -----------------------------
    with st.chat_message("assistant"):
        st.write("### Agent Execution")

        initial_state = AgentState(
            user_input=user_input,
            parsed_input=None,
            execution_plan=None,
            validation_error=None,
            raw_llm_output=None,
            ui_data=None
        )

        step_outputs = {}

        for event in graph.stream(initial_state):
            for node_name, state in event.items():

                st.write(f"#### Step: {node_name}")

                # Convert state safely
                # state_dict = state.model_dump()
                if hasattr(state, "model_dump"):
                    state_dict = state.model_dump()
                else:
                    state_dict = state

                st.json(state_dict)

                step_outputs[node_name] = state_dict

        final_state = state


        def safe_get(obj, attr):
            if hasattr(obj, attr):
                return getattr(obj, attr)
            elif isinstance(obj, dict):
                return obj.get(attr)
            return None


        def safe_dump(value):
            if hasattr(value, "model_dump"):
                return value.model_dump()
            return value


        parsed_input = safe_get(final_state, "parsed_input")
        execution_plan = safe_get(final_state, "execution_plan")
        ui_data = safe_get(final_state, "ui_data")
        validation_error = safe_get(final_state, "validation_error")

        result = {
            "parsed_input": safe_dump(parsed_input),
            "execution_plan": safe_dump(execution_plan),
            "ui_data": ui_data,
            "validation_error": validation_error
        }

        st.write("### Final Output")
        st.json(result)

    # store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "output": result
    })