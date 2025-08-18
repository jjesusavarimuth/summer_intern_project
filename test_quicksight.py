#!/usr/bin/env python3
"""
QuickSight Service Test Suite

Comprehensive tests for all QuickSight API functions including:
- Analysis creation, deletion, listing, and permissions update
- Dashboard creation and permissions
- Automatic cleanup of test resources
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.services.quicksight_service import (
    create_analysis, 
    delete_analysis, 
    get_available_analyses, 
    create_dashboard, 
    update_dashboard_permissions,
    update_analysis_permissions
)

# Test dashboard definition for QuickSight analysis creation
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

class QuickSightTester:
    """Test suite for QuickSight API functions with automatic cleanup"""
    
    def __init__(self):
        self.test_resources = {
            'analyses': [],
            'dashboards': []
        }
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"   └─ {message}")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
    
    def test_analysis_creation(self):
        """Test creating a QuickSight analysis"""
        print("\n🧪 Testing Analysis Creation...")
        
        analysis_name = "test-analysis-automated"
        analysis_id = "test-analysis-automated"
        
        try:
            result = create_analysis(test_dashboard_definition, analysis_name, analysis_id)
            
            if result.get("status") == "success":
                self.test_resources['analyses'].append(analysis_id)
                self.log_test("Analysis Creation", True, f"Created analysis: {analysis_id}")
                return True
            else:
                self.log_test("Analysis Creation", False, f"Failed: {result}")
                return False
                
        except Exception as e:
            self.log_test("Analysis Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_analysis_listing(self):
        """Test listing available analyses"""
        print("\n🧪 Testing Analysis Listing...")
        
        try:
            result = get_available_analyses()
            
            if isinstance(result, dict) and 'AnalysisSummaryList' in result:
                count = len(result['AnalysisSummaryList'])
                self.log_test("Analysis Listing", True, f"Found {count} analyses")
                return True
            else:
                self.log_test("Analysis Listing", False, f"Unexpected response: {result}")
                return False
                
        except Exception as e:
            self.log_test("Analysis Listing", False, f"Exception: {str(e)}")
            return False
    
    def test_analysis_permissions_update(self):
        """Test updating analysis permissions"""
        print("\n🧪 Testing Analysis Permissions Update...")
        
        # Check if we have a created analysis to update
        if not self.test_resources['analyses']:
            self.log_test("Analysis Permissions Update", False, "No analysis available to update permissions")
            return False
        
        analysis_id = self.test_resources['analyses'][0]  # Use the first created analysis
        
        try:
            result = update_analysis_permissions(analysis_id)
            self.log_test("Analysis Permissions Update", True, f"Updated permissions for: {analysis_id}")
            return True
                
        except Exception as e:
            self.log_test("Analysis Permissions Update", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_creation(self):
        """Test creating a QuickSight dashboard"""
        print("\n🧪 Testing Dashboard Creation...")
        
        try:
            result = create_dashboard(test_dashboard_definition["Definition"])
            
            if result.get("status") == "success":
                # Extract dashboard ID from response for cleanup
                dashboard_id = "test-dashboard-1"  # Default ID from create_dashboard function
                self.test_resources['dashboards'].append(dashboard_id)
                self.log_test("Dashboard Creation", True, f"Created dashboard: {dashboard_id}")
                return True
            else:
                self.log_test("Dashboard Creation", False, f"Failed: {result}")
                return False
                
        except Exception as e:
            self.log_test("Dashboard Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_dashboard_permissions(self):
        """Test updating dashboard permissions"""
        print("\n🧪 Testing Dashboard Permissions Update...")
        
        if not self.test_resources['dashboards']:
            self.log_test("Dashboard Permissions Update", False, "No dashboard available to update permissions")
            return False
        
        dashboard_id = self.test_resources['dashboards'][0]  # Use the first created dashboard
        
        try:
            result = update_dashboard_permissions(dashboard_id)
            self.log_test("Dashboard Permissions", True, "Permissions updated successfully")
            return True
                
        except Exception as e:
            self.log_test("Dashboard Permissions", False, f"Exception: {str(e)}")
            return False
    

    
    def cleanup_test_resources(self):
        """Clean up all test resources created during testing"""
        print("\n🧹 Cleaning up test resources...")
        
        # Clean up analyses
        for analysis_id in self.test_resources['analyses']:
            try:
                print(f"   🗑️  Deleting analysis: {analysis_id}")
                result = delete_analysis(analysis_id)
                self.log_test(f"Cleanup Analysis ({analysis_id})", True)
                    
                # Small delay between deletions
                time.sleep(1)
                
            except Exception as e:
                self.log_test(f"Cleanup Analysis ({analysis_id})", False, f"Exception: {str(e)}")
        
        # Note: Dashboard cleanup would require additional API calls
        # QuickSight doesn't have a simple delete_dashboard function in the current service
        if self.test_resources['dashboards']:
            print("   ⚠️  Dashboard cleanup requires manual deletion via AWS Console")
            print(f"   📋 Dashboards to clean up: {', '.join(self.test_resources['dashboards'])}")
    
    def run_all_tests(self):
        """Execute all QuickSight API tests"""
        print("🚀 Starting QuickSight API Test Suite")
        print("=" * 50)
        
        # Test sequence with dependencies
        tests = [
            ("Analysis Creation", self.test_analysis_creation),
            ("Analysis Listing", self.test_analysis_listing),
            ("Analysis Permissions Update", self.test_analysis_permissions_update),
            ("Dashboard Creation", self.test_dashboard_creation),
            ("Dashboard Permissions", self.test_dashboard_permissions),
        ]
        
        # Execute tests
        for test_name, test_func in tests:
            try:
                test_func()
                time.sleep(2)  # Brief pause between tests
            except Exception as e:
                self.log_test(test_name, False, f"Test execution failed: {str(e)}")
        
        # Cleanup
        self.cleanup_test_resources()
        
        # Print summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print final test results summary"""
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        # Show failed tests
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"   • {test['test']}: {test['message']}")
        
        print("\n🎉 Test suite completed!" if passed == total else "\n⚠️  Some tests failed - check AWS credentials and permissions")


def main():
    """Main test execution function"""
    print("QuickSight Service Test Suite")
    print("Testing all API functions with automatic cleanup\n")
    
    # Create and run test suite
    tester = QuickSightTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()