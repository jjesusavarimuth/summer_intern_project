from agents import Agent, Runner, function_tool, WebSearchTool

INSTRUCTIONS = """
    You are a helpful web search assistant. 
    If the user input is not in English, use the translation_agent to translate it to English.
    Using the WebSearchTool, use the user's input or translated input as the query term.
    Give the result to the user.
"""

# Example using agent as tool
# If you want to create more function tools, create them in separate files for organization
# and import them to use them here.
@function_tool
async def translation_agent(user_input: str) -> str:
    """Translate the user's input to English"""
    translator = Agent(
        name="Translator",
        instructions="Translate the user's input to English",
        model="gpt-4o-mini",
    )
    translation = await Runner.run(translator, user_input)
    return translation.final_output

web_search_agent = Agent(
    name="WebSearchAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool(), translation_agent]
)