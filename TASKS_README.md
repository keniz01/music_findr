# Music Findr Task Automation

This directory contains an improved `tasks.py` script that provides comprehensive automation for the Music Findr project.

## Installation

First, install the required dependencies:

```bash
pip install -r requirements-tasks.txt
```

Or install manually:
```bash
pip install invoke colorama
```

## Quick Start

```bash
# Show project status and available commands
inv status

# Run all tests
inv test

# Run complete quality assurance pipeline
inv qa

# Install all dependencies
inv install
```

## Available Tasks

### Setup and Installation
- `inv install` - Install dependencies for all components
- `inv install --component=backend-data` - Install dependencies for specific component
- `inv dev-setup --component=frontend-app` - Complete development setup for a component

### Testing
- `inv test` - Run all tests across the entire project
- `inv test-backend-data` - Test back-end data accessor
- `inv test-backend-server` - Test back-end MCP server
- `inv test-frontend-app` - Test front-end React app

### Development Servers
- `inv dev-backend-server` - Start MCP server on http://localhost:8000
- `inv dev-frontend-client` - Start MCP client on http://localhost:8080
- `inv dev-frontend-app` - Start React app on http://localhost:5173

### Code Quality
- `inv lint` - Run linting for all components
- `inv format` - Format code for all components
- `inv typecheck` - Run type checking for all components
- `inv qa` - Run complete quality assurance pipeline (format + lint + typecheck + test)
- `inv pre-commit` - Run pre-commit checks (format + lint + typecheck)

### Building
- `inv build` - Build all components
- `inv build-backend-data` - Build back-end data accessor package
- `inv build-backend-server` - Build back-end MCP server package
- `inv build-frontend-app` - Build front-end React app for production

### Coverage
- `inv coverage` - Generate coverage reports for all backend components
- `inv coverage-backend-data` - Generate coverage report for data accessor
- `inv coverage-backend-server` - Generate coverage report for MCP server

### Cleanup
- `inv clean` - Clean all build artifacts
- `inv clean-backend-data` - Clean data accessor artifacts
- `inv clean-frontend-app` - Clean React app artifacts (including node_modules)

## Component-Specific Commands

### Backend Data Accessor
```bash
inv test-backend-data    # Run tests with coverage
inv lint-backend-data    # Run linting (black + isort)
inv format-backend-data  # Format code
inv typecheck-backend-data # Type checking with mypy
inv build-backend-data   # Build package with uv
inv coverage-backend-data # Generate HTML coverage report
```

### Backend MCP Server
```bash
inv test-backend-server    # Run tests with coverage
inv lint-backend-server    # Run linting (black + isort)
inv format-backend-server  # Format code
inv typecheck-backend-server # Type checking with mypy
inv build-backend-server   # Build package with uv
inv dev-backend-server     # Start development server
inv coverage-backend-server # Generate HTML coverage report
```

### Frontend MCP Client
```bash
inv test-frontend-client    # Run tests (if available)
inv lint-frontend-client    # Run formatting
inv format-frontend-client  # Format code
inv typecheck-frontend-client # Type checking with mypy
inv build-frontend-client   # Build package with uv
inv dev-frontend-client     # Start development server
```

### Frontend React App
```bash
inv test-frontend-app    # Run tests with Vitest
inv lint-frontend-app    # Run ESLint
inv format-frontend-app  # Auto-fix ESLint issues
inv typecheck-frontend-app # Type checking with TypeScript
inv build-frontend-app   # Build for production
inv dev-frontend-app     # Start Vite development server
```

## Features

### ✨ Enhanced User Experience
- **Colored output** with emojis for better readability
- **Error handling** with clear error messages
- **Progress indicators** for long-running tasks
- **Fallback support** for systems without colorama

### 🔧 Comprehensive Automation
- **Multi-component support** for the entire Music Findr stack
- **Dependency management** with uv and npm
- **Quality assurance** pipeline with formatting, linting, and testing
- **Development workflow** tasks for common development scenarios

### 🚀 Development Workflow
- **One-command setup** for new components
- **Parallel task execution** where appropriate
- **Build artifact management** with cleanup tasks
- **Coverage reporting** for Python components

### 📦 Package Management
- **uv** for Python package management (fast and modern)
- **npm** for Node.js dependencies
- **Automatic dependency detection** based on project structure

## Error Handling

The script includes comprehensive error handling:
- Commands that fail will stop execution with clear error messages
- Exit codes are properly propagated
- Colored output helps identify issues quickly
- Fallback behavior when optional dependencies are missing

## Extending the Script

To add new tasks:
1. Define the task function with the `@task` decorator
2. Use the helper functions for consistent output
3. Add error handling with `run_with_error_handling`
4. Update the status command to include new tasks

Example:
```python
@task
def my_new_task(c):
    """Description of what this task does"""
    print_header("My New Task")
    run_with_error_handling(c, "my-command", description="My Command")
    print_success("Task completed!")
```

## Troubleshooting

### Colorama Not Available
If you see plain text output instead of colors, install colorama:
```bash
pip install colorama
```

### Command Not Found
Ensure you're using `inv` (or `invoke`) to run tasks:
```bash
# Correct
inv test

# Incorrect
python tasks.py test
```

### Permission Issues
Some cleanup tasks may require appropriate permissions. On Unix systems, ensure the script has write permissions to the project directories.

## Contributing

When modifying the tasks script:
1. Test changes with different components
2. Ensure error handling works correctly
3. Update this README if adding new functionality
4. Maintain backward compatibility where possible
