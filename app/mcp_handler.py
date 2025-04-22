# app/mcp_handler.py

import os
import requests
from dotenv import load_dotenv
from app.db import execute_sql_query
from agents_mcp import Agent, RunnerContext  # We'll load MCP config from the YAML file
from agents import Runner, function_tool     # Use the function_tool decorator to register tools
from agents.mcp import MCPServer, MCPServerStdio

load_dotenv()


@function_tool
def sql_executor(query: str) -> str:
    """
    Executes a SQL query on the PostgreSQL database and returns the result as a string.
    Use this tool when you need to query the database.
    Args:
        query: The SQL query string to execute.
    """
    print(f"Executing SQL Tool with query: {query}")
    try:
        result = execute_sql_query(query)
        response = str(result)
        print(f"SQL Result: {response}")
        return response
    except Exception as e:
        error_message = f"SQL Execution Error: {str(e)}"
        print(error_message)
        return error_message


@function_tool
def weather_api(location: str) -> str:
    """
    Calls a public weather API (wttr.in) to get current weather information for the given location.
    Use this tool when you need to retrieve weather data.
    Args:
        location: The location for which to get the current weather.
    """
    print(f"Calling Weather API for location: {location}")
    try:
        url = f"http://wttr.in/{location}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            weather_info = response.text
            print(f"Weather API Response: {weather_info}")
            return weather_info
        else:
            error_message = f"Weather API error: {response.status_code}"
            print(error_message)
            return error_message
    except Exception as e:
        error_message = f"Weather API Execution Error: {str(e)}"
        print(error_message)
        return error_message


async def handle_conversation(user_input: str) -> str:
    """
    Constructs and runs an MCP-enabled agent that uses both the SQL tool and the weather_api tool,
    along with external MCP servers loaded from the YAML configuration, to answer the user's query.
    """
    instructions = (
        "You are a helpful assistant with access to MCP tools. "
        #"When you need to query structured data from a SQL database, use the 'sql_executor' tool. "
        #"When asked for weather information, use the 'weather_api' tool. "
        "You may also use external MCP tools (such as 'fetch' or 'filesystem') as needed. "
        "Use the tools to read the filesystem and answer questions based on those files"
        f"The user has asked: {user_input}"
    )

    # Create the MCP-enabled agent with our registered tools.
    agent = Agent(
        name="MCP Agent",
        instructions=instructions,
        mcp_servers=[MCPServer],
        #tools=[sql_executor, weather_api]
    )

    # Create the RunnerContext and load MCP configuration from the YAML file.
    context = RunnerContext(mcp_config_path="mcp_agent.config.yaml")

    try:
        print(f"Running agent for user input: {user_input}")
        # Run the agent with the given input.
        result = await Runner.run(starting_agent=agent, input=user_input, context=context)

        # Handle the final response by checking common attributes.
        if hasattr(result, 'response') and hasattr(result.response, 'value'):
            final_response = result.response.value
        elif hasattr(result, 'output'):
            final_response = result.output
        elif hasattr(result, 'final_output'):
            final_response = result.final_output
        else:
            final_response = str(result)

        print(f"Agent finished. Response: {final_response}")
        return final_response

    except Exception as e:
        print(f"Error during agent run: {str(e)}")
        return f"❌ Error running agent: {str(e)}"
