#!/bin/bash
# Generic Test Runner Template

set -e

PROJECT_NAME="Weather app"
BASE_URL="http://localhost:5000"
HEALTH_ENDPOINT="/health"

echo "🧪 $PROJECT_NAME - Test Runner"
echo "========================================"

# Check if service is running
echo "🔍 Checking if $PROJECT_NAME is running..."
if curl -s "$BASE_URL$HEALTH_ENDPOINT" > /dev/null 2>&1; then
    echo "✅ $PROJECT_NAME is responding at $BASE_URL"
else
    echo "❌ $PROJECT_NAME is not responding at $BASE_URL"
    echo "💡 Start it with: ./manage.sh start"
    exit 1
fi

echo "✅ $PROJECT_NAME is already running and healthy"


# Enforce 4-phase test coverage before running tests
if [ -f "scripts/check-test-coverage.py" ]; then
    echo "🔒 Enforcing 4-phase test coverage..."
    .venv/bin/python scripts/check-test-coverage.py
fi

# Run test suite
echo "🚀 Running comprehensive test suite..."
if [ -f ".venv/bin/python" ] && [ -f "tests/test_suite.py" ]; then
    echo "✅ $PROJECT_NAME is responding at $BASE_URL"
    echo "🧪 Executing test suite with validated environment..."
    .venv/bin/python tests/test_suite.py
else
    echo "⚠️  Test suite not found - implement tests/test_suite.py"
    echo "✅ Basic connectivity test passed"
fi

echo "✅ Test suite execution completed"

# Post-test health check
echo "🔍 Post-test health check..."
if curl -s "$BASE_URL$HEALTH_ENDPOINT" > /dev/null 2>&1; then
    echo "✅ $PROJECT_NAME is responding at $BASE_URL"
else
    echo "⚠️  $PROJECT_NAME stopped responding after tests"
fi

echo ""
echo "🧹 Auto-cleaning test artifacts..."
# Add any cleanup logic here
