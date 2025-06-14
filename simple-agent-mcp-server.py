"""Azure AI Agent Service MCP Server for Claude Desktop using Azure AI Search and Bing Web Grounding Tools."""

import os
import sys
import asyncio
from dotenv import load_dotenv
from fastmcp import FastMCP
import time

# Import Azure AI Agent Service modules
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ListSortOrder


# Create MCP server
mcp = FastMCP(
    "azure-ai-agent", 
   
)
print("MCP server instance created", file=sys.stderr)

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add an agent invocation tool
@mcp.tool()
def invoke_agent(message: str) -> str:
    """Invoke AI Agent"""

    # Load environment variables
    load_dotenv()
    print("Environment variables loaded", file=sys.stderr)
    credential = DefaultAzureCredential()

    agent_client = AgentsClient(endpoint=os.getenv("PROJECT_CONNECTION_STRING"), credential=credential)

    '''
    agent = agent_client.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="city-travel-agent",
        instructions="You are helpful agent"
    )
    '''

    agent = agent_client.get_agent(agent_id=os.getenv("AGENT_ID"))

    thread = agent_client.threads.create()

    userMessage = agent_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )

    print(f"Created message, ID: {userMessage.id}")


    # Process the run
    run = agent_client.runs.create(thread_id=thread.id, agent_id=agent.id)
    print(f"Run ID: {run.id}")
    
    # Poll the run status
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = agent_client.runs.get(thread_id=thread.id, run_id=run.id)
        print(f"Run status: {run.status}")

    if run.status == "failed":
        print(f"Run error: {run.last_error}")

    messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    lastMessage = None
    for msg in messages:
        print(f"Message ID: {msg.id}, Role: {msg.role}")
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role}: {last_text.text.value}")
            lastMessage = last_text.text.value
    # List messages in the thread
    if lastMessage:
        print(f"Last message from agent: {lastMessage}")
        return lastMessage

if __name__ == "__main__":
    # Run the server with stdio transport (default)
    print("Starting MCP server run...", file=sys.stderr)
    mcp.run(transport="sse", host="127.0.0.1", port=8000)
