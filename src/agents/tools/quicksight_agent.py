from agents import Agent, ModelSettings, function_tool
from ...memory.agent_memory import AGENT_MEMORY


@function_tool
def set_create_analysis(user_input: str):
    """Set create_analysis"""
    AGENT_MEMORY.set_create_analysis(True)
    AGENT_MEMORY.set_quicksight_analysis_name(user_input)

@function_tool
def set_update_analysis(user_input: str):
    """Set update_analysis"""
    AGENT_MEMORY.set_update_analysis(True)
    AGENT_MEMORY.set_quicksight_analysis_name(user_input)

@function_tool
def set_list_analyses():
    """Set list_analyses"""
    AGENT_MEMORY.set_list_analyses(True)

INSTRUCTIONS = """
Your role:
- is to set the create_analysis, update_analysis, list_analyses flags in the memory based on the user's request. 
- is to set the quicksight_analysis_name in the memory based on the exact name of the analysis the user provided in the user's request.

WORKFLOW:
1. analyze the user's request and see if the user wants to create or update an analysis.
2. If the user's request is to create an analysis, then :
    - call the set_create_analysis tool wit ONLY the exact name of the analysis the user provided in the user's request.
3. If the user's request is to update an analysis, then :
    - check if the user has provided the name of the analysis in the user's request.
    - if the user has provided the name of the analysis, then :
        - call the set_update_analysis tool with ONLY the exact name of the analysis the user provided in the user's request.
    - if the user has not provided the name of the analysis, then :
        - call the set_list_analyses tool
4. If the user's request is to list analyses, then :
    - call the set_list_analyses tool

"""

quicksight_agent = Agent(
    name="quicksight_agent",
    instructions=INSTRUCTIONS,
    model_settings=ModelSettings(tool_choice="required"),
    tools=[set_create_analysis, set_update_analysis, set_list_analyses],
)