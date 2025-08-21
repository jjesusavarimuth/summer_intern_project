"""
Agent Memory - Shared memory system for multi-agent conversations.

This module provides a centralized memory store that allows agents to share
context, query results, and visualization definitions across interactions.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
import json

@dataclass
class AgentMemory:
    """
    Centralized memory store for agent interactions and workflow state.
    
    Maintains conversation context, data insights, visualization plans,
    and QuickSight configuration across multiple agent interactions.
    """
    
    # session context - list of user/agent interactions
    data_insights_context: Optional[List[Dict[str, Any]]] = None
    context: Optional[List[Dict[str, Any]]] = None
    has_direct_sql_query: Optional[bool] = False
    
    # Data Visualizer Agent outputs  
    visualization_plan: Optional[str] = None
    json_visual_definition: Optional[Dict[str, Any]] = None
    
    # QuickSight Agent outputs
    quicksight_analysis_id: Optional[str] = None
    quicksight_analysis_name: Optional[str] = None
    create_analysis: Optional[bool] = False
    update_analysis: Optional[bool] = False
    list_analyses: Optional[bool] = False
    
    # User context
    original_user_query: Optional[str] = None
    has_visualization_plan: Optional[bool] = False
    has_json_visual_definition: Optional[bool] = False


    
    def add_data_insights_context_pair(self, user_message: str, agent_response: str):
        """Add a complete user/agent interaction pair"""
        if self.data_insights_context is None:
            self.data_insights_context = []
        self.data_insights_context.append({"user": user_message, "agent": agent_response})
    
    def set_has_direct_sql_query(self, has_direct_sql_query: bool):
        """Set has_direct_sql_query"""
        self.has_direct_sql_query = has_direct_sql_query
        
    def set_visualization_plan(self, visualization_plan: str):
        """Set visualization plan"""
        self.visualization_plan = visualization_plan

    def set_json_visual_definition(self, json_visual_definition: Dict[str, Any]):
        """Set json visual definition"""
        self.json_visual_definition = json_visual_definition
    
    def set_quicksight_analysis_name(self, analysis_name: str):
        """Store results from QuickSight agent"""
        self.quicksight_analysis_name = analysis_name
    
    def set_quicksight_analysis_id(self, analysis_id: str):
        """Store results from QuickSight agent"""
        self.quicksight_analysis_id = analysis_id

    def set_has_visualization_plan(self, has_visualization_plan: bool):
        """Set has_visualization_plan"""
        self.has_visualization_plan = has_visualization_plan
    
    def set_has_json_visual_definition(self, has_json_visual_definition: bool):
        """Set has_json_visual_definition"""
        self.has_json_visual_definition = has_json_visual_definition

    def set_create_analysis(self, create_analysis: bool):
        """Set create_analysis"""
        self.create_analysis = create_analysis

    def set_list_analyses(self, list_analyses: bool):
        """Set list_analyses"""
        self.list_analyses = list_analyses
    
    def set_update_analysis(self, update_analysis: bool):
        """Set update_analysis"""
        self.update_analysis = update_analysis

    def get_data_insights_context(self) -> List[Dict[str, str]]:
        """Get the session context as list of user/agent pairs"""
        return self.data_insights_context or []
    
    def get_data_insights_context_as_string(self) -> str:
        """Get the context formatted as a readable string"""
        if not self.data_insights_context:
            return ""
        
        formatted_context = []
        for interaction in self.data_insights_context:
            if interaction["user"]:
                formatted_context.append(f"\nUser: {interaction['user']}\n")
            if interaction["agent"]:
                formatted_context.append(f"\nAgent: {interaction['agent']}\n")
        
        return "\n".join(formatted_context)
        
    def get_has_direct_sql_query(self) -> bool:
        """Get has_direct_sql_query"""
        return self.has_direct_sql_query

    def get_quicksight_analysis_name(self) -> str:
        """Get quicksight_analysis_name"""
        return self.quicksight_analysis_name
    
    def get_quicksight_analysis_id(self) -> str:
        """Get quicksight_analysis_id"""
        return self.quicksight_analysis_id

    def get_visualization_plan(self) -> str:
        """Get visualization plan"""
        return self.visualization_plan
    
    def get_json_visual_definition(self) -> Dict[str, Any]:
        """Get json visual definition"""
        return self.json_visual_definition

    
    def get_has_visualization_plan(self) -> bool:
        """Check if visualization results are available"""
        return bool(self.has_visualization_plan)
    
    def get_has_json_visual_definition(self) -> bool:
        """Check if JSON visual definition is available"""
        return bool(self.has_json_visual_definition)

    def get_create_analysis(self) -> bool:
        """Get create_analysis"""
        return self.create_analysis

    def get_update_analysis(self) -> bool:
        """Get update_analysis"""
        return self.update_analysis
    
    def get_list_analyses(self) -> bool:
        """Get list_analyses"""
        return self.list_analyses
    
    def reset_analysis_flags(self):
        """Reset analysis flags"""
        self.create_analysis = False
        self.update_analysis = False
        self.list_analyses = False

    def clear(self):
        """Clear all stored data"""
        self.context = None
        self.visualization_plan = None
        self.json_visual_definition = None
        self.quicksight_analysis_id = None
        self.quicksight_analysis_name = None

    
    def __str__(self) -> str:
        """String representation of memory contents"""
        context_summary = f"{len(self.data_insights_context)} interactions" if self.data_insights_context else "No context"
        return f"""AgentMemory:
- Context: {context_summary}
- Has Visualization Plan: {self.get_has_visualization_plan()}
- Has JSON Visual Definition: {self.get_has_json_visual_definition()}
- QuickSight Analysis: {self.quicksight_analysis_name} ({self.quicksight_analysis_id})
"""

# Global memory instance for the coordinator
AGENT_MEMORY = AgentMemory()