"""
Coordinator Agent - Main routing agent for the data analysis system.

This agent acts as the central dispatcher, routing user requests to appropriate
specialized agents based on the intent (data analysis vs visualization).
"""

from agents import Agent, ModelSettings, function_tool, Runner
from .data_insights_agent import data_insights_agent
from .visual_coordinator_agent import visual_coordinator_agent





# Agent instructions defining routing logic and behavior
INSTRUCTIONS = """
You are a Main Coordinator Agent that routes user requests to the appropriate specialized agents via handoffs.

TOOLS:
- run_data_insights_agent: For getting data insights
- visual_coordinator_agent: For creating visualizations

TOOL USAGE:
- When the user wants to get data insights or to get answers to questions about the data :
    - HANDOFF to run_data_insights_agent
- When the user wants to visualize the data insights :
    - HANDOFF to visual_coordinator_agent

- OUTPUT FORMAT:
    - ALWAYS ONLY return the exact output of the tool call. DO NOT add any other text or comments or formatting.

"""

# Main coordinator agent - routes requests to specialized sub-agents
coordinator_agent = Agent(
    name="Coordinator Agent",
    model="gpt-4o-mini",
    instructions=INSTRUCTIONS,
    handoffs=[data_insights_agent, visual_coordinator_agent]
)
