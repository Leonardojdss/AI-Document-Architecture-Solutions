from ms_langgraph_agents.process.graph import Graph
from ms_langgraph_agents.services.messages_services import pretty_print_messages

async def conversation_contracts_usecase(input_message):

    graph_supervisor_contracts = await Graph.contracts_supervisor_graph()

    for chunk in graph_supervisor_contracts.astream(
    {
        "messages": [
            {
                "role": "user",
                "content": f"{input_message}",
            }
        ]
        },
    ):
        pretty_print_messages(chunk, last_message=True)

    final_message_history = chunk["supervisor_contracts"]["messages"]
    if final_message_history and len(final_message_history) > 0:
        last_message = final_message_history[-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        else:
            return str(last_message)
    
    return "Nenhuma resposta encontrada"

async def conversation_documents_usecase(input_message):
    graph_supervisor_documents = await Graph.document_supervisor_graph()

    async for chunk in graph_supervisor_documents.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"{input_message}",
                }
            ]
        },
    ):
        pretty_print_messages(chunk, last_message=True)

    final_message_history = chunk["supervisor_documents"]["messages"]
    if final_message_history and len(final_message_history) > 0:
        last_message = final_message_history[-1]
        if hasattr(last_message, 'content'):
            return last_message.content
        else:
            return str(last_message)
    
    return "Nenhuma resposta encontrada"