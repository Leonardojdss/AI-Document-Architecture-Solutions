from langchain_mcp_adapters.client import MultiServerMCPClient

async def mcp_database():
    client = MultiServerMCPClient(
        {
            "database and blob": {
                "url": "http://localhost:8002/sse",
                "transport": "sse",
            }
        }
    )
    tools = await client.get_tools()
    return tools

