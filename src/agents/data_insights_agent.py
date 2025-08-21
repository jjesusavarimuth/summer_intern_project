"""
Data Insights Agent - Handles data analysis queries and retrieval.

This agent processes user questions about e-commerce data, creates query plans,
retrieves results from the knowledge base, and formats responses with insights.
"""

from agents import Agent, Runner, function_tool
from .tools.insights_planner import query_planner_agent, query_KB
from typing import Optional, Dict
from ..memory.agent_memory import AGENT_MEMORY

@function_tool
async def plan_and_retrieve(user_input: str) -> str:
    """
    Main tool for processing data queries.
    Creates query plan, retrieves KB results, and stores context in memory.
    """

    agent_response: Optional [Dict[str, str]] = None
    try:
        
        # Step 1: Create structured query plan
        query_plan_result = await Runner.run(query_planner_agent, f"Create a query plan for this question: {user_input}")
        query_plan = query_plan_result.final_output
        print(f"\n🔍 Query plan: {query_plan} \n")
        
        # Step 2: Combine question and plan for KB query
        combined_input = f""" Question: {user_input} Query Plan: {query_plan}"""
        
        # Step 3: Format request for knowledge base API
        event = {
            'requestBody': {
                'content': {
                    'application/json': {
                        'properties': [{'name': 'question', 'value': combined_input}]
                    }
                }
            }
        }
        
        # Step 4: Query knowledge base for results
        kb_results = query_KB(event)
        print(f"\n✅ Got KB results: {kb_results} \n")
        
        # Step 5: Store context and return results
        if kb_results['sql'] and kb_results['answer']:
            agent_response = {"query_plan": query_plan, "sql": kb_results['sql'], "insights": kb_results['answer']}
            AGENT_MEMORY.add_data_insights_context_pair(user_input, agent_response)
            
        return kb_results
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while retrieving data: {str(e)}."
        print(f"\n❌ Error in retrieve_query_results: {error_msg} \n")
        return error_msg

@function_tool
async def retrieve_results(user_input: str) -> str:
    """
    Retrieve the results from the knowledge base.
    """
    AGENT_MEMORY.set_has_direct_sql_query(True)
    try:
        event = {
            'requestBody': {
                'content': {
                    'application/json': {
                        'properties': [{'name': 'question', 'value': user_input}]
                    }
                }
            }
        }
        kb_results = query_KB(event)
        if kb_results['sql'] and kb_results['answer']:
            agent_response = {"sql": kb_results['sql'], "insights": kb_results['answer']}
            AGENT_MEMORY.add_data_insights_context_pair(user_input, agent_response)
        return kb_results
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while retrieving data: {str(e)}."
        print(f"\n❌ Error in retrieve_results: {error_msg} \n")
        return error_msg


INSTRUCTIONS = """
    Role
        You are a data insights assistant for a digital fashion e-commerce store. 
        You help users by refine their questions about sales, sales items, customers, products, campaigns,channels and stocks. 
        You then forward the user request to the appropriate function tool.
    Workflow
        - HANDLE USER REQUEST AND CALL THE APPROPRIATE TOOL:
            - When a user asks a question about sales, sales items, customers, products, campaigns, channels and stocks, do not answer directly or generate SQL yourself.
                - ONLY If the question is unclear, politely ask clarifying questions. DO NOT ASK THE USER CLARIFYING QUESTIONS IF THE QUESTION/REQUEST IS CLEAR.
                - Once clear, refine the question and forward the user's question to the plan_and_retrieve tool.
            - If the user's question is a direct SQL query, forward the question to the retrieve_results tool.
        - FORMAT AND PRESENT THE ANSWER:
            - Always present the plan_and_retrieve tool's answer in a clear, structured, and actionable format.
            - Include the exact SQL query from the plan_and_retrieve tool's response at the end of your response.
            - DO NOT use markdown headers (# ## ###) in your response. Use simple text labels instead.
        - RESPONSE FORMAT:
            - Whenever you receive a response from plan_and_retrieve tool or retrieve_results tool, present it as follows:
                - Summary: A concise answer to the user's question.
                - Key Findings: Bullet points or a numbered list of main insights.
                - Sample Data: (Optional) A small Markdown table if sample rows are part of the answer.
                - SQL Used: ALWAYS include the SQL query used in a markdown code block like this:
                ```sql
                [SQL query here]
                ```
                - Follow-Up Suggestion: Offer a related next step or question.
            - ALWAYS Suggest Visualization:
                - IN THE END, ALWAYS ask the user if they would like to see a visualization of the data.
        - CONVERSATIONAL GUIDELINES:
            - Avoid technical jargon unless the user asks for technical details.
            - Focus on actionable, easy-to-understand insights.
            - Be concise, clear, and helpful.
    PERMISSIONS REMINDER:
        - If the user asks to add, delete, or modify columns or tables, politely inform them you can only 
        provide data insights and analytics, but cannot change the database structure.
"""


# Data insights agent - processes queries and retrieves business intelligence
data_insights_agent = Agent(
    name="DataInsightsAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[plan_and_retrieve, retrieve_results]
)