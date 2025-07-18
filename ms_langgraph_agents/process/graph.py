from langgraph.graph import END
from langgraph.graph import StateGraph, START, MessagesState, END
from ms_langgraph_agents.process.agents import NetworkAgentsContracts

supervisor_contract_agent = NetworkAgentsContracts.supervisor_contracts()
agent_analyze_contracts = NetworkAgentsContracts.agent_analyze_contracts()
agent_resume_contracts = NetworkAgentsContracts.agent_resume_contracts()

# Define the multi-agent supervisor graph
class Graph:

    @staticmethod
    def contracts_supervisor_graph():
        supervisor = (
            StateGraph(MessagesState)
            # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
            .add_node(supervisor_contract_agent, destinations=("analyze_contracts_agent", "resume_contracts_agent", END))
            .add_node(agent_analyze_contracts)
            .add_node(agent_resume_contracts)
            .add_edge(START, "supervisor")
            # always return back to the supervisor
            .add_edge("analyze_contracts_agent", "supervisor")
            .add_edge("resume_contracts_agent", "supervisor")
            .compile()
        )
        return supervisor