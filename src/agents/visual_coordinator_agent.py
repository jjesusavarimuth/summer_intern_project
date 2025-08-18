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
    Run the data visualizer agent to create visualization plans.
    Use this when no visualization plan exists in memory.
    """
    try : 
        required_context = AGENT_MEMORY.get_data_insights_context()
        print(f"\n🔍 Required context: {required_context} \n")
        
        # Extract SQL query from context for analysis
        if required_context and len(required_context) > 0:
            latest_context = required_context[-1]  # Get the most recent context
            if 'agent' in latest_context and isinstance(latest_context['agent'], dict):
                    sql_query = latest_context['agent'].get('sql', '')
                    sql_analyzer_result = await Runner.run(sql_analyzer_agent, f"Analyze this SQL query: {sql_query}")
                    print(f"\n🔍 SQL analyzer result: {sql_analyzer_result} \n")
                    formatted_user_input = f"User request: {user_input}\nContext: {required_context}\nSQL analyzer result: {sql_analyzer_result}"
        else:
            print(f"\nNo SQL query found in context, proceeding without SQL analysis\n")
            print(f"\n Checking if the user's request has the SQL query\n")
            sql_analyzer_result = await Runner.run(sql_analyzer_agent, f"Analyze this SQL query: {user_input}")
            print(f"\n🔍 SQL analyzer result: {sql_analyzer_result} \n")
            formatted_user_input = f"User request: {user_input}\nSQL analyzer result: {sql_analyzer_result}"
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

    visualization_plan = AGENT_MEMORY.get_visualization_plan()
    try :
        json_definition = await Runner.run(visual_definition_generator, f"Prepare the json definition from the visualisation plan: {visualization_plan}")
        print(f"\n✅ Got JSON definition: {json_definition.final_output} \n")
        valid_json_definition = get_definition_json(json_definition.final_output)
        print(f"\n✅ Valid JSON definition: {valid_json_definition} \n")
        complete_json_definition = add_dataset_identifier(valid_json_definition)
        print(f"\n✅ Complete JSON definition: {complete_json_definition} \n")
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
    Run the quicksight agent to create a QuickSight analysis.
    Use this when the user wants to create a QuickSight analysis.
    """
    print(f"\n✅ Quicksight analysis called\n")
    await Runner.run(quicksight_agent, user_input)
    if AGENT_MEMORY.get_has_json_visual_definition():
        print(f"\n✅ Has JSON definition\n")
        json_visual_definition = AGENT_MEMORY.get_json_visual_definition()
        if AGENT_MEMORY.get_quicksight_analysis_name() is None:
            analysis_name = "test-analysis-2"
        else:
            analysis_name = AGENT_MEMORY.get_quicksight_analysis_name()
        analysis_id = analysis_name.strip()
        while ' ' in analysis_id:
            analysis_id = analysis_id.replace(' ', '')
        if AGENT_MEMORY.get_create_analysis():
            print(f"\n✅ Creating analysis\n")
            response = create_analysis(json_visual_definition, analysis_name, analysis_id)
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


INSTRUCTIONS = """
You are a Visual Coordinator Agent that manages the complete visualization workflow from planning to QuickSight analysis creation.

TASK: Your task is to analyze the user's request and decide which agent to call. 
REMEMBER: For a new analysis, you need to create a visualization plan first.

AVAILABLE TOOLS:
- run_visual_planner
- quicksight_analysis

TOOL USAGE:
- When the user wants to create a visualization :
    - ALWAYS FIRST CALL run_visual_planner with the user's request
    - RETURN EXACTLY what run_visual_planner returns (the JSON definition)
    - DO NOT ask questions or add commentary - just return the tool output
- ONLY When the user prompts to create a QuickSight analysis :
    - CHECK if the user has provided the name of the analysis in the user's request.
                - IF the user has provided the name of the analysis, THEN :
                    - CALL quicksight_analysis with the user's request including the name of the analysis.
                - IF the user has not provided the name of the analysis, THEN :
                    - MAKE a meaningful name for the analysis.
                    - CALL quicksight_analysis with the user's request including the name of the analysis you made.      
                    - RETURN EXACTLY what quicksight_analysis returns
- IF the user does not want to create a QuickSight analysis, THEN DO NOT CALL quicksight_analysis.

MANDATORY OUTPUT FORMAT:
- ALWAYS return EXACTLY the output from the tool call
- DO NOT add any commentary, questions, or additional text
- IF run_visual_planner is called: return the JSON definition
- IF quicksight_analysis is called: return the analysis status

"""

visual_coordinator_agent = Agent(
    name="Visual Coordinator Agent",
    model="gpt-4o-mini",
    instructions=INSTRUCTIONS,
    tools=[run_visual_planner, quicksight_analysis]
)