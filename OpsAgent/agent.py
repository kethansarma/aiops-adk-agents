from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import transfer_to_agent_tool
from gitAgent import gitagent
from kubeAgent import agent
from fileAgent import fileagent
from terminalAgent import terminal_agent as terminalagent
import os




git_terminal_agent = Agent(
    model=os.getenv("MODEL", "gemini-2.0-flash-lite"),
    name='git_and_terminal_agent',
    description='A helpful assistant for devops tasks',
    instruction='''
    - Ask for the context folder
    - Set the context for all sub agents 
    - If the task is listed to git_agent, use the git agent
    - Else confirm the command with the user and execute it using the terminal agent''',
    # tools=[AgentTool(agent=agent.root_agent), AgentTool(agent=gh_agent.root_agent), AgentTool(agent=fileagent.root_agent)],
    # tools=[AgentTool(agent=terminalagent.root_agent)],
    sub_agents=[gitagent.root_agent,
                terminalagent.root_agent],  # Include the AgentTool
)

root_agent = Agent(
    model=os.getenv("MODEL", "gemini-2.0-flash-lite"),
    name='ops_agent',
    description='A helpful assistant for devops tasks',
    instruction='''
    - You are a helpful assistant for devops tasks
    - You have git agent for git tasks, terminal agent for command tasks, kubernetes agent for kubernetes tasks and file agent for all file related tasks to help you
    - You have github cli utility to work with tasks pull request.
    - Consider the user question. Infer if there are any folder directory context. If not Ask for the context folder
    - Set the folder context for all agents.
    - Arrive at relevant agent from tools list, description and instructions 
    - execute within the available context without too many questions.
    - you have git_terminal_agent for git tasks, kubernetes agent for kubernetes tasks and file agent for all file related tasks to help you
    - If agents cannot do the task check if it can be done using commandline tools.
    - Create a command, get confirmation and execute with git_terminal_agent tasks.
    - You have github cli utility to work with tasks pull request.''',
    # tools=[AgentTool(agent=agent.root_agent), AgentTool(agent=gh_agent.root_agent), AgentTool(agent=fileagent.root_agent)],
    # tools=[AgentTool(agent=terminalagent.root_agent)],
    sub_agents=[git_terminal_agent, agent.root_agent, fileagent.root_agent])