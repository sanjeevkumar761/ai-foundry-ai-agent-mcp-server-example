# AI Foundry Agent Service MCP Server

This project provides a simple MCP server and client for interacting with Azure AI Agents using FastMCP. It demonstrates how to expose tools and agent invocation endpoints over SSE (Server-Sent Events).

## Features

- **MCP Server**: Exposes tools for addition and invoking Azure AI Agents.
- **MCP Client**: Connects to the server, lists available tools, and calls them.
- **Azure AI Integration**: Uses Azure AI Agents and Azure Identity for secure access.
- **Environment Configuration**: Loads credentials and configuration from environment variables.

## Requirements

- Python 3.8+
- `fastmcp`
- `python-dotenv`
- `azure-ai-agents`
- `azure-identity`

Install dependencies:

```sh
pip install fastmcp python-dotenv azure-ai-agents azure-identity
```

## Usage

### 1. Configure Environment

Create a `.env` file with the following variables:

```
PROJECT_CONNECTION_STRING=your-azure-ai-endpoint
MODEL_DEPLOYMENT_NAME=your-model-name
AGENT_ID=your-agent-id
```

### 2. Start the MCP Server

```sh
python simple-agent-mcp-server.py
```

This will start the server on `http://127.0.0.1:8000/sse`.

### 3. Run the MCP Client

```sh
python simple-client-mcp.py
```

The client will connect to the server, list available tools, and demonstrate calling the `add` and `invoke_agent` tools.

## File Overview

- `simple-agent-mcp-server.py`: Main MCP server exposing tools and agent invocation.
- `simple-client-mcp.py`: Example client for interacting with the server.

## Example Output

```
Available tools: ['add', 'invoke_agent']
Result: 8
Agent response: Paris
```

## License

See [LICENSE.md](LICENSE.md) for license information.