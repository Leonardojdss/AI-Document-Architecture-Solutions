from ms_langgraph_agents.process.mcp_tools import mcp_database
from langgraph.prebuilt import create_react_agent
from ms_langgraph_agents.infrastructure.connection_openai import ConnectionAzureOpenai
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState, create_react_agent
from langgraph.graph import MessagesState, END
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent

llm = ConnectionAzureOpenai.llm_azure_openai()
mcp_tools = mcp_database()

class NetworkAgents:

    @staticmethod
    def prompt(path):
        with open(path, "r") as file:
            return file.read()

    @staticmethod
    def create_handoff_tool(*, agent_name: str, description: str | None = None):
        name = f"transfer_to_{agent_name}"
        description = description or f"Ask {agent_name} for help."

        @tool(name, description=description)
        def handoff_tool(
            state: Annotated[MessagesState, InjectedState],
            tool_call_id: Annotated[str, InjectedToolCallId],
        ) -> Command:
            tool_message = {
                "role": "tool",
                "content": f"Successfully transferred to {agent_name}",
                "name": name,
                "tool_call_id": tool_call_id,
            }
            return Command(
                goto=agent_name,  
                update={**state, "messages": state["messages"] + [tool_message]},  
                graph=Command.PARENT,  
            )

        return handoff_tool

    analyze_contracts_agent_prompt = prompt("ms_langgraph_agents/prompt/analise_contratos_prompt.txt")

    @staticmethod
    def agent_analyze_contracts():
        analyze_contracts_agent = create_react_agent(
            model=llm,
            tools=mcp_tools,
            prompt=(
                f"{NetworkAgents.analyze_contracts_agent_prompt}"
            ),
            name="analyze_contracts_agent",
        )
        return analyze_contracts_agent

    assign_to_analyze_contracts_agent = create_handoff_tool(
        agent_name="analyze_contracts_agent",
        description="Atribuir tarefa a um agente de análise de contratos.",
    )

    resume_contracts_agent_prompt = prompt("ms_langgraph_agents/prompt/consulta_analise_prompt.txt")

    @staticmethod
    def agent_resume_contracts():
        resume_contracts_agent = create_react_agent(
            model=llm,
            tools=mcp_tools,
            prompt=(
                f"{NetworkAgents.resume_contracts_agent_prompt}"
            ),
            name="resume_contracts_agent",
        )
        return resume_contracts_agent
    
    assign_to_resume_contracts_agent = create_handoff_tool(
        agent_name="resume_contracts_agent",
        description="Atribuir tarefa a um agente de resumo de contratos.",
    )

    @staticmethod
    def supervisor_contracts():
        supervisor_contracts_agent = create_react_agent(
            model=llm,
            tools=[
            NetworkAgents.assign_to_analyze_contracts_agent,
            NetworkAgents.assign_to_resume_contracts_agent
            ],
            prompt=(
            "Você é um supervisor responsável por gerenciar dois agentes:\n"
            "- Um agente de análise de contratos. Atribua tarefas relacionadas à análise de contratos para este agente.\n"
            "- Um agente de resumo de contratos. Atribua tarefas relacionadas a responder dúvidas de contratos para este agente.\n"
            "Atribua o trabalho para apenas um agente por vez, não chame agentes em paralelo.\n"
            "Não execute nenhuma tarefa você mesmo." \
            "ao final responda com o conteúdo do último agente chamado," \
            "Você receber o ocr de um contrato (então deve enviar para analise ao agente de análise de contratos)" \
            "ou uma pergunta sobre um contrato (então deve enviar para o agente de resumo de contratos buscar a resposta no banco ou informação no blob)"
            ),
            name="supervisor_contracts"
        )
        return supervisor_contracts_agent

    analyze_documents_prompt = prompt("ms_langgraph_agents/prompt/analise_documentos_processuais_prompt.txt")

    @staticmethod
    def agent_analyze_documents():
        analyze_documents_agent = create_react_agent(
            model=llm,
            tools=mcp_tools,
            prompt=(
                f"{NetworkAgents.analyze_documents_prompt}"
            ),
            name="analyze_documents_agent",
        )
        return analyze_documents_agent

    assign_to_analyze_documents_agent = create_handoff_tool(
        agent_name="analyze_documents_agent",
        description="Atribuir tarefa a um agente de análise de documentos.",
    )
    resume_documents_prompt = prompt("ms_langgraph_agents/prompt/consulta_documentos_processuais_prompt.txt")
    
    @staticmethod
    def agent_resume_documents():
        resume_documents_agent = create_react_agent(
            model=llm,
            tools=mcp_tools,
            prompt=(
                f"{NetworkAgents.resume_documents_prompt}"
            ),
            name="resume_documents_agent",
        )
        return resume_documents_agent

    assign_to_resume_documents_agent = create_handoff_tool(
        agent_name="resume_documents_agent",
        description="Atribuir tarefa a um agente de resumo de documentos.",
    )

    @staticmethod
    def supervisor_documents():
        supervisor_documents_agent = create_react_agent(
            model=llm,
            tools=[
                NetworkAgents.assign_to_analyze_documents_agent,
                NetworkAgents.assign_to_resume_documents_agent
            ],
            prompt=(
                "Você é um supervisor responsável por gerenciar dois agentes:\n"
                "- Um agente de análise de documentos. Atribua tarefas relacionadas à análise de documentos para este agente.\n"
                "- Um agente de resumo de documentos. Atribua tarefas relacionadas a responder dúvidas de documentos para este agente.\n"
                "Atribua o trabalho para apenas um agente por vez, não chame agentes em paralelo.\n"
                "Não execute nenhuma tarefa você mesmo." \
                "ao final responda com o conteúdo do último agente chamado" \
                "Você receber o ocr de um documento (então deve enviar para analise ao agente de análise de documentos)" \
                "ou uma pergunta sobre um documento (então deve enviar para o agente de resumo de documentos buscar a resposta no banco ou informação no blob)"
            ),
            name="supervisor_documents"
        )
        return supervisor_documents_agent