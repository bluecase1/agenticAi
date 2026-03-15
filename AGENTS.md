# AGENTS.md - AI Coding Agent Guidelines

This file provides guidance for AI coding agents operating in this repository.

---

## 1. Project Overview

**Project Type**: Python (LangGraph-based Stock Analysis Agent)  
**Python Version**: 3.14+  
**Main Dependencies**: langgraph, langchain_openai, langchain-google-genai, pykrx, yfinance, mcp

---

## 2. Build & Development Commands

### Running the Application
```bash
# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run main application
python main.py

# Run MCP servers individually (for testing)
python mcp_servers/kr_stock.py
python mcp_servers/us_stock.py
```

### Testing
> **Note**: Currently no test suite exists. Tests should be added using pytest.

```bash
# Run all tests (when tests exist)
pytest

# Run a single test file
pytest tests/test_file.py

# Run a single test function
pytest tests/test_file.py::test_function_name

# Run tests matching a pattern
pytest -k "test_pattern"
```

### Linting & Formatting
> **Note**: No linting/formatting config currently exists. Recommended to add:
- `ruff` for linting (fast, modern)
- `black` for formatting

```bash
# Install recommended tools
pip install ruff black

# Lint with ruff
ruff check .

# Format with black
black .

# Type checking (if type stubs added)
mypy .
```

---

## 3. Code Style Guidelines

### General Principles
- Follow existing code patterns in this repository
- Use Korean comments (as seen in existing code)
- Keep functions focused and single-purpose
- Use TypedDict for state definitions

### Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Files | snake_case | `kr_stock.py`, `agent_state.py` |
| Classes | PascalCase | `AgentState`, `FastMCP` |
| Functions | snake_case | `get_kr_stock_price()`, `identifier_node()` |
| Variables | snake_case | `user_input`, `stock_info` |
| Constants | UPPER_SNAKE | `MAX_RETRIES`, `API_TIMEOUT` |
| Type Aliases | PascalCase | `AgentState` (TypedDict) |

### Import Order (Recommended)
1. Standard library (`os`, `sys`, `datetime`)
2. Third-party packages (`langchain_openai`, `pykrx`)
3. Local modules (`from nodes.identifier import ...`, `from mcp_servers.kr_stock import ...`)

```python
# Correct order
import os
import sys
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pykrx import stock

from state import AgentState
from nodes.identifier import identifier_node
from mcp_servers.kr_stock import get_kr_stock_price
```

### Type Annotations
- Use `typing.TypedDict` for state definitions
- Use `typing.Annotated` for LangGraph's message addition
- Add type hints for function parameters and return types

```python
# Good - TypedDict for state
from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[Dict[str, Any]], add_messages]
    market: str
    stock_data: Dict[str, Any]

# Good - Function type hints
def researcher_node(state: AgentState) -> dict:
    """Process docstring."""
    market: str = state.get("market", "UNKNOWN")
    return {"stock_data": {...}}
```

### Error Handling
- Use try/except blocks with specific exception types
- Always include error messages in returns or logs
- Never swallow exceptions silently

```python
# Good
try:
    result = get_kr_stock_price(target)
except ValueError as e:
    logger.error(f"Invalid ticker: {e}")
    return {"error": f"Invalid ticker: {str(e)}"}
except Exception as e:
    return {"error": f"Data collection failed: {str(e)}"}

# Bad - silent catch
try:
    result = get_kr_stock_price(target)
except:
    pass  # Never do this
```

### Function & Class Docstrings
- Use triple quotes for docstrings
- Include Args and Returns sections for complex functions

```python
def get_us_stock_price(symbol: str) -> str:
    """
    Get current US stock price and metrics.
    
    Args:
        symbol (str): US stock ticker (e.g., 'AAPL', 'NVDA')
    
    Returns:
        str: Formatted price information with change percentage
    """
```

### LangGraph Node Conventions
- Each node is a function returning a dictionary (state updates)
- Node functions accept `state: AgentState` as parameter
- Use descriptive print statements for debugging

```python
def identifier_node(state: AgentState) -> dict:
    """Description of what this node does."""
    user_input = state["messages"][-1].content
    
    print(f"--- [Node: Identifier] ---")
    print(f"Input: {user_input}")
    
    return {"market": "KR"}
```

### Environment & Configuration
- All secrets go in `.env` file
- Always load `.env` at the start of entry points
- Add sensitive files to `.gitignore`

```python
from dotenv import load_dotenv

load_dotenv()  # Load FIRST, before any other imports
```

---

## 4. Directory Structure

```
agenticAi/
├── .env                 # API keys (never commit!)
├── .gitignore           # Excludes .env, __pycache__, .venv
├── main.py              # Entry point - graph compilation
├── state.py             # TypedDict state definitions
├── requirements.txt     # Dependencies
│
├── nodes/               # LangGraph nodes
│   ├── __init__.py
│   ├── identifier.py    # Market identification (KR/US)
│   ├── researcher.py    # Data collection via MCP
│   └── analyst.py       # Report generation
│
├── mcp_servers/         # MCP tool servers
│   ├── __init__.py
│   ├── kr_stock.py      # Korean stock data (pykrx)
│   └── us_stock.py      # US stock data (yfinance)
│
└── prompts/             # (reserved for system prompts)
```

---

## 5. Important Notes for Agents

### Critical Rules
1. **Never commit `.env`** - it contains API keys
2. **Never use `as any`** or suppress type errors
3. **Never leave empty catch blocks**
4. **Always run `lsp_diagnostics`** after making code changes
5. **Always verify build/tests pass** before reporting completion

### Git Workflow
- Create feature branches for new features
- Commit messages in English (imperative mood)
- Run tests before committing

### Adding Dependencies
1. Add to `requirements.txt`
2. Test locally
3. Document new dependencies in comments

---

## 6. Existing Cursor/Copilot Rules

None found. This file serves as the primary guidance for AI coding agents.
