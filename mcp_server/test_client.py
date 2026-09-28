import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # -----------------------------------------------------
    # START THE MCP SERVER
    # -----------------------------------------------------

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"],
    )

    # -----------------------------------------------------
    # CONNECT TO THE SERVER
    # -----------------------------------------------------

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            print("\nMCP server connected successfully!\n")

            # -------------------------------------------------
            # LIST AVAILABLE TOOLS
            # -------------------------------------------------

            response = await session.list_tools()

            print("Available MCP tools:\n")

            for tool in response.tools:

                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
                print("-" * 60)

            print("\nMCP server test completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())