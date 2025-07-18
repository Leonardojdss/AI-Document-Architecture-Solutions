from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from ms_mcp_database.capacities.tools import mcp


def mcp_server_sse(mcp_server: Server, debug: bool = False) -> Starlette:
    """Create a Starlette app with SSE transport for MCP."""
    
    sse = SseServerTransport("/messages/")
    
    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )
    
    routes = [
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
    
    # Create Starlette app
    app = Starlette(debug=debug, routes=routes)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

mcp_server = mcp._mcp_server
mcp_app = mcp_server_sse(mcp_server, debug=True)

if __name__ == "__main__":
    port = 8002
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    uvicorn.run(mcp_app, host="0.0.0.0", port=port)