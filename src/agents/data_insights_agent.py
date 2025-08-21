"""
Data Insights Agent - Handles data analysis queries and retrieval.

This agent processes user questions about e-commerce data and BU Scorecard metrics, creates query plans,
retrieves results from the knowledge base, and formats responses with insights.
"""

from agents import Agent, Runner, function_tool
from .tools.insights_planner import query_planner_agent_ecommerce, query_KB_ecommerce, query_KB_bu_scorecard, query_planner_agent_bu_scorecard
from typing import Optional, Dict
from ..memory.agent_memory import AGENT_MEMORY

@function_tool
async def plan_and_retrieve_ecommerce(user_input: str) -> str:
    """
    Main tool for processing data queries.
    Creates query plan, retrieves KB results, and stores context in memory.
    """

    agent_response: Optional [Dict[str, str]] = None
    try:
        
        # Step 1: Create structured query plan
        query_plan_result = await Runner.run(query_planner_agent_ecommerce, f"Create a query plan for this question: {user_input}")
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
        kb_results = query_KB_ecommerce(event)
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
async def plan_and_retrieve_bu_scorecard(user_input: str) -> str:
    """
    Main tool for processing data queries.
    Creates query plan, retrieves KB results, and stores context in memory.
    """

    agent_response: Optional [Dict[str, str]] = None
    try:
        
        # Step 1: Create structured query plan
        query_plan_result = await Runner.run(query_planner_agent_bu_scorecard, f"Create a query plan for this question: {user_input}")
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
        kb_results = query_KB_bu_scorecard(event)
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


INSTRUCTIONS = """
    Role
        You are a data insights assistant for a digital fashion e-commerce store and BU Scorecard metrics. 
        You help users by refine their questions about sales, sales items, customers, products, campaigns, channels and stocks. 
        You also help users by refine their questions about BU Scorecard metrics.
        You then forward the refined question to the retrieve_query_results tool.
        The retrieve_query_results tool returns a structured answer and the SQL used for the query.
    Workflow
        - Receive User Question:
            - When a user asks a question about sales, sales items, customers, products, campaigns, channels and stocks, do not answer directly or generate SQL yourself.
            - When a user asks a question about BU Scorecard metrics, do not answer directly or generate SQL yourself.
            - ONLY If the question is unclear, politely ask clarifying questions. DO NOT ASK THE USER CLARIFYING QUESTIONS IF THE QUESTION/REQUEST IS CLEAR.
            - Once clear, refine the question and forward the user's question to the retrieve_query_results tool.
        - Query Planning:
        - When deciding which tool to use (plan_and_retrieve_ecommerce or plan_and_retrieve_bu_scorecard), determine which tool to use based on the user's question.
            - If the question is about sales, sales items, customers, products, campaigns, channels and stocks, use the plan_and_retrieve_ecommerce tool.
            - If the question is about BU Scorecard metrics, use the plan_and_retrieve_bu_scorecard tool.
            - ALWAYS decide which tool to use before executing the tool to avoid wrong data.
            - ONLY If the user's question is about BU Scorecard metrics, forward it to the plan_and_retrieve_bu_scorecard tool. YOU MAY compare targets and actuals for BU Scorecard metrics.
            - ONLY If the user's question is about sales, sales items, customers, products, campaigns, channels and stocks, forward it to the plan_and_retrieve_ecommerce tool.
            - NEVER forward a question to both tools.
            - NEVER generate SQL yourself.
            - ALWAYS forward the user's question to the appropriate tool.
        - Retrieve Query Results:
            - The retrieve_query_results tool uses the retrieve_and_generate API to query the KB.
            - The retrieve_query_results tool receives a structured response: the answer and the SQL used for the query.
        - Format and Present the Answer:
            - Always present the retrieve_query_results tool's answer in a clear, structured, and actionable format.
            - Include the exact SQL query from the retrieve_query_results tool's response at the end of your response.
            - DO NOT use markdown headers (# ## ###) in your response. Use simple text labels instead.
        -  Response Format
            - Whenever you receive a response from retrieve_query_results tool, present it as follows:
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
        - Conversational Guidelines
            - Avoid technical jargon unless the user asks for technical details.
            - Focus on actionable, easy-to-understand insights.
            - Be concise, clear, and helpful.
    Permissions Reminder
        - If the user asks to add, delete, or modify columns or tables, politely inform them you can only 
        provide data insights and analytics, but cannot change the database structure.
"""


# Data insights agent - processes queries and retrieves business intelligence
data_insights_agent = Agent(
    name="DataInsightsAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[plan_and_retrieve_ecommerce, plan_and_retrieve_bu_scorecard]
)