from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph_supervisor import create_supervisor
from langchain_core.messages import convert_to_messages
from langgraph.prebuilt import create_react_agent
from ms_langgraph_agents.infrastructure.connection_openai import ConnectionAzureOpenai

llm = ConnectionAzureOpenai.llm_azure_openai()

analyze_contracts_agent = create_react_agent(
    model=llm,
    tools=[],
    prompt=(
        "você é um agente de análise de contratos.\n\n"
    ),
    name="analyze_contracts_agent",
)

resume_contracts_agent = create_react_agent(
    model=llm,
    tools=[],
    prompt=(
        "você é um agente de resumo de contratos.\n\n"
    ),
    name="resume_contracts_agent",
)

supervisor = create_supervisor(
    model=llm,
    agents=[analyze_contracts_agent, resume_contracts_agent],
    prompt=(
        "Você é um supervisor de agentes, deve decidir se envia a tarefa para o analisador ou resumidor.\n\n"
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
    ).compile()

def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")

for chunk in supervisor.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "o que é um contrato resumido? envie para o agente de resumo ou analise",
            }
        ]
    },
):
    pretty_print_messages(chunk, last_message=True)

final_message_history = chunk["supervisor"]["messages"]