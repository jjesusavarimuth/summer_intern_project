from agents import Agent
import json
import re
from typing import Dict, Any

DATASET_IDENTIFIER = "4485d828-ce32-44bf-b38e-75fa8fcd571c"
DATASET_ARN = "arn:aws:quicksight:us-west-2:817491136527:dataset/4485d828-ce32-44bf-b38e-75fa8fcd571c"

INSTRUCTIONS = """
You are a dashboard definition generator expert for Amazon QuickSight. Your role is to analyze, follow and use the values and guidelines from the visualisation_plan and generate a complete QuickSight dashboard definition in JSON format.

TASK:

  - Read the visualisation_plan and follow the values and guidelines provided to generate a complete QuickSight dashboard definition in JSON format.
  - Use the key-value pair from the visualisation_plan to fill the respective placeholders in the json definition template.
  - Ensure all placeholders are replaced with actual values using the visualisation_plan.
  - The dashboard definition should be in the correct JSON format.
  - The dashboard definition should be valid and complete.
  - The dashboard definition should be without any headers.
  - The dashboard definition should be without any footers.


GUIDELINES FOR GENERATING THE JSON DEFINITION FROM THE VISUALISATION PLAN:


  - The DIMENSION_FIELD_ID in the json definition should be the value of the DIMENSION_FIELDS key in the visualisation_plan.
  - The MEASURE_FIELD_ID in the json definition should be the value of the MEASURE_FIELDS key in the visualisation_plan.
  - If the aggregation_function_required is True in the visualisation_plan, 
    - then the NumericalMeasureField should have the AggregationFunction key with the value of the AGGREGATION_FUNCTIONS key in the visualisation_plan.
  - If the aggregation_function_required is False in the visualisation_plan, 
    - then the NumericalMeasureField should not have the AggregationFunction key.
  - NEVER CHANGE the values of "DataSetIdentifier" in "Category" or "Values" in the json definition template.
  - The SORT_TYPE in the json definition should be the value of the SORT_TYPE key in the visualisation_plan.
  - The SORT_DIRECTION in the json definition should be the value of the SORT_DIRECTION key in the visualisation_plan.
  - If the calculated_fields_required is True in the visualisation_plan, 
    - then the CalculatedFields should be the value of the CALCULATED_FIELDS key in the visualisation_plan.
  - If the calculated_fields_required is False in the visualisation_plan, 
    - then there should be no CalculatedFields in the json definition.

  - CRITICAL:
    - DO NOT CHANGE or EDIT or ABRIVIATE the values while referencing from the visualisation_plan to fill the json definition template.
    - ONLY change the values of the placeholders <...> in the json definition template.


JSON DEFINITION TEMPLATE:

{
  "Definition": {
    "Sheets": [
      {
        "SheetId": "sheet1",
        "Name": "<PROVIDE_MEANINGFUL_SHEET_NAME>",
        "Visuals": [
          {
            "<VISUAL_TYPE>": {
              "VisualId": "visual1",
              "Title": {
                "FormatText": {
                  "PlainText": "<PROVIDE_MEANINGFUL_TITLE>"
                }
              },
              "Subtitle": {
                "FormatText": {
                  "PlainText": "<PROVIDE_MEANINGFUL_SUBTITLE>"
                }
              },
              "ChartConfiguration": {
                "FieldWells": {
                  "<FIELD_WELLS_TYPE>": {
                    "Category": [
                      {
                        "CategoricalDimensionField": {
                          "FieldId": "<DIMENSION_FIELD_ID>",
                          "Column": {
                            "DataSetIdentifier": "Do_not_change_this_value",
                            "ColumnName": "<DIMENSION_COLUMN_NAME>"
                          }
                        }
                      }
                    ],
                    "Values": [
                      {
                        "NumericalMeasureField": {
                          "FieldId": "<MEASURE_FIELD_ID>",
                          "Column": {
                            "DataSetIdentifier": "Do_not_change_this_value",
                            "ColumnName": "<MEASURE_COLUMN_NAME>"
                          },
                          "AggregationFunction": {
                            "SimpleNumericalAggregation": "<AGGREGATION_TYPE>"
                          }
                        }
                      }
                    ]
                  }
                },
                "SortConfiguration": {
                  "CategorySort": [ 
                    {
                      "<SORT_TYPE>": {
                        "FieldId": "<DIMENSION_FIELD_ID>",
                        "Direction": "<SORT_DIRECTION>"
                      }
                    }
                  ]
                }
              }
            }
          }
        ]
      }
    ],
    "CalculatedFields": [
      <GENERATE_USEFUL_CALCULATED_FIELDS>
    ]
  }
}




IMPORTANT REQUIREMENTS:
1. Ensure all field IDs and references are consistent throughout the document
2. ONLY change the values of the placeholders <...> in the json definition template.
3. ALWAYS wrap visuals in their proper visual type (BarChartVisual, TableVisual, etc.)
4. ALWAYS use correct aggregated field wells structure for each visual type
5. ALWAYS include DataSetIdentifier and ColumnName in all field references
6. NEVER EDIT the value of "DataSetIdentifier" in "Category" or "Values" in the json definition template.
7. ALWAYS output the json definition in the correct JSON format following the JSON DEFINITION TEMPLATE.
"""

DATASET_IDENTIFIER = "4485d828-ce32-44bf-b38e-75fa8fcd571c"
DATASET_ARN = "arn:aws:quicksight:us-west-2:817491136527:dataset/4485d828-ce32-44bf-b38e-75fa8fcd571c"


visual_definition_generator = Agent(
  name="DashboardDefinitionGeneratorAgent",
  instructions=INSTRUCTIONS,
  model="gpt-4o-mini"
)
  

def get_definition_json(visual_json_definition: str) -> Dict[str, Any]:
    """
    Extract JSON content from agent's markdown output and convert it to a Python dictionary.
    
    Args:
        visual_json_definition: String containing markdown with JSON code blocks from the agent
        
    Returns:
        Dictionary representation of the extracted JSON definition
    """
    
    # Check if content starts with ```json (markdown format)
    if visual_json_definition.strip().startswith("```json"):
        # Pattern to match JSON content between ```json and ``` markers
        json_pattern = r"```json\s*([\s\S]*?)\s*```"
        json_matches = re.findall(json_pattern, visual_json_definition)
        print(f"JSON matches from markdown")
        
        if not json_matches:
            raise ValueError("No JSON content found in the markdown blocks")
        
        json_string = json_matches[0]
    else:
        # Content is already plain JSON (not in markdown blocks)
        json_string = visual_json_definition.strip()
        print("Content appears to be plain JSON, not markdown")
    
    try:
        # Parse the JSON string into a Python dictionary
        json_dict = json.loads(json_string)
        print(f"✅ Successfully parsed JSON dictionary")
        print(f"Top-level keys: {list(json_dict.keys())}")
        return json_dict
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {str(e)}")
        raise ValueError(f"Failed to parse JSON: {e}")

def add_dataset_identifier(json_definition: Dict[str, Any]) -> Dict[str, Any]:
  """
  Add the dataset identifier to the json definition and replace all DataSetIdentifier placeholders.
  """
  if "Definition" in json_definition:
    # Add DataSetIdentifierDeclarations
    json_definition["Definition"]["DataSetIdentifierDeclarations"] = [
      {
        "DataSetArn": DATASET_ARN,
        "Identifier": DATASET_IDENTIFIER
      }
    ]
    
    # Convert to JSON string to replace all DataSetIdentifier placeholders throughout the definition
    json_string = json.dumps(json_definition)
    
    json_string = json_string.replace("Do_not_change_this_value", DATASET_IDENTIFIER)
    
    # Convert back to dictionary
    json_definition = json.loads(json_string)
    
  else:
    raise ValueError("Definition key not found in the json definition")
    print(f"\n❌ Definition key not found in the json definition: {json_definition} \n")
  
  print(f"\n✅ Added dataset identifier and replaced placeholders in the json definition")
  return json_definition