"""
Data Analysis & Visualization Assistant - Streamlit UI

This module provides a web-based interface for the AI-powered data analysis and 
visualization assistant. It handles user interactions, agent coordination, and 
displays results including SQL queries, insights, and QuickSight dashboard definitions.

Features:
- Chat interface for natural language queries
- Real-time agent processing with visual feedback
- Formatted display of JSON dashboard definitions
- Conversation history management
- Integration with coordinator agent for task delegation
"""

import streamlit as st
import asyncio
import sys
import os
from pathlib import Path
import json
import ast

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import agent framework and coordinator
from agents import Runner, SQLiteSession
from src.agents.coordinator_agent import coordinator_agent

# ========================================
# STREAMLIT PAGE CONFIGURATION
# ========================================

# Configure page settings for optimal display
st.set_page_config(
    page_title="Data Insights Assistant",
    page_icon="📊",
    layout="wide"  # Use full width for better JSON display
)

# ========================================
# SESSION STATE INITIALIZATION
# ========================================

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize agent session for conversation persistence
if "agent_session" not in st.session_state:
    # SQLite session stores conversation context across interactions
    st.session_state.agent_session = SQLiteSession("streamlit_session")

# ========================================
# PAGE HEADER AND TITLE
# ========================================

st.title("📊 Data Analysis & Visualization Assistant")
st.markdown("*Your AI assistant for data analysis and QuickSight visualization*")

# ========================================
# SIDEBAR CONFIGURATION
# ========================================

with st.sidebar:
    st.header("🛠️ Options")
    
    # Reset conversation and start fresh
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        # Create new session to avoid context carryover
        st.session_state.agent_session = SQLiteSession("streamlit_session_new")
        st.rerun()
    
    st.markdown("---")
    
    # Provide example queries to help users get started
    st.markdown("### 💡 Sample E-commerce Questions")
    st.markdown("- What are the top performing products in terms of revenue?")
    st.markdown("- Compare revenue by product category?")
    st.markdown("---")
    st.markdown("### 💡 Sample BU Scorecard Questions")
    st.markdown("- Compare targets and actuals for OpEx Costs from Care & Services in March 2024.")
    st.markdown("- Compare actuals for OpEx Costs from Care & Services YOY comparing March 2024 and March 2025.")
    st.markdown("- What are the top performing metrics for the USI business unit?")
    
    # 

# ========================================
# CHAT MESSAGE DISPLAY
# ========================================

# Display conversation history with proper formatting
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Handle JSON dashboard definitions with special formatting
        if message.get("is_json_definition", False):
            st.subheader("🎨 Dashboard Definition")
            try:
                # Parse stored JSON content (handles both string and dict formats)
                if isinstance(message["content"], str):
                    try:
                        # Try standard JSON parsing first
                        json_obj = json.loads(message["content"])
                    except json.JSONDecodeError:
                        # Fallback to Python literal evaluation
                        json_obj = ast.literal_eval(message["content"])
                else:
                    json_obj = message["content"]
                
                # Display formatted JSON with syntax highlighting and line numbers
                st.code(json.dumps(json_obj, indent=2), language="json", line_numbers=True)
            except Exception as e:
                # If parsing fails, display as plain JSON
                st.code(message["content"], language="json")
        else:
            # Display regular text/markdown messages
            st.markdown(message["content"])

# ========================================
# CHAT INPUT AND PROCESSING
# ========================================

# Main chat input handler
if prompt := st.chat_input("Ask me about your data..."):
    # Add user message to conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process user request through agent system
    with st.chat_message("assistant"):
        with st.spinner("Processing your request..."):
            try:
                # Route request through coordinator agent which handles task delegation
                # The coordinator decides whether to use data insights or visualization agents
                response = asyncio.run(
                    Runner.run(coordinator_agent, prompt, session=st.session_state.agent_session)
                )
                
                assistant_response = response.final_output
                
                # Debug logging for development/troubleshooting
                print(f"DEBUG - Response preview: {assistant_response[:200]}...")
                
                # ========================================
                # RESPONSE PROCESSING AND FORMATTING
                # ========================================
                
                # Check if response is a QuickSight JSON definition
                is_json_definition = False
                try:
                    cleaned_response = assistant_response.strip()
                    
                    # Detect JSON responses by checking structure
                    if cleaned_response.startswith('{') and cleaned_response.endswith('}'):
                        is_json_definition = True
                        st.subheader("🎨 Dashboard Definition")
                        
                        # Parse and format JSON for better readability
                        try:
                            # Standard JSON parsing
                            json_obj = json.loads(cleaned_response)
                        except json.JSONDecodeError:
                            # Fallback for Python dict strings
                            json_obj = ast.literal_eval(cleaned_response)
                        
                        # Display formatted JSON with proper indentation and line numbers
                        st.code(json.dumps(json_obj, indent=2), language="json", line_numbers=True)
                                
                except Exception as e:
                    print(f"JSON parsing error: {e}")
                    # Fallback: display as plain text if JSON parsing fails
                    st.code(cleaned_response, language="text")
                
                # Display regular text responses (non-JSON)
                if not is_json_definition:
                    st.markdown(assistant_response)
                
                # ========================================
                # MESSAGE STORAGE AND METADATA
                # ========================================
                
                # Prepare message data for storage
                message_data = {
                    "role": "assistant", 
                    "content": assistant_response
                }
                
                # Mark JSON definitions for special display formatting
                if is_json_definition:
                    message_data["is_json_definition"] = True
                
                # Extract SQL queries for potential future use/display
                if "```sql" in assistant_response.lower():
                    sql_start = assistant_response.lower().find("```sql") + 6
                    sql_end = assistant_response.find("```", sql_start)
                    if sql_end != -1:
                        sql_query = assistant_response[sql_start:sql_end].strip()
                        message_data["sql"] = sql_query
                
                # Save to conversation history
                st.session_state.messages.append(message_data)
                
            except Exception as e:
                # Handle and display any processing errors
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# ========================================
# FOOTER AND FINAL NOTES
# ========================================

# Note: The coordinator_agent handles the routing between different specialized agents:
# - data_insights_agent: For data analysis and SQL queries
# - visual_coordinator_agent: For creating QuickSight visualizations
# This architecture allows for flexible task delegation based on user intent.

# Page footer separator
st.markdown("---")

