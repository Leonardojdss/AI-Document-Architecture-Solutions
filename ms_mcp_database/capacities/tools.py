from mcp.server.fastmcp import FastMCP, Context
from ms_mcp_database.infra.postgrsql_connection import PostgreSQLConnection

# instance the MCP server
mcp = FastMCP()
db = PostgreSQLConnection()

@mcp.tool()
def list_archives_blob(type_documento: str) -> str:
