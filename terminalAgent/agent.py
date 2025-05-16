# ./adk_agent_samples/mcp_agent/agent.py
import asyncio, os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
from google.adk.tools.agent_tool import AgentTool
# Load environment variables from .env file in the parent directory
load_dotenv()

# Define root_agent at module level for the ADK CLI to find
root_agent = None

# Initialize the agent and tools synchronously for the CLI to use
def init_agent():
    global root_agent
    
    # Create a simple non-MCP agent initially
    # This will be replaced with the MCP agent when async initialization is complete
    root_agent = LlmAgent(
        model=os.getenv("MODEL", "gemini-2.0-flash-lite"),
        name='terminal_command_analyzer_executor_agent',
        instruction=(
          'Setup the session as per existing context and execute the command'
        ),
        tools=[],  # Empty tools list initially
    )
    
    # Start async initialization in background
    asyncio.create_task(init_agent_async())
    
    return root_agent

async def init_agent_async():
    global root_agent
    
    # Get MCP tools
    try:
        tools, exit_stack = await get_tools_async()
        print(f"Fetched {len(tools)} tools from MCP server.")
        
        # Update the existing agent with tools
        root_agent.tools = tools
        
        # Store exit_stack in module to prevent garbage collection
        # Note: This needs proper cleanup strategy in production
        global _exit_stack
        _exit_stack = exit_stack
        
    except Exception as e:
        print(f"Error initializing MCP tools: {e}")
command = 'npx'
args = ["iterm_mcp_server"]
env = {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN"), 
       "GITHUB_TOOLSETS":"all"}
# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    """Gets tools from the File System MCP Server."""
    print("Attempting to connect to MCP Filesystem server...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
                    command=command,
                    args=args,
                    # env=env
                )
        )
    print("MCP Toolset created successfully.")
    return tools, exit_stack

# --- Step 2: Agent Definition ---
async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")
    agent = LlmAgent(
        model='gemini-2.0-flash',
      name='terminal_command_analyzer_executor_agent',
        instruction=(
          'Setup the session as per existing context, analyze and execute the command'
        ),
        tools=[tools],
    )
    return agent, exit_stack

# Initialize the agent
init_agent()

# --- Step 3: Main Execution Logic ---
async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name='git_app', user_id='ksarma'
    )

    query = "list files"
    print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    agent, exit_stack = await get_agent_async()

    runner = Runner(
        app_name='git_app',
        agent=agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print(f"Event received: {event}")

    print("Closing MCP server connection...")
    await exit_stack.aclose()
    print("Cleanup complete.")

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")