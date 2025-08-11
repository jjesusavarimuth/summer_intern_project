import streamlit as st
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path  
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents import Runner, SQLiteSession
from src.agents.data_insights_agent import data_insights_agent
from src.agents.data_visualizer_agent import data_visualizer_agent
import json

# Page configuration
st.set_page_config(
    page_title="Data Insights Assistant",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_session" not in st.session_state:
    # Initialize SQLite session for conversation history
    st.session_state.agent_session = SQLiteSession("streamlit_session")

# Title and description
st.title("📊 Data Insights Assistant")
st.markdown("*Your AI assistant for digital fashion e-commerce data analysis*")

# Sidebar for options
with st.sidebar:
    st.header("🛠️ Options")
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.agent_session = SQLiteSession("streamlit_session_new")
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Sample Questions")
    st.markdown("- What are the top performing products in terms of revenue?")
    st.markdown("- Compare revenue by product category?")
    st.markdown("- Which campaigns generated the most revenue?")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        #Display additional data if present
        # if "sql" in message and message["sql"]:
        #     st.code(message["sql"], language="sql")
        
        if "visualization" in message and message["visualization"]:
            st.json(message["visualization"])

# Chat input
if prompt := st.chat_input("Ask me about your e-commerce data..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your data..."):
            try:
                # Run the data insights agent
                response = asyncio.run(
                    Runner.run(data_insights_agent, prompt, session=st.session_state.agent_session)
                )
                
                assistant_response = response.final_output
                st.markdown(assistant_response)
                
                # Store the response
                message_data = {
                    "role": "assistant", 
                    "content": assistant_response
                }
                
                # Check if response contains SQL (basic parsing)
                if "```sql" in assistant_response.lower():
                    # Extract SQL from markdown code block
                    sql_start = assistant_response.lower().find("```sql") + 6
                    sql_end = assistant_response.find("```", sql_start)
                    if sql_end != -1:
                        sql_query = assistant_response[sql_start:sql_end].strip()
                        message_data["sql"] = sql_query
                
                st.session_state.messages.append(message_data)
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# Visualization section
if len(st.session_state.messages) > 0:
    last_message = st.session_state.messages[-1]
    if (last_message["role"] == "assistant" and 
        "visualization" in last_message.get("content", "").lower()):
        
        st.markdown("---")
        st.subheader("📊 Create Visualization")
        
        if st.button("Generate Dashboard Definition"):
            with st.spinner("Creating dashboard definition..."):
                try:
                    # Get the last data query and response
                    context = f"User Question: {st.session_state.messages[-2]['content']}\n"
                    context += f"Data Response: {last_message['content']}"
                    
                    # Run dashboard generator
                    viz_response = asyncio.run(
                        Runner.run(data_visualizer_agent, context)
                    )
                    
                    st.subheader("🎨 Dashboard Definition")
                    st.code(viz_response.final_output, language="json")
                    
                    # Try to parse and display as JSON
                    try:
                        json_data = json.loads(viz_response.final_output)
                        st.json(json_data)
                    except:
                        st.info("Dashboard definition generated (not valid JSON format)")
                        
                except Exception as e:
                    st.error(f"Error generating visualization: {str(e)}")

# Footer
st.markdown("---")
