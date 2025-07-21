from langgraph.graph import StateGraph, START, MessagesState, END
from ms_langgraph_agents.process.agents import NetworkAgents


class Graph:

    @staticmethod
    async def contracts_supervisor_graph():
        supervisor_contract_agent = NetworkAgents.supervisor_contracts()
        agent_analyze_contracts = await NetworkAgents.agent_analyze_contracts()
        agent_resume_contracts = await NetworkAgents.agent_resume_contracts()

        supervisor_contract = (
            StateGraph(MessagesState)
            .add_node(supervisor_contract_agent, destinations=("analyze_contracts_agent", "resume_contracts_agent", END))
            .add_node("analyze_contracts_agent", agent_analyze_contracts)
            .add_node("resume_contracts_agent", agent_resume_contracts)
            .add_edge(START, "supervisor_contracts")
            .add_edge("analyze_contracts_agent", "supervisor_contracts")
            .add_edge("resume_contracts_agent", "supervisor_contracts")
            .compile()
        )
        return supervisor_contract

    @staticmethod
    async def document_supervisor_graph():
        supervisor_document_agent = NetworkAgents.supervisor_documents()
        agent_analyze_documents = await NetworkAgents.agent_analyze_documents()
        agent_resume_documents = await NetworkAgents.agent_resume_documents()

        supervisor_document = (
            StateGraph(MessagesState)
            .add_node(supervisor_document_agent, destinations=("analyze_documents_agent", "resume_documents_agent", END))
            .add_node("analyze_documents_agent", agent_analyze_documents)
            .add_node("resume_documents_agent", agent_resume_documents)
            .add_edge(START, "supervisor_documents")
            .add_edge("analyze_documents_agent", "supervisor_documents")
            .add_edge("resume_documents_agent", "supervisor_documents")
            .compile()
        )
        return supervisor_document