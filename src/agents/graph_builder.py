from langgraph.graph import StateGraph, END
from src.schemas import AgentState
from src.agents.graph.nodes import input_node,planner_node,validator_node,ui_node,sql_generation_node,db_query_node
from src.agents.graph.nodes import comparison_node,report_node
from typing import Optional
from langchain_core.runnables import Runnable


class GraphBuilder:
    def __init__(self):
        self.builder = StateGraph(AgentState)

    def register_nodes(self):
        """
        Register all nodes in the graph
        """
        self.builder.add_node("input", input_node)
        self.builder.add_node("validate", validator_node)
        self.builder.add_node("plan", planner_node)
        self.builder.add_node("ui", ui_node)
        self.builder.add_node("sql_generation", sql_generation_node)
        self.builder.add_node("db_query_data", db_query_node)
        self.builder.add_node("comparison_node", comparison_node)
        self.builder.add_node("report_node", report_node)



    def register_edges(self):
        """
        Define graph flow and routing
        """

        self.builder.set_entry_point("input")

        self.builder.add_edge("input", "validate")
        self.builder.add_edge("validate", "plan")
        self.builder.add_edge("plan", "ui")
        self.builder.add_edge("ui","sql_generation")
        self.builder.add_edge("sql_generation","db_query_data")
        self.builder.add_edge("db_query_data","comparison_node")
        self.builder.add_edge("comparison_node","report_node")
        self.builder.add_edge("report_node", END)


    @staticmethod
    def route_after_validation(state: AgentState) -> str:
        """
        Decide next step based on validation result
        """
        if state.validation_error:
            return "end"
        return "plan"

    def build(self):
        """
        Compile graph
        """
        self.register_nodes()
        self.register_edges()
        return self.builder.compile()



class GraphProvider:
    _graph_instance: Optional[Runnable] = None

    @classmethod
    def get(cls) -> Runnable:
        if cls._graph_instance is None:
            cls._graph_instance = GraphBuilder().build()
        return cls._graph_instance