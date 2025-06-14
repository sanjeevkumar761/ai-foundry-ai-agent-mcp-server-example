from fastmcp import Client

async def main():
    # Connect via SSE
    async with Client("http://localhost:8000/sse") as client:
        # ... use the client
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result[0].text}")

        result2 = await client.call_tool("invoke_agent", {"message": "What is the capital of France?"})
        print(f"Agent response: {result2[0].text}")

if __name__ == "__main__":
    # Run the server with stdio transport (default)
    import asyncio
    asyncio.run(main())