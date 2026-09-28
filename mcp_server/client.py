import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# =========================================================
# MCP SERVER CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SERVER_FILE = PROJECT_ROOT / "mcp_server" / "server.py"


# =========================================================
# MCP SERVER PARAMETERS
# =========================================================

server_parameters = StdioServerParameters(
    command="python",
    args=[str(SERVER_FILE)],
    cwd=str(PROJECT_ROOT)
)


# =========================================================
# LIST AVAILABLE MCP TOOLS
# =========================================================

async def list_mcp_tools():

    async with stdio_client(
        server_parameters
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.list_tools()

            return result.tools


# =========================================================
# CALL AN MCP TOOL
# =========================================================

async def call_mcp_tool(
    tool_name: str,
    arguments: dict
):

    async with stdio_client(
        server_parameters
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments
            )

            return result


# =========================================================
# SYNCHRONOUS HELPERS
# =========================================================

def get_mcp_tools():

    return asyncio.run(
        list_mcp_tools()
    )


def call_tool(
    tool_name: str,
    arguments: dict
):

    return asyncio.run(
        call_mcp_tool(
            tool_name,
            arguments
        )
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\nConnecting to MCP server...\n")

    tools = get_mcp_tools()

    print("Available MCP tools:\n")

    for tool in tools:

        print(
            f"- {tool.name}"
        )

    print(
        "\nMCP client connection test successful!"
    )