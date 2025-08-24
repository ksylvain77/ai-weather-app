# Weather app - AI Collaboration Instructions

## Project Overview

This is a **Flask application** project using AI-Native Development methodology.

**Repository**: https://github.com/yourusername/weather-app

## 🚨 **CRITICAL: MANDATORY WORKFLOW**

### **Git Workflow (REQUIRED)**

```bash
# 1. AI creates branch using automation
./scripts/create-branch.sh feature-name "Description of work"

# 2. AI implements feature following DRY patterns

# 3. AI shows user results and waits for approval

# 4. AI finalizes using automation
./scripts/merge-to-main.sh "Final commit message"
```

### **Testing Requirements (MANDATORY)**

- **Quick Tests**: `.venv/bin/python tests/quick_test.py` (development)
- **Full Tests**: `./scripts/run-tests.sh` (pre-commit)
- **4-Phase Testing**: Backend → API → Contract → Frontend
- **Completion Criteria**: 100% test pass rate required

### **Environment Requirements**

- **Python**: Always use `.venv/bin/python` (never system python)
- **Server**: http://localhost:5000
- **Port Check**: Quick validation - `netstat -tuln | grep :5000` (should be empty)
- **Setup**: `./manage.sh setup` (one-time)
- **Start**: `./manage.sh start`

## Core Philosophy

- **AI-Native**: Project structure optimized for AI collaboration
- **Automation-First**: Scripts handle repetitive tasks
- **Test-Driven**: Features only complete when fully tested
- **Documentation-Driven**: Clear context enables effective AI work
- **Merge as You Go**: Immediate integration, clean history

## Development Patterns

### Adding Features (DRY Pattern)

1. **Backend**: Add function to appropriate module in `modules/`
2. **Test**: Add to `test_suite.py` using dictionary format
3. **API**: Add endpoint to `weather_app.py`
4. **Frontend**: Update templates/static if needed

### Testing Approach (4-Phase Methodology)

```python
# Backend test - DRY format
"test_name": {
    "description": "Test description",
    "module": "modules.your_module",
    "function": "your_function",
    "assertions": ["assert 'field' in result"]
}

# API test - simple dictionary
"api_name": {
    "endpoint": "/api/your/endpoint",
    "expected_fields": ["field1", "field2"]
}
```

## Project Structure

```
weather_app.py                 # Application entry point
modules/                      # Core business logic
templates/                    # UI templates
static/                       # Static assets
tests/                        # Testing framework
scripts/                      # Automation scripts
BOOTSTRAP_PROMPT.md           # Quick AI context
ROADMAP.md                    # Development roadmap and progress
PROJECT_GOALS.md              # Requirements and discovery results
```

## Working with AI

- **Context**: Bootstrap Prompt provides immediate project context
- **Roadmap**: ROADMAP.md tracks development phases and progress
- **Goals**: PROJECT_GOALS.md stores requirements and discovery results
- **Workflow**: Always use automation scripts, never manual Git
- **Testing**: Complete all 4 phases before feature completion
- **Documentation**: Auto-maintained, stays current with system state
- **Error Handling**: Structured for AI debugging and self-healing

**Success Criteria**: Feature complete when automated workflow passes with 100% test coverage.
