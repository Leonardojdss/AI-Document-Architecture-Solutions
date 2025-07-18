from langgraph.graph import StateGraph, START, MessagesState, END
from ms_langgraph_agents.process.agents import NetworkAgents

supervisor_contract_agent = NetworkAgents.supervisor_contracts()
agent_analyze_contracts = NetworkAgents.agent_analyze_contracts()
agent_resume_contracts = NetworkAgents.agent_resume_contracts()

supervisor_document_agent = NetworkAgents.supervisor_documents()
agent_analyze_documents = NetworkAgents.agent_analyze_documents()
agent_resume_documents = NetworkAgents.agent_resume_documents()

# Define the multi-agent supervisor graph
class Graph:

    @staticmethod
    def contracts_supervisor_graph():
        supervisor_contract = (
            StateGraph(MessagesState)
            # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
            .add_node(supervisor_contract_agent, destinations=("analyze_contracts_agent", "resume_contracts_agent", END))
            .add_node(agent_analyze_contracts)
            .add_node(agent_resume_contracts)
            .add_edge(START, "supervisor_contracts")
            # always return back to the supervisor
            .add_edge("analyze_contracts_agent", "supervisor_contracts")
            .add_edge("resume_contracts_agent", "supervisor_contracts")
            .compile()
        )
        return supervisor_contract

    @staticmethod
    def document_supervisor_graph():
        supervisor_document = (
            StateGraph(MessagesState)
            .add_node(supervisor_document_agent, destinations=("analyze_documents_agent", "resume_documents_agent", END))
            .add_node(agent_analyze_documents)
            .add_node(agent_resume_documents)
            .add_edge(START, "supervisor_documents")
            .add_edge("analyze_documents_agent", "supervisor_documents")
            .add_edge("resume_documents_agent", "supervisor_documents")
            .compile()
        )
        return supervisor_document