from langgraph.graph import StateGraph, END
from state import AgentState
from agents import databricks_agent, vector_agent
from memory_manager import save_memory

db_agent = databricks_agent()
vec_agent = vector_agent()


def orchestrator(state: AgentState):
    query = state["query"]

    if "sql" in query.lower():
        return {**state, "next_agent": "databricks"}
    return {**state, "next_agent": "vector"}


def databricks_node(state: AgentState):
    response = db_agent(state["query"])
    return {**state, "response": response}


def vector_node(state: AgentState):
    response = vec_agent(state["query"])
    return {**state, "response": response}


def memory_node(state: AgentState):
    save_memory(state["user_id"], state["response"])
    return state


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("orchestrator", orchestrator)
    builder.add_node("databricks", databricks_node)
    builder.add_node("vector", vector_node)
    builder.add_node("memory", memory_node)

    builder.set_entry_point("orchestrator")

    builder.add_conditional_edges(
        "orchestrator",
        lambda x: x["next_agent"],
        {
            "databricks": "databricks",
            "vector": "vector",
        },
    )

    builder.add_edge("databricks", "memory")
    builder.add_edge("vector", "memory")
    builder.add_edge("memory", END)

    return builder.compile()