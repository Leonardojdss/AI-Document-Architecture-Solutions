from ms_langgraph_agents.process.graph import Graph
from ms_langgraph_agents.services.messages_services import pretty_print_messages

def conversation_contracts_usecase(input_message):

    Graph_supervisor_contracts = Graph.contracts_supervisor_graph()

    for chunk in Graph_supervisor_contracts.stream(
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

    final_message_history = chunk["supervisor"]["messages"]
    return final_message_history