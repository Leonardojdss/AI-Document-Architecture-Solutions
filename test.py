from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "blob": {
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:8002/sse",
            "transport": "sse",
        }
    }
)
import asyncio

async def main():
    tools = await client.get_tools()
    agent = create_react_agent(
        "azure_openai:gpt-4o",
        tools
    )
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "use a ferramentas de listar blobs do container contratos, sem data"}]}
    )
    print(math_response)

asyncio.run(main())
