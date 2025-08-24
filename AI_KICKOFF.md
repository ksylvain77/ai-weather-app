# AI Project Kickoff Guide

## 🤖 Getting Started with AI Development

After initializing your project, follow these steps to create an AI-guided development roadmap:

### Step 1: AI Context Setup

```
Hi! I just created a new project from the AI-native template.

Please:
1. Read the BOOTSTRAP_PROMPT.md file to understand the project context
2. Ask me discovery questions to understand what I want to build
3. Fill out PROJECT_GOALS.md with my answers
4. Create a development roadmap in ROADMAP.md broken into feature chunks
5. Each chunk should be sized for one branch using our automation

Let's start!
```

### Step 2: AI Discovery Questions

The AI should ask questions like:

- What type of application are you building? (web app, API, tool, etc.)
- Who are the main users and what do they need to do?
- What are the core features you want to implement first?
- Do you have any specific integrations or requirements?
- What's your timeline and priorities?

### Step 3: AI Creates Persistent Roadmap

The AI will:

1. **Fill PROJECT_GOALS.md** with discovery answers
2. **Create ROADMAP.md** with detailed development plan
3. **Update files** as project progresses

Example roadmap structure:

```
Development Roadmap for [Your Project]

Phase 1: Foundation
├── Branch 1: "setup-core-models" - Define data models and basic structure
├── Branch 2: "add-user-auth" - Implement authentication system
└── Branch 3: "create-basic-ui" - Build initial user interface

Phase 2: Core Features
├── Branch 4: "implement-feature-x" - Main feature implementation
├── Branch 5: "add-data-processing" - Core business logic
└── Branch 6: "integrate-external-api" - Third-party integrations

Phase 3: Enhancement
├── Branch 7: "add-advanced-features" - Additional functionality
└── Branch 8: "polish-and-deploy" - Final touches and deployment
```

These roadmaps are **persistent** and **living documents** that the AI maintains throughout development.

### Step 4: Execute Roadmap

For each feature:

```bash
# Start feature branch
./scripts/create-branch.sh "feature-name" "Feature description"

# Tell AI: "Implement [feature] according to our roadmap"
# AI implements with 4-phase testing

# When ready to merge
./scripts/merge-to-main.sh "Complete feature implementation"

# Move to next feature
```

## 🎯 Benefits

- **No blank page syndrome** - Clear roadmap from day one
- **Logical progression** - Each branch builds on previous work
- **4-phase testing enforced** - Quality maintained throughout
- **Clean git history** - One feature per branch
- **AI collaboration ready** - Context and workflow built-in

## 💡 Tips

- Start with the AI kickoff immediately after project creation
- Let the AI ask follow-up questions to refine the roadmap
- Adjust the roadmap as you learn and requirements evolve
- Use the branch automation for consistent workflow
