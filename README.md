# Weather app

a flask weather app

## 🤖 AI-Guided Development

**New to this project?** Start with AI collaboration:

1. Open `AI_KICKOFF.md` in your IDE
2. Follow the AI discovery process to create your development roadmap
3. Execute features one-by-one using the branch automation

## Quick Start

```bash
# Setup (one time)
./manage.sh setup

# Start the service
./manage.sh start


# Run tests (enforces 4-phase coverage)
./scripts/run-tests.sh

# Development workflow
./scripts/create-branch.sh feature-name "Description"
# ... make changes ...
./scripts/merge-to-main.sh "Final commit message"
```

## AI-Native Development

This project uses an **AI-Native Development Workflow**:

- **Bootstrap Prompt**: `BOOTSTRAP_PROMPT.md` - Quick context for AI collaboration
- **Automation Scripts**: `scripts/` - Consistent Git workflow and testing
- **DRY Testing**: Dictionary-based test configuration
- **Auto-Documentation**: README updates with live system data

## Architecture

```
weather_app.py                 # Main application entry point
modules/                      # Core business logic
  ├── core.py         # Core business logic
  └── utils.py         # Utility functions
tests/
  ├── quick_test.py          # Fast development tests (2s)
  └── test_suite.py          # Comprehensive testing (30s+)
scripts/
  ├── create-branch.sh       # AI workflow: create feature branch
  ├── merge-to-main.sh       # AI workflow: test + merge + cleanup
  ├── check-test-coverage.py # Enforces 4-phase test coverage (auto-fails if missing)
  └── run-tests.sh           # Comprehensive test runner
```

## Requirements

- Python 3.8+
- Virtual environment (`.venv/`)

## Project Status

- **Status**: In Development
- **Version**: 0.1.0
- **Last Updated**: 2025-01-01

## 4-Phase Test Coverage Enforcement

All new features/endpoints must be covered by tests in all four phases:

- **Backend**: Core logic in `modules/`
- **API**: Endpoints in `weather_app.py`
- **Contract**: Data contract/validation
- **Frontend**: UI or simulated client

The test runner (`./scripts/run-tests.sh`) will fail if any new function or endpoint is missing from any test phase. See `scripts/check-test-coverage.py` for details.

## Contributing

This project follows the **"Merge as You Go"** philosophy for AI collaboration:

1. AI creates feature branches using `./scripts/create-branch.sh`
2. AI implements and tests features (all 4 phases required)
3. User approves changes
4. AI merges using `./scripts/merge-to-main.sh` (auto: test → commit → merge → cleanup)

**Key Principle**: Main branch always working, immediate integration, clean history.
