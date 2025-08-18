import boto3
from typing import Dict, Any
from botocore.exceptions import ClientError
import json

# For testing purposes - simplified valid QuickSight dashboard
test_dashboard_definition = {
    "Definition": {
        "Sheets": [
            {
                "SheetId": "sheet1",
                "Name": "Test Dashboard Sheet",
                "Visuals": [
                    {
                        "BarChartVisual": {
                            "VisualId": "visual1",
                            "Title": {
                                "FormatText": {
                                    "PlainText": "Test Bar Chart"
                                }
                            },
                            "ChartConfiguration": {
                                "FieldWells": {
                                    "BarChartAggregatedFieldWells": {
                                        "Category": [
                                            {
                                                "CategoricalDimensionField": {
                                                    "FieldId": "product_category",
                                                    "Column": {
                                                        "DataSetIdentifier": "4485d828-ce32-44bf-b38e-75fa8fcd571c",
                                                        "ColumnName": "category"
                                                    }
                                                }
                                            }
                                        ],
                                        "Values": [
                                            {
                                                "NumericalMeasureField": {
                                                    "FieldId": "total_revenue_generated",
                                                    "Column": {
                                                        "DataSetIdentifier": "4485d828-ce32-44bf-b38e-75fa8fcd571c",
                                                        "ColumnName": "item_total"
                                                    },
                                                    "AggregationFunction": {
                                                        "SimpleNumericalAggregation": "SUM"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        ],
        "DataSetIdentifierDeclarations": [
            {
                "DataSetArn": "arn:aws:quicksight:us-west-2:817491136527:dataset/4485d828-ce32-44bf-b38e-75fa8fcd571c",
                "Identifier": "4485d828-ce32-44bf-b38e-75fa8fcd571c"
            }
        ]
    }
}



def create_analysis(visual_definition: Dict[str, Any], name: str,analysis_id: str) -> Dict[str, Any]:
    """
    Visualize the dashboard definition in Quicksight
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
    
def create_dashboard() -> Dict[str, Any]:
    """
    Create a dashboard in Quicksight
    """
    client = boto3.client('quicksight')
    response = client.create_dashboard(
        AwsAccountId = '817491136527',
        Name = "test-dashboard-1",
        DashboardId = "test-dashboard-1",
        Definition = test_dashboard_definition["Definition"]
    )
    return response

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

def update_dashboard_permissions() -> Dict[str, Any]:
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
                "quicksight:UpdateDashboardPublishedVersion",
                "quicksight:GenerateEmbedUrlForRegisteredUser"
            ]
        }
    ]
    client = boto3.client('quicksight')
    response = client.update_dashboard_permissions(
        AwsAccountId = '817491136527',
        DashboardId = "test-dashboard-1",
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