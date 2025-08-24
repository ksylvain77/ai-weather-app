#!/usr/bin/env python3
"""
Weather app - Comprehensive Testing Suite
Template for 4-phase testing methodology
"""

import sys
import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSuite:
    """
    Comprehensive testing suite template following 4-phase methodology:
    Phase 1: Backend Function Testing (MANDATORY)
    Phase 2: API Integration Testing (MANDATORY) 
    Phase 2.5: Data Contract Validation (MANDATORY)
    Phase 3: Frontend Integration Testing (MANDATORY)
    """
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.results = {
            "phase_1_backend": {},
            "phase_2_api": {},
            "phase_2_5_contracts": {},
            "phase_3_frontend": {},
            "summary": {"total_tests": 0, "passed": 0, "failed": 0, "errors": []}
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log test message with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        icon = {"TEST": "🧪", "INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"{icon.get(level, 'ℹ️')} [{timestamp}] {message}")
    
    def phase_1_backend_tests(self):
        """Phase 1: Test all backend functions directly"""
        self.log("🔬 PHASE 1: BACKEND FUNCTION TESTING", "TEST")
        self.log("=" * 60)
        
        # DRY configuration - customize for your project
        backend_tests = {
            "core_function": {
                "description": "Test core functionality",
                "module": "modules.core",  # Customize
                "function": "get_status",   # Customize
                "assertions": [
                    "assert 'status' in result",
                    "assert result['status'] == 'running'"
                ]
            },
            # Add more backend tests here
        }
        
        for test_name, test_config in backend_tests.items():
            self.log(f"Testing {test_config['description']}...")
            
            try:
                # Dynamic import and execution
                module = __import__(test_config['module'], fromlist=[test_config['function']])
                func = getattr(module, test_config['function'])
                result = func()
                
                # Run assertions
                for assertion in test_config['assertions']:
                    exec(assertion)
                
                self.results["phase_1_backend"][test_name] = {
                    "success": True,
                    "result": "Test completed successfully",
                    "error": None
                }
                self.log(f"✅ {test_name}: PASSED", "PASS")
                
            except Exception as e:
                self.results["phase_1_backend"][test_name] = {
                    "success": False,
                    "result": None,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: FAILED - {e}", "FAIL")
    
    def phase_2_api_tests(self):
        """Phase 2: Test all API endpoints"""
        self.log("\n🌐 PHASE 2: API INTEGRATION TESTING", "TEST")
        self.log("=" * 60)
        
        api_tests = {
            "health_endpoint": {
                "endpoint": "/health",
                "expected_fields": ["status"]  # Customize
            },
            # Add more API tests here
        }
        
        for test_name, test_config in api_tests.items():
            self.log(f"Testing {test_config['endpoint']}...")
            
            try:
                response = requests.get(f"{self.base_url}{test_config['endpoint']}", timeout=10)
                
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code}")
                
                data = response.json()
                
                # Check expected fields
                missing_fields = []
                for field in test_config['expected_fields']:
                    if field not in data:
                        missing_fields.append(field)
                
                if missing_fields:
                    raise Exception(f"Missing fields: {missing_fields}")
                
                self.results["phase_2_api"][test_name] = {
                    "success": True,
                    "endpoint": test_config['endpoint'],
                    "expected_fields": test_config['expected_fields'],
                    "missing_fields": [],
                    "details": f"✅ All {len(test_config['expected_fields'])} fields present"
                }
                self.log(f"✅ {test_config['endpoint']}: PASSED", "PASS")
                
            except Exception as e:
                self.results["phase_2_api"][test_name] = {
                    "success": False,
                    "endpoint": test_config['endpoint'],
                    "error": str(e)
                }
                self.log(f"❌ {test_config['endpoint']}: FAILED - {e}", "FAIL")
    
    def phase_2_5_contract_validation(self):
        """Phase 2.5: Validate API-Frontend data contracts"""
        self.log("\n🔗 PHASE 2.5: DATA CONTRACT VALIDATION", "TEST")
        self.log("=" * 60)
        
        # Test data contracts between API and frontend
        contract_tests = {
            "main_contract": {
                "api_endpoint": "/health",
                "expected_structure": {
                    "status": "string"  # Customize
                },
                "frontend_expectations": [
                    "data.status"  # Customize
                ]
            },
            # Add more contract tests here
        }
        
        for test_name, test_config in contract_tests.items():
            self.log(f"Validating {test_config['api_endpoint']} contract...")
            
            try:
                response = requests.get(f"{self.base_url}{test_config['api_endpoint']}", timeout=10)
                data = response.json()
                
                # Validate structure
                missing_fields = []
                for field_path, expected_type in test_config['expected_structure'].items():
                    # Simple field validation - extend as needed
                    if '.' in field_path:
                        parts = field_path.split('.')
                        current = data
                        for part in parts:
                            if part not in current:
                                missing_fields.append(field_path)
                                break
                            current = current[part]
                    else:
                        if field_path not in data:
                            missing_fields.append(field_path)
                
                self.results["phase_2_5_contracts"][test_name] = {
                    "success": len(missing_fields) == 0,
                    "api_endpoint": test_config['api_endpoint'],
                    "missing_fields": missing_fields,
                    "sample_data": {k: str(v)[:50] for k, v in data.items() if k != 'error'}
                }
                
                if missing_fields:
                    self.log(f"❌ {test_name}: CONTRACT INVALID - Missing: {missing_fields}", "FAIL")
                else:
                    self.log(f"✅ {test_name}: CONTRACT VALID", "PASS")
                
            except Exception as e:
                self.results["phase_2_5_contracts"][test_name] = {
                    "success": False,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: CONTRACT ERROR - {e}", "FAIL")
    
    def phase_3_frontend_tests(self):
        """Phase 3: Test frontend functionality"""
        self.log("\n🖥️ PHASE 3: FRONTEND INTEGRATION TESTING", "TEST")
        self.log("=" * 60)
        
        # Basic frontend tests - extend with browser automation if needed
        frontend_tests = [
            ("page_load", self._test_page_load),
            # Add more frontend tests here
        ]
        
        for test_name, test_func in frontend_tests:
            self.log(f"Testing {test_name}...")
            
            try:
                success, result = test_func()
                
                self.results["phase_3_frontend"][test_name] = {
                    "success": success,
                    "result": result,
                    "error": None if success else result
                }
                
                if success:
                    self.log(f"✅ {test_name}: PASSED", "PASS")
                else:
                    self.log(f"❌ {test_name}: FAILED - {result}", "FAIL")
                    
            except Exception as e:
                self.results["phase_3_frontend"][test_name] = {
                    "success": False,
                    "result": None,
                    "error": str(e)
                }
                self.log(f"❌ {test_name}: ERROR - {e}", "FAIL")
    
    def _test_page_load(self) -> Tuple[bool, str]:
        """Test main page loading"""
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                return True, "Main page loaded successfully"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def generate_summary(self):
        """Generate test summary"""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        errors = []
        
        for phase, tests in self.results.items():
            if phase == "summary":
                continue
                
            for test_name, result in tests.items():
                total_tests += 1
                if result.get("success", False):
                    passed_tests += 1
                else:
                    failed_tests += 1
                    error_msg = result.get("error", "Unknown error")
                    errors.append(f"{phase}.{test_name}: {error_msg}")
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": errors
        }
        
        return total_tests, passed_tests, failed_tests
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.log("🚀 Weather app - COMPREHENSIVE TEST SUITE", "TEST")
        self.log("=" * 80)
        self.log(f"Target: {self.base_url}")
        self.log(f"Started: {datetime.now().isoformat()}")
        self.log("")
        
        # Run all phases
        self.phase_1_backend_tests()
        self.phase_2_api_tests()
        self.phase_2_5_contract_validation()
        self.phase_3_frontend_tests()
        
        # Generate summary
        total, passed, failed = self.generate_summary()
        
        self.log("\n📊 FINAL TEST REPORT", "TEST")
        self.log("=" * 80)
        self.log(f"Total Tests: {total}")
        self.log(f"Passed: {passed}", "PASS")
        self.log(f"Failed: {failed}", "FAIL" if failed > 0 else "PASS")
        self.log("")
        
        # Save results
        timestamp = int(datetime.now().timestamp())
        results_file = f"test-results/test_results_{timestamp}.json"
        os.makedirs("test-results", exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.log(f"📄 Detailed report saved: {os.path.abspath(results_file)}")
        self.log(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
        
        if failed == 0:
            self.log("🎉 ALL TESTS PASSED - SYSTEM FULLY OPERATIONAL!", "PASS")
            return True
        else:
            self.log(f"❌ {failed} TESTS FAILED - REVIEW REQUIRED", "FAIL")
            return False

def main():
    """Main test runner"""
    suite = TestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
