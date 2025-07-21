from langchain_mcp_adapters.client import MultiServerMCPClient
import os
import logging

logger = logging.getLogger(__name__)

async def mcp_database():
    mcp_url = os.getenv("MCP_DATABASE_URL")
    
    try:
        logger.info(f"Attempting to connect to MCP service at: {mcp_url}")
        
        client = MultiServerMCPClient(
            {
                "database and blob": {
                    "url": mcp_url,
                    "transport": "sse",
                }
            }
        )
        tools = await client.get_tools()
        logger.info(f"Successfully connected to MCP service and retrieved {len(tools)} tools")
        return tools
        
    except Exception as e:
        logger.error(f"Failed to connect to MCP service at {mcp_url}: {str(e)}")

        return []

