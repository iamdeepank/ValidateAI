import pandas as pd
import streamlit as st

from src.agents import graph
from src.schemas import AgentState
import platform
import asyncio

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ValidateAI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ValidateAI")
st.caption(" Dashboard Validation Platform")


# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HELPERS
# =========================================================
def safe_get(obj, key, default=None):

    # Pydantic object
    if hasattr(obj, key):
        return getattr(obj, key)

    # Dictionary
    if isinstance(obj, dict):
        return obj.get(key, default)

    return default


def safe_dump(value):

    if hasattr(value, "model_dump"):
        return value.model_dump()

    return value


def render_status(status):

    if status == "PASS":
        st.success("✅ VALIDATION PASSED")

    elif status == "FAIL":
        st.error("❌ VALIDATION FAILED")

    else:
        st.warning("⚠️ VALIDATION STATUS UNKNOWN")


def render_metric_cards(report):

    if not report:
        return

    summary = report.get("summary", {})

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "UI Rows",
            summary.get("total_ui_rows", 0)
        )

    with c2:
        st.metric(
            "DB Rows",
            summary.get("total_db_rows", 0)
        )

    with c3:
        st.metric(
            "Matched Rows",
            summary.get("matched_rows", 0)
        )

    with c4:
        st.metric(
            "Failed Rows",
            summary.get("failed_rows", 0)
        )


def highlight_status(row):

    if row["status"] == "PASS":
        return [
            "background-color: #d4edda"
        ] * len(row)

    return [
        "background-color: #f8d7da"
    ] * len(row)


# =========================================================
# CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":

            st.write(msg["content"])

        else:

            st.json(msg["output"])


# =========================================================
# USER INPUT
# =========================================================
user_input = st.chat_input(
    "Ask validation query..."
)

if user_input:

    # =====================================================
    # STORE USER MESSAGE
    # =====================================================
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    # =====================================================
    # ASSISTANT RESPONSE
    # =====================================================
    with st.chat_message("assistant"):

        with st.spinner(
            "Running validation workflow..."
        ):

            # =============================================
            # INITIAL STATE
            # =============================================
            initial_state = AgentState(
                user_input=user_input
            )

            # =============================================
            # FINAL MERGED STATE
            # =============================================
            final_state = {}

            # =============================================
            # EXECUTION TRACE
            # =============================================
            with st.expander(
                "⚙️ Agent Execution Trace",
                expanded=False
            ):

                for event in graph.stream(initial_state):

                    for node_name, state in event.items():

                        st.write(
                            f"### Node: `{node_name}`"
                        )

                        state_dict = safe_dump(state)

                        st.json(state_dict)

                        # =================================
                        # MERGE PARTIAL STATE UPDATES
                        # =================================
                        if isinstance(state_dict, dict):
                            final_state.update(
                                state_dict
                            )

            # =============================================
            # EXTRACT FINAL VALUES
            # =============================================
            parsed_input = safe_dump(
                final_state.get("parsed_input")
            )

            execution_plan = safe_dump(
                final_state.get("execution_plan")
            )

            ui_data = safe_dump(
                final_state.get("ui_data")
            )

            db_data = safe_dump(
                final_state.get("db_data")
            )

            generated_sql = safe_dump(
                final_state.get("generated_sql")
            )

            comparison_result = safe_dump(
                final_state.get("comparison_result")
            )

            final_report = safe_dump(
                final_state.get("final_report")
            )

            validation_error = safe_dump(
                final_state.get("validation_error")
            )
            # =============================================
            # VALIDATION ERROR
            # =============================================
            if validation_error:

                st.error(validation_error)

            # =============================================
            # STATUS
            # =============================================
            if final_report:

                render_status(
                    final_report.get("status")
                )

                render_metric_cards(
                    final_report
                )

            st.divider()

            # =============================================
            # TABS
            # =============================================
            tabs = st.tabs([
                "📥 Parsed Input",
                "🧠 Execution Plan",
                "🖥️ UI Data",
                "🗄️ DB Data",
                "🧾 SQL Query",
                "⚖️ Comparison",
                "📄 Final Report"
            ])

            # =============================================
            # PARSED INPUT
            # =============================================
            with tabs[0]:

                st.subheader(
                    "Parsed User Input"
                )

                st.json(parsed_input)

            # =============================================
            # EXECUTION PLAN
            # =============================================
            with tabs[1]:

                st.subheader(
                    "Execution Workflow"
                )

                if execution_plan:

                    steps = execution_plan.get(
                        "steps",
                        []
                    )

                    df = pd.DataFrame(steps)

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

            # =============================================
            # UI DATA
            # =============================================
            with tabs[2]:

                st.subheader(
                    "Extracted UI Data"
                )

                if ui_data:

                    ui_df = pd.DataFrame(
                        ui_data
                    )

                    st.dataframe(
                        ui_df,
                        use_container_width=True
                    )

            # =============================================
            # DB DATA
            # =============================================
            with tabs[3]:

                st.subheader(
                    "Backend Database Data"
                )

                if db_data:

                    db_df = pd.DataFrame(
                        db_data
                    )

                    st.dataframe(
                        db_df,
                        use_container_width=True
                    )

            # =============================================
            # SQL QUERY
            # =============================================
            with tabs[4]:

                st.subheader(
                    "Generated SQL"
                )

                if generated_sql:

                    st.code(
                        generated_sql,
                        language="sql"
                    )

            # =============================================
            # COMPARISON
            # =============================================
            with tabs[5]:

                st.subheader(
                    "Metric-Level Comparison"
                )

                if comparison_result:

                    metric_results = (
                        comparison_result.get(
                            "metric_results",
                            []
                        )
                    )

                    comparison_df = (
                        pd.DataFrame(
                            metric_results
                        )
                    )

                    styled_df = (
                        comparison_df.style.apply(
                            highlight_status,
                            axis=1
                        )
                    )

                    st.dataframe(
                        styled_df,
                        use_container_width=True
                    )

            # =============================================
            # FINAL REPORT
            # =============================================
            with tabs[6]:

                st.subheader(
                    "Validation Report"
                )

                st.json(final_report)

            # =============================================
            # STORE FINAL RESPONSE
            # =============================================
            result = {
                "parsed_input": parsed_input,
                "execution_plan": execution_plan,
                "ui_data": ui_data,
                "db_data": db_data,
                "generated_sql": generated_sql,
                "comparison_result": comparison_result,
                "final_report": final_report,
                "validation_error": validation_error
            }

            st.session_state.messages.append({
                "role": "assistant",
                "output": result
            })