import boto3
from typing import Dict, Any





def create_analysis(visual_definition: Dict[str, Any], name: str,analysis_id: str) -> Dict[str, Any]:
    """
    Visualize the dashboard definition in Quicksight
    """
    # For testing purposes - simplified valid QuickSight dashboard
    test_dashboard = {
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
    # test_dashboard = {'Definition': {'Sheets': [{'SheetId': 'sheet1', 'Name': 'Sales Performance Overview', 'Visuals': [{'BarChartVisual': {'VisualId': 'visual1', 'Title': {'FormatText': {'PlainText': 'Total Items by Category'}}, 'Subtitle': {'FormatText': {'PlainText': 'Overview of items sold across categories'}}, 'ChartConfiguration': {'FieldWells': {'BarChartAggregatedFieldWells': {'Category': [{'CategoricalDimensionField': {'FieldId': 'category', 'Column': {'DataSetIdentifier': '4485d828-ce32-44bf-b38e-75fa8fcd571c', 'ColumnName': 'category'}}}], 'Values': [{'NumericalMeasureField': {'FieldId': 'item_total', 'Column': {'DataSetIdentifier': '4485d828-ce32-44bf-b38e-75fa8fcd571c', 'ColumnName': 'item_total'}, 'AggregationFunction': {'SimpleNumericalAggregation': 'SUM'}}}]}}, 'SortConfiguration': {'CategorySort': [{'FieldSort': {'FieldId': 'category', 'Direction': 'DESC'}}]}}}}]}], 'DataSetIdentifierDeclarations': [{'DataSetArn': 'arn:aws:quicksight:us-west-2:817491136527:dataset/4485d828-ce32-44bf-b38e-75fa8fcd571c', 'Identifier': '4485d828-ce32-44bf-b38e-75fa8fcd571c'}]}} 
    #strip any spaces from the name

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