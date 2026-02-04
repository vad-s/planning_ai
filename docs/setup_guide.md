# Setup Guide - Planning AI System

**Last Updated:** February 4, 2026  
**Tested On:** Windows, Python 3.11+

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)
7. [Development Workflow](#development-workflow)

---

## Prerequisites

### Required Software
- **Python 3.11+** (3.12 recommended)
- **Git** (for cloning repository)
- **Azure OpenAI API access** (for production LLMs) OR local LLM setup

### Optional Tools
- **VS Code** with Python extension
- **Docker** (for containerized deployment)
- **Pytest** (for running tests)

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/vad-s/planning_ai.git
cd planning_ai
```

### 2. Create Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows CMD
python -m venv venv
venv\Scripts\activate.bat

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

**⚠️ IMPORTANT:** The `pyproject.toml` is currently empty. Until it's populated, install manually:

```bash
pip install crewai
pip install crewai-tools
pip install langchain
pip install langchain-openai
pip install pydantic
pip install pyyaml
pip install python-dotenv
```

**For development/testing:**
```bash
pip install pytest
pip install pytest-asyncio
pip install black
pip install flake8
pip install mypy
```

**Once pyproject.toml is populated:**
```bash
pip install -e .
```

---

## Configuration

### 1. Environment Variables (API Keys)

**Create `.env` file in project root:**

```bash
# .env (DO NOT COMMIT THIS FILE)

# Azure OpenAI Configuration (GPT-4)
AZURE_OPENAI_API_KEY_GPT4=your-gpt4-api-key-here
AZURE_OPENAI_ENDPOINT_GPT4=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME_GPT4=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure OpenAI Configuration (GPT-5)
AZURE_OPENAI_API_KEY_GPT5=your-gpt5-api-key-here
AZURE_OPENAI_ENDPOINT_GPT5=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME_GPT5=gpt-5-nano

# Alternative: Use OpenAI directly
# OPENAI_API_KEY=sk-...
```

**Create `.env.example` for team:**
```bash
# .env.example (COMMIT THIS FILE)
AZURE_OPENAI_API_KEY_GPT4=your-key-here
AZURE_OPENAI_ENDPOINT_GPT4=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME_GPT4=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Add to `.gitignore`:**
```bash
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
echo "!.env.example" >> .gitignore
```

---

### 2. Flow Configuration

**Edit `src/resources/flow_config.yaml`:**

```yaml
# Output configuration
save_folder: "output/bfs_runs"
project_name: "my_project"  # Change this for your project
version: "v1.0.0"
overwrite: true  # false to create timestamped folders

# LLM selection per crew
llm_type:
  manager_crew: "mock"      # Options: mock, gpt4, gpt5
  planners_crew: "mock"     # Use mock for testing (free)
  reviewer_crew: "mock"     # Use gpt4/gpt5 for production (costs money)
  writer_crew: "mock"
```

**For testing (no API costs):**
```yaml
llm_type:
  manager_crew: "mock"
  planners_crew: "mock"
  reviewer_crew: "mock"
  writer_crew: "mock"
```

**For production (uses Azure API):**
```yaml
llm_type:
  manager_crew: "gpt4"
  planners_crew: "gpt4"
  reviewer_crew: "gpt4"
  writer_crew: "gpt5"
```

---

### 3. Project Idea Configuration

**Edit `src/resources/init_idea.yaml`:**

```yaml
mission: |
  Your project mission here. Example:
  Build a task management system with AI-powered prioritization,
  natural language input, and smart scheduling.

technical_constraints:
  platform: "Web-based, mobile-responsive"
  tech_stack: "Python backend, React frontend"
  deployment: "Docker containers on AWS"
  database: "PostgreSQL with Redis cache"

suggestion_pillar_future_experimental:
  ai_features: "GPT-4 for task analysis and suggestions"
  integrations: "Calendar sync, Slack notifications"
  scaling: "Support 10K concurrent users"

required_output_format_for_planners:
  structure: "Markdown with YAML frontmatter"
  sections: |
    - Overview (purpose, goals)
    - Technical Architecture (components, data flow)
    - Implementation Timeline (phases, milestones)
    - Risk Analysis (technical, business, operational)
```

---

## Running the System

### Option 1: Quick Start with Mock LLMs (Recommended for First Run)

```bash
# Ensure mock LLMs configured in flow_config.yaml
python main.py
```

**Expected Output:**
```
Starting BFSNodeFlow...
[Manager] Processing root node...
[Planners] Generating 3 plans...
[Reviewer] Evaluating plans...
[Writer] Creating documentation...
Flow execution complete.
```

**Output Location:** `output/bfs_runs/my_project_v1.0.0/`

---

### Option 2: Production Run with Real LLMs

```bash
# 1. Verify .env file has API keys
cat .env  # or type .env on Windows

# 2. Set flow_config.yaml to use gpt4/gpt5

# 3. Run
python main.py
```

**⚠️ Cost Warning:** Each crew call uses LLM tokens. Estimate: $0.01-$0.10 per node depending on model.

---

### Option 3: BFS Simulator (No LLMs)

For understanding the BFS algorithm without AI:

```bash
python main_bfs.py
```

**Output:** Colorized tree visualization in terminal

---

## Testing

### Run All Tests

```bash
pytest src/tests/ -v
```

**⚠️ Current Status:** Tests are broken due to missing schema files. See [Step 2: Resolve Missing Dependencies](#step-2-resolve-missing-dependencies) below.

---

### Run Specific Test

```bash
pytest src/tests/test_manager_crew.py -v
```

---

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html
```

---

## Troubleshooting

### Issue 1: ModuleNotFoundError: No module named 'src.schemas'

**Cause:** Missing schema files (see [code_review_findings.md](code_review_findings.md) #1)

**Solution A (Temporary):** Use mock LLMs and avoid running tests

**Solution B (Permanent):** Create missing schemas or refactor imports (Step 2 below)

---

### Issue 2: Azure API Authentication Error

**Symptoms:**
```
AuthenticationError: Invalid API key
```

**Solutions:**
1. Verify `.env` file exists and has correct keys
2. Check `flow_config.yaml` has `llm_type: "gpt4"` (not "mock")
3. Ensure API keys not expired
4. Verify Azure resource name in endpoint URL

**Test API Connection:**
```bash
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('API Key:', os.getenv('AZURE_OPENAI_API_KEY_GPT4')[:10] + '...')
print('Endpoint:', os.getenv('AZURE_OPENAI_ENDPOINT_GPT4'))
"
```

---

### Issue 3: Empty Output Folder

**Cause:** Flow completes but no files written

**Status:** Expected behavior (output generation not implemented yet)

**Workaround:** Check `state.completed_queue` in code or add print statements

---

### Issue 4: Random Child Generation

**Symptoms:** Different tree structures on each run

**Cause:** `random.randint(0, 2)` in WriterCrew

**Workaround:** Set random seed for reproducibility
```python
# Add to main.py
import random
random.seed(42)
```

---

### Issue 5: Crew Timeout

**Symptoms:** Hangs during crew execution

**Solutions:**
1. Check internet connection (for API calls)
2. Increase timeout in crew configuration
3. Use mock LLMs to test flow logic

---

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
```bash
# Edit files
# Add tests
```

### 3. Run Tests
```bash
pytest src/tests/ -v
```

### 4. Format Code
```bash
black src/
flake8 src/
```

### 5. Commit and Push
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

---

## Project Structure

```
planning_ai/
├── main.py                    # Primary entry point (BFSNodeFlow)
├── main_bfs.py                # BFS simulator (no AI)
├── main_*.py                  # Other entry points (see docs)
├── pyproject.toml             # Dependencies (TO BE POPULATED)
├── README.md                  # Project overview (TO BE WRITTEN)
├── .env                       # Secrets (CREATE THIS, DON'T COMMIT)
├── .env.example               # Template for .env
├── .gitignore                 # Git ignore patterns
├── docs/                      # Documentation
│   ├── code_review_findings.md
│   ├── architecture_overview.md
│   └── setup_guide.md (this file)
├── output/                    # Generated output
│   └── bfs_runs/
│       └── project_v1.0.0/
├── src/
│   ├── crews/                 # 4 AI agent crews
│   │   ├── manager_crew/
│   │   ├── planners_crew/
│   │   ├── reviewer_crew/
│   │   └── writer_crew/
│   ├── flows/                 # Flow orchestration
│   │   ├── bfs_node_flow.py  # Current (Node-based)
│   │   ├── bfs_flow.py       # Legacy (dict-based)
│   │   └── depth_first_traversal_flow.py
│   ├── generic/               # Reusable components
│   │   ├── base_schema.py    # Pydantic base
│   │   ├── node.py           # Node hierarchy
│   │   ├── init_idea.py      # Project spec
│   │   └── llm_utils.py      # LLM factory
│   ├── state/                 # State management
│   │   ├── node_state.py     # Current (Node-based)
│   │   └── state.py          # Legacy (dict-based)
│   ├── enums/                 # Enum definitions
│   ├── resources/             # Configuration files
│   │   ├── flow_config.yaml
│   │   └── init_idea.yaml
│   └── tests/                 # Test suite
└── venv/                      # Virtual environment (not committed)
```

---

## Quick Reference

### Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run main flow
python main.py

# Run tests
pytest src/tests/ -v

# Format code
black src/

# Install new dependency
pip install package-name
pip freeze > requirements.txt  # Until pyproject.toml populated

# Check Python version
python --version

# Verify installation
python -c "import crewai; print('CrewAI installed:', crewai.__version__)"
```

---

### Configuration Quick Tweaks

**Change Project Name:**
```yaml
# src/resources/flow_config.yaml
project_name: "new_project_name"
```

**Increase Tree Depth:**
```python
# src/generic/base_schema.py
depth_limit: int = 7  # Default is 5
```

**Change LLM Temperature:**
```python
# src/generic/llm_utils.py
# Edit get_llm() method, temperature parameter
```

---

## Next Steps

After setup:

1. **Read [architecture_overview.md](architecture_overview.md)** to understand system design
2. **Read [code_review_findings.md](code_review_findings.md)** for known issues
3. **Run `python main.py`** with mock LLMs to verify installation
4. **Customize `init_idea.yaml`** for your project
5. **Review output** in `output/bfs_runs/`

---

## Support

### Issues
- **GitHub Issues:** https://github.com/vad-s/planning_ai/issues
- **Documentation:** `docs/` folder
- **Code Comments:** Check inline docstrings

### Contributing
1. Fork repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

---

## License

[TO BE ADDED]

---

## Changelog

### v1.0.0 (Current)
- Initial release
- BFS Node-based flow
- 4-crew orchestration
- Mock LLM support
- Azure OpenAI integration

---

*For detailed architecture information, see [architecture_overview.md](architecture_overview.md)*  
*For known issues and roadmap, see [code_review_findings.md](code_review_findings.md)*
