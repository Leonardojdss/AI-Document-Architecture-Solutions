from langgraph.graph import END
from langgraph.graph import StateGraph, START, MessagesState
from process.agents import NetworkAgents

supervisor_agent = NetworkAgents.supervisor()
agent_analyze_contracts = NetworkAgents.agent_analyze_contracts()
agent_resume_contracts = NetworkAgents.agent_resume_contracts()

# Define the multi-agent supervisor graph
def supervisor_graph():
    supervisor = (
        StateGraph(MessagesState)
        .add_node(supervisor_agent, destinations=("agent_analyze_contracts", "agent_resume_contracts", END))
        .add_node(agent_analyze_contracts)
        .add_node(agent_resume_contracts)
        .add_edge(START, "supervisor")
        .add_edge("agent_analyze_contracts", "supervisor")
        .add_edge("agent_resume_contracts", "supervisor")
        .compile()
        )
    return supervisor