import streamlit as st
import asyncio
import sys
import os
from pathlib import Path
import json
import ast

# Add the project root to Python path  
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents import Runner, SQLiteSession
from src.agents.coordinator_agent import coordinator_agent
import json
import ast

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
st.title("📊 Data Analysis & Visualization Assistant")
st.markdown("*Your AI assistant for digital fashion e-commerce data analysis and QuickSight visualization*")

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
        # Check if this message contains a JSON definition
        if message.get("is_json_definition", False):
            st.subheader("🎨 Dashboard Definition")
            try:
                # Parse and format the stored JSON
                if isinstance(message["content"], str):
                    try:
                        json_obj = json.loads(message["content"])
                    except json.JSONDecodeError:
                        json_obj = ast.literal_eval(message["content"])
                else:
                    json_obj = message["content"]
                
                # Display formatted JSON with line numbers
                st.code(json.dumps(json_obj, indent=2), language="json", line_numbers=True)
            except Exception as e:
                # Fallback to regular display
                st.code(message["content"], language="json")
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your e-commerce data..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from agent
    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            try:
                # Route the request through the coordinator agent (uses handoffs)
                response = asyncio.run(
                    Runner.run(coordinator_agent, prompt, session=st.session_state.agent_session)
                )
                
                assistant_response = response.final_output
                
                # Debug: Print first 200 chars of response
                print(f"DEBUG - Response preview: {assistant_response[:200]}...")
                
                # Check if response contains a JSON definition
                is_json_definition = False
                try:
                     # Clean the response and check if it's JSON
                     cleaned_response = assistant_response.strip()
                     
                     # Try to parse as JSON string first
                     if cleaned_response.startswith('{') and cleaned_response.endswith('}'):
                         is_json_definition = True
                         st.subheader("🎨 Dashboard Definition")
                         
                         # Parse and format the JSON properly
                         try:
                             # Try json.loads first (for proper JSON strings)
                             json_obj = json.loads(cleaned_response)
                         except json.JSONDecodeError:
                             # Fall back to ast.literal_eval (for Python dict strings)
                             json_obj = ast.literal_eval(cleaned_response)
                         
                         # Display formatted JSON in a full-width container
                         st.code(json.dumps(json_obj, indent=2), language="json", line_numbers=True)
                                 
                except Exception as e:
                    print(f"JSON parsing error: {e}")
                    # If JSON parsing fails, display as regular text
                    st.code(cleaned_response, language="text")
                
                # Only display as markdown if it's not a JSON definition
                if not is_json_definition:
                    st.markdown(assistant_response)
                
                # Store the response
                message_data = {
                    "role": "assistant", 
                    "content": assistant_response
                }
                
                # Mark if this message contains a JSON definition for proper display
                if is_json_definition:
                    message_data["is_json_definition"] = True
                
                # Optional: basic SQL extraction if present
                if "```sql" in assistant_response.lower():
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

# The coordinator_agent will manage visualization and QuickSight handoffs within the conversation.

# Footer
st.markdown("---")

