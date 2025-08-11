from agents import Agent, Runner, function_tool
import boto3
import logging

client = boto3.client('bedrock-agent-runtime')

INSTRUCTIONS = """
    You are a database query planner. Analyze the user's question and create a query plan.
    
    DATABASE SCHEMA: 
    - public
        - dataset_fashion_store_sales (sale_id, channel, discounted, total_amount, start_date, customer_id, country)
        - dataset_fashion_store_customers (customer_id, country, age_range, signup_date)
        - dataset_fashion_store_stock (country, product_id, stock_quantity)
        - dataset_fashion_store_products (product_id, product_name, category, brand, color, size, catalog_price, cost_price, gender)
        - dataset_fashion_store_salesitems (item_id, sale_id, product_id, quantity, original_price, unit_price, discount_applied, discount_percent, discounted, item_total, sale_date, channel, channel_campaigns)
        - dataset_fashion_store_campaigns (campaign_id, campaign_name, start_date, end_date, channel, discount_type, discount_value)
        - dataset_fashion_store_channels (channel, description)
    
    Your task:
    1. Identify which tables, columns and the relationships between tables that need to be joined to answer the question
    3. summarize the plan into a samll paragraph and output ONLY the summary.
    4. DO NOT try to generate SQL query in your response.
"""

@function_tool
async def plan_and_retrieve(user_input: str) -> str:
    """Gets the results of a query from the knowledge base and structures the output"""
    query_planner_agent = Agent(
        name="QueryPlannerAgent",
        instructions= INSTRUCTIONS,
        model="gpt-4o-mini",
    )

    try:
        
        query_plan_result = await Runner.run(query_planner_agent, f"Create a query plan for this question: {user_input}")
        query_plan = query_plan_result.final_output
        print(f"\n🔍 Query plan: {query_plan} \n")
        # Combine question and query plan into a single input for the knowledge base
        combined_input = f""" Question: {user_input} Query Plan: {query_plan}"""
        
        # Get raw results from knowledge base
        event = {
            'requestBody': {
                'content': {
                    'application/json': {
                        'properties': [{'name': 'question', 'value': combined_input}]
                    }
                }
            }
        }
        
        
        kb_results = query_KB(event)
        print(f"\n✅ Got KB results: {kb_results} \n")
        
        # Check if there's an error in the KB results  
        if isinstance(kb_results, dict) and 'error' in kb_results:
            return f"Sorry, I couldn't retrieve data from the knowledge base: {kb_results['error']}"
        
        return kb_results
        
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while retrieving data: {str(e)}. This might be due to AWS credential issues."
        print(f"\n❌ Error in retrieve_query_results: {error_msg} \n")
        return error_msg


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def query_KB(event):
    try:
        # question  = event['question']
        question = None
        try:
            props = event['requestBody']['content']['application/json']['properties']
            for prop in props:
                if prop.get('name') == 'question':
                    question = prop.get('value')
                    break
        except Exception as ex:
            logger.error(f"Failed to extract user question from requestBody: {ex}")   
        if not question:
            return {"error": "No question provided in the request."}    
        
        response = client.retrieve_and_generate(
            input={'text': question},
            retrieveAndGenerateConfiguration={
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'QCQ10YU9FE',
                    'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0'
                },
                'type': 'KNOWLEDGE_BASE'
            }
        )
        answer = response['output']['text']
        sql_query = None
        for citation in response.get('citations', []):
            for ref in citation.get('retrievedReferences', []):
                sql_loc = ref.get('location', {}).get('sqlLocation')
                if sql_loc and 'query' in sql_loc:
                    sql_query = sql_loc['query']
        return {
            "answer": answer,
            "sql": sql_query
        }
    except Exception as e:
        logger.error(f"Error in query_KB: {str(e)}")
        raise