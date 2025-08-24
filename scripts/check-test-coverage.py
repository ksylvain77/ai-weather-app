#!/usr/bin/env python3
"""
check-test-coverage.py: Enforce 4-phase test coverage for all features/endpoints.

Fails if any backend function or API endpoint is missing from any test phase.
"""
import sys
import os
import ast
import re

# --- Configurable paths ---
MODULES_DIR = 'modules'
TEST_SUITE = 'tests/test_suite.py'
API_FILE = 'weather_app.py'  # Will be replaced in generated project

# --- Helper functions ---
def get_functions_from_module(module_path):
    with open(module_path, 'r') as f:
        tree = ast.parse(f.read(), filename=module_path)
    return [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]

def get_api_endpoints(api_path):
    endpoints = set()
    with open(api_path, 'r') as f:
        for line in f:
            m = re.search(r'@app\.route\(["\'](/api/[^"\']*)', line)
            if m:
                endpoints.add(m.group(1))
    return endpoints

def get_test_dict_keys(test_path, dict_name):
    with open(test_path, 'r') as f:
        content = f.read()
    m = re.search(rf'{dict_name}\s*=\s*{{(.*?)}}', content, re.DOTALL)
    if not m:
        return set()
    dict_body = m.group(1)
    keys = re.findall(r'"([^"]+)":', dict_body)
    return set(keys)

# --- Main check ---
def main():
    # Backend functions
    backend_funcs = set()
    for fname in os.listdir(MODULES_DIR):
        if fname.endswith('.py'):
            backend_funcs.update(get_functions_from_module(os.path.join(MODULES_DIR, fname)))
    # API endpoints
    api_endpoints = get_api_endpoints(API_FILE)
    # Test suite dicts
    backend_tests = get_test_dict_keys(TEST_SUITE, 'backend_tests')
    api_tests = get_test_dict_keys(TEST_SUITE, 'api_tests')
    contract_tests = get_test_dict_keys(TEST_SUITE, 'contract_tests')
    frontend_tests = get_test_dict_keys(TEST_SUITE, 'frontend_tests')
    # Check all backend functions are tested
    missing_backend = backend_funcs - backend_tests
    # Check all endpoints are tested
    missing_api = api_endpoints - api_tests
    # Check all phases for each endpoint
    missing_contract = api_endpoints - contract_tests
    missing_frontend = api_endpoints - frontend_tests
    errors = []
    if missing_backend:
        errors.append(f"Missing backend tests for: {sorted(missing_backend)}")
    if missing_api:
        errors.append(f"Missing API tests for: {sorted(missing_api)}")
    if missing_contract:
        errors.append(f"Missing contract tests for: {sorted(missing_contract)}")
    if missing_frontend:
        errors.append(f"Missing frontend tests for: {sorted(missing_frontend)}")
    if errors:
        print("\n❌ 4-Phase Test Coverage Check Failed:")
        for err in errors:
            print("  -", err)
        sys.exit(1)
    print("✅ All features/endpoints have 4-phase test coverage!")

if __name__ == '__main__':
    main()
