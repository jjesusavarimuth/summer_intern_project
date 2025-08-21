"""
Visual Coordinator Agent - Manages the complete visualization workflow.

This agent orchestrates the creation of QuickSight visualizations by coordinating
between visual planning, JSON definition generation, and analysis creation.
"""

from agents import Agent, ModelSettings, function_tool, Runner
from .tools.visual_planner import visual_planner_agent
from .tools.visual_creator import visual_definition_generator, get_definition_json, add_dataset_identifier
from .tools.quicksight_agent import quicksight_agent
from ..memory.agent_memory import AGENT_MEMORY
from ..services.quicksight_service import create_analysis, get_available_analyses, update_analysis_permissions
from .tools.sql_analyzer import sql_analyzer_agent

@function_tool
async def run_visual_planner(user_input: str) -> str:
    """
    Creates visualization plan and generates complete JSON definition for QuickSight.
    
    Workflow: Context retrieval -> SQL analysis -> Visual planning -> JSON generation
    Returns: Complete JSON definition ready for QuickSight analysis creation
    """
    try : 
        # Step 1: Get data insights context from memory
        required_context = AGENT_MEMORY.get_data_insights_context()
        print(f"\n🔍 Required context: {required_context} \n")
        
        # Step 2: Extract and analyze SQL query for better visualization planning
        if required_context and len(required_context) > 0:
            latest_context = required_context[-1]  # Get the most recent context
            if 'agent' in latest_context and isinstance(latest_context['agent'], dict):
                    sql_query = latest_context['agent'].get('sql', '')
                    sql_analyzer_result = await Runner.run(sql_analyzer_agent, f"Analyze this SQL query: {sql_query}")
                    print(f"\n🔍 SQL analyzer result: {sql_analyzer_result} \n")
                    formatted_user_input = f"User request: {user_input}\nContext: {required_context}\nSQL analyzer result: {sql_analyzer_result}"
        else:
            # Fallback: analyze user input directly for SQL query
            print(f"\nNo SQL query found in context, proceeding without SQL analysis\n")
            print(f"\n Checking if the user's request has the SQL query\n")
            sql_analyzer_result = await Runner.run(sql_analyzer_agent, f"Analyze this SQL query: {user_input}")
            print(f"\n🔍 SQL analyzer result: {sql_analyzer_result} \n")
            formatted_user_input = f"User request: {user_input}\nSQL analyzer result: {sql_analyzer_result}"
        
        # Step 3: Generate visualization plan
        result = await Runner.run(visual_planner_agent, formatted_user_input)
        output = result.final_output
        AGENT_MEMORY.set_visualization_plan(output)
        AGENT_MEMORY.set_has_visualization_plan(True)
        print(f"\nVisualization plan: {AGENT_MEMORY.visualization_plan}\n")
        print(f"\nHas visualization plan: {AGENT_MEMORY.get_has_visualization_plan()}\n")
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while creating the visualization plan: {str(e)}."
        print(f"\n❌ Error creating visualization plan: {error_msg} \n")
        print(f"\n❌ User's request: {user_input} \n")
        return error_msg

    # Step 4: Convert visualization plan to QuickSight JSON definition
    visualization_plan = AGENT_MEMORY.get_visualization_plan()
    try :
        # Generate base JSON structure
        json_definition = await Runner.run(visual_definition_generator, f"Prepare the json definition from the visualisation plan: {visualization_plan}")
        print(f"\n✅ Got JSON definition: {json_definition.final_output} \n")
        
        # Parse and validate JSON structure
        valid_json_definition = get_definition_json(json_definition.final_output)
        print(f"\n✅ Valid JSON definition: {valid_json_definition} \n")
        
        # Add required dataset identifiers for QuickSight
        complete_json_definition = add_dataset_identifier(valid_json_definition)
        print(f"\n✅ Complete JSON definition: {complete_json_definition} \n")
        
        # Store complete definition in memory
        output = complete_json_definition
        AGENT_MEMORY.set_json_visual_definition(output)
        AGENT_MEMORY.set_has_json_visual_definition(True)
        print(f"\nHas JSON definition: {AGENT_MEMORY.get_has_json_visual_definition()}\n")
        return output
    except Exception as e:
        error_msg = f"Sorry, I encountered an error while preparing the json definition: {str(e)}. This might be due to the visualisation plan or the json definition template."
        print(f"\n❌ Error preparing json definition: {error_msg} \n")
        print (f"\n❌ Visualisation plan: {visualization_plan} \n")
        return error_msg
    
  
@function_tool
async def quicksight_analysis(user_input: str) -> str:
    """
    Creates QuickSight analysis from stored JSON definition.
    
    Handles analysis creation, permission updates, and analysis listing
    based on flags set by the quicksight_agent.
    """
    print(f"\n✅ Quicksight analysis called\n")
    
    # Set analysis flags based on user request
    await Runner.run(quicksight_agent, user_input)
    
    # Check if JSON definition exists in memory
    if AGENT_MEMORY.get_has_json_visual_definition():
        print(f"\n✅ Has JSON definition\n")
        json_visual_definition = AGENT_MEMORY.get_json_visual_definition()
        
        # Determine analysis name (user-provided or default)
        if AGENT_MEMORY.get_quicksight_analysis_name() is None:
            analysis_name = "test-analysis-2"
        else:
            analysis_name = AGENT_MEMORY.get_quicksight_analysis_name()
        
        # Create valid analysis ID (no spaces)
        analysis_id = analysis_name.strip()
        while ' ' in analysis_id:
            analysis_id = analysis_id.replace(' ', '')
        
        # Execute requested action based on memory flags
        if AGENT_MEMORY.get_create_analysis():
            print(f"\n✅ Creating analysis\n")
            response = create_analysis(json_visual_definition, analysis_name, analysis_id)
            
            # Update permissions if analysis creation succeeded
            if(response.get("status") == "success"):
                perms_response = update_analysis_permissions(analysis_id)
                print(f"\n✅ Analysis permissions updated: {perms_response}\n")
            else:
                print(f"\n❌ Error creating analysis: {response}\n")
            
            AGENT_MEMORY.reset_analysis_flags()
            print(f"\n✅ Analysis creation status: {response}\n")
            return response
            
        elif AGENT_MEMORY.get_list_analyses():
            print(f"\n✅ Listing analyses\n")
            response = get_available_analyses()
            print(f"\n✅ Analysis list status: {response}\n")
            AGENT_MEMORY.reset_analysis_flags()
            return response
    else:
        return "There is no JSON definition to create a QuickSight analysis from. Do you want to create a visualization plan first?"


# Agent instructions defining workflow coordination logic
INSTRUCTIONS = """
You are a Visual Coordinator Agent that manages the complete visualization workflow from planning to QuickSight analysis creation.

TASK: Your task is to analyze the user's request and decide which agent to call. 
REMEMBER: For a new analysis, you need to create a visualization plan first.

AVAILABLE TOOLS:
- run_visual_planner
- quicksight_analysis

TOOL USAGE:
- When the user wants to create a visualization :
    - CALL run_visual_planner with the user's request
    - RETURN EXACTLY what run_visual_planner returns (the JSON definition)
    - DO NOT ask questions or add commentary - just return the tool output
- ONLY When the user prompts to create a QuickSight analysis :- CHECK if the user has provided the name of the analysis in the user's request.
    - IF the user has provided the name of the analysis, THEN :
        - CALL quicksight_analysis with the user's request including the name of the analysis.
    - IF the user has not provided the name of the analysis, THEN :
        - MAKE a meaningful name for the analysis.
        - CALL quicksight_analysis with the user's request including the name of the analysis you made.      
        - RETURN EXACTLY what quicksight_analysis returns
- IF the user has not created a visualization definition, THEN :
    - RETURN "There is no visualization definition to create a QuickSight analysis from. Do you want to create a visualization definition first?"
- IF the user does not want to create a QuickSight analysis, THEN DO NOT CALL quicksight_analysis.

MANDATORY OUTPUT FORMAT:
- ALWAYS return EXACTLY the output from the tool call
- DO NOT add any commentary, questions, or additional text
- IF run_visual_planner is called: return the JSON definition
- IF quicksight_analysis is called: return the analysis status

"""

# Visual coordinator agent - orchestrates the complete visualization workflow
visual_coordinator_agent = Agent(
    name="Visual Coordinator Agent",
    model="gpt-4o-mini",
    instructions=INSTRUCTIONS,
    tools=[run_visual_planner, quicksight_analysis]
)