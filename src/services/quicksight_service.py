"""
QuickSight Service - AWS QuickSight integration for dashboard and analysis management.

This service provides functions to create, update, and manage QuickSight analyses
and dashboards through the AWS SDK. Handles permissions and error management.
"""

import boto3
from typing import Dict, Any
from botocore.exceptions import ClientError
import json





def create_analysis(visual_definition: Dict[str, Any], name: str,analysis_id: str) -> Dict[str, Any]:
    """
    Create a QuickSight analysis from a visual definition.
    
    Args:
        visual_definition: JSON definition containing the visualization structure
        name: Display name for the analysis
        analysis_id: Unique identifier for the analysis
    
    Returns:
        Dict containing status and response from AWS
    """

    print(f"\n✅ Creating analysis: {analysis_id}\n")
    try :
        client = boto3.client('quicksight')
        response = client.create_analysis(
            AwsAccountId = '817491136527',
            Name = name,
            AnalysisId = analysis_id,
            Definition = visual_definition["Definition"]
        )
        print(f"\n✅ Analysis creation status: {response}\n")
        return {"status": "success", "response": response}
    except Exception as e:
        print(f"\n❌ Error creating analysis: {e}\n")
        return {"status": "error", "response": str(e)}
    
def create_dashboard(dashboard_definition: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a simple test dashboard in QuickSight
    """
    try:
        client = boto3.client('quicksight')
        
        response = client.create_dashboard(
            AwsAccountId = '817491136527',
            Name = "test-dashboard-1",
            DashboardId = "test-dashboard-1",
            Definition = dashboard_definition
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "response": str(e)}

def get_available_analyses() -> Dict[str, Any]:
    """
    Get the list of available analyses
    """
    client = boto3.client('quicksight')
    response = client.list_analyses(
        AwsAccountId = '817491136527'
    )
    return response

def update_analysis_permissions(analysis_id: str) -> Dict[str, Any]:
    """
    Update the permissions of an analysis for the user to be able to view the analysis.
    """

    grant_permissions = [
        {
            "Principal": "arn:aws:quicksight:us-west-2:817491136527:user/default/GD-AWS-USA-GD-AISummerCa-Dev-Private-PowerUser/jjesusavarimuth@godaddy.com",
            "Actions": [
                "quicksight:RestoreAnalysis",
                "quicksight:UpdateAnalysisPermissions", 
                "quicksight:DeleteAnalysis",
                "quicksight:QueryAnalysis",
                "quicksight:DescribeAnalysisPermissions",
                "quicksight:DescribeAnalysis",
                "quicksight:UpdateAnalysis"
            ]
        }
    ]
    client = boto3.client('quicksight')
    response = client.update_analysis_permissions(
        AwsAccountId = '817491136527',
        AnalysisId = analysis_id,
        GrantPermissions = grant_permissions
    )
    return response

def update_dashboard_permissions(dashboard_id: str) -> Dict[str, Any]:
    """
    Update the permissions of a dashboard for the user to be able to view the dashboard.
    """
    grant_permissions = [
        {
            "Principal": "arn:aws:quicksight:us-west-2:817491136527:user/default/GD-AWS-USA-GD-AISummerCa-Dev-Private-PowerUser/jjesusavarimuth@godaddy.com",
            "Actions": [
                "quicksight:UpdateDashboardPermissions", 
                "quicksight:DeleteDashboard",
                "quicksight:QueryDashboard",
                "quicksight:DescribeDashboardPermissions",
                "quicksight:DescribeDashboard",
                "quicksight:UpdateDashboard",
                "quicksight:ListDashboardVersions",
                "quicksight:UpdateDashboardPublishedVersion"
            ]
        }
    ]
    client = boto3.client('quicksight')
    response = client.update_dashboard_permissions(
        AwsAccountId = '817491136527',
        DashboardId = dashboard_id,
        GrantPermissions = grant_permissions
    )
    return response

def delete_analysis(analysis_id: str) -> Dict[str, Any]:
    """
    Delete an analysis
    """
    client = boto3.client('quicksight')
    response = client.delete_analysis(
        AwsAccountId = '817491136527',
        AnalysisId = analysis_id
    )
    return response

#This API action is supported only when the account has an active Capacity Pricing plan.
def generateEmbedUrlForAnonymousUser():
    try:
        client = boto3.client('quicksight')
        response = client.generate_embed_url_for_anonymous_user(
            AwsAccountId = '817491136527',
            Namespace = 'default',
            AuthorizedResourceArns = ['arn:aws:quicksight:us-west-2:817491136527:dashboard/test-dashboard-1'],
            ExperienceConfiguration = {
                "Dashboard": {
                    "InitialDashboardId": 'test-dashboard-1'
                }
            },
            SessionLifetimeInMinutes = 600
        )
            
        return {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type"},
            'body': json.dumps(response),
            'isBase64Encoded':  bool('false')
        }
    except ClientError as e:
        print(e)
        return "Error generating embeddedURL: " + str(e)