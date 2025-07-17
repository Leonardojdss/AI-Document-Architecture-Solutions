from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph_supervisor import create_supervisor
from langchain_core.messages import convert_to_messages
from langgraph.prebuilt import create_react_agent
from ms_langgraph_agents.infrastructure.connection_openai import ConnectionAzureOpenai

llm = ConnectionAzureOpenai.llm_azure_openai()

class NetworkAgents:

    @staticmethod
    def agent_analyze_contracts():
        analyze_contracts_agent = create_react_agent(
            model=llm,
            tools=[],
            prompt=(
                "você é um agente de análise de contratos.\n\n"
            ),
            name="analyze_contracts_agent",
        )
        return analyze_contracts_agent

    @staticmethod
    def agent_resume_contracts():
        resume_contracts_agent = create_react_agent(
            model=llm,
            tools=[],
            prompt=(
                "você é um agente de resumo de contratos.\n\n"
            ),
            name="resume_contracts_agent",
        )
        return resume_contracts_agent

    @staticmethod
    def supervisor():
        supervisor = create_supervisor(
            model=llm,
            agents=[Agents.agent_analyze_contracts(), Agents.agent_resume_contracts()],
            prompt=(
                "Você é um supervisor de agentes, deve decidir se envia a tarefa para o analisador ou resumidor.\n\n"
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
        ).compile()
        return supervisor