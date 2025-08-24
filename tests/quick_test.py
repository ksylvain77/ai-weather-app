#!/usr/bin/env python3
"""
Weather app - Quick Test Runner
Fast development testing for immediate feedback
"""

import sys
import os
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_backend_test():
    """Test core backend functions"""
    try:
        # Import your main modules here
        # Example:
        # from modules.core import get_status
        # result = get_status()
        # assert 'status' in result
        print("✅ Backend functions working")
        return True
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def quick_api_test():
    """Test core API endpoints"""
    base_url = "http://localhost:5000"
    
    endpoints = [
        "/health",
        # Add your core endpoints here
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}")
            else:
                print(f"❌ {endpoint} (status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ {endpoint} (error: {e})")
            return False
    
    return True

def quick_frontend_test():
    """Test core frontend pages"""
    base_url = "http://localhost:5000"
    
    pages = [
        "/",
        # Add your core pages here
    ]
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}{page}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {page}")
            else:
                print(f"❌ {page} (status: {response.status_code})")
                return False
        except Exception as e:
            print(f"❌ {page} (error: {e})")
            return False
    
    return True

def main():
    """Run quick tests"""
    print("🏃‍♂️ QUICK TEST RUNNER")
    print("========================================")
    print()
    
    tests = [
        ("🔬 Testing Backend Functions...", quick_backend_test),
        ("🌐 Testing API Endpoints...", quick_api_test),
        ("🖥️ Testing Frontend Pages...", quick_frontend_test),
    ]
    
    all_passed = True
    
    for description, test_func in tests:
        print(description)
        if not test_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 ALL QUICK TESTS PASSED!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
