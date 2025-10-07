from invoke import task
import os

DATA_ACCESSOR_DIR = os.path.join("back-end", "data_accessor")
MCP_SERVER_DIR = os.path.join("back-end", "mcp_server")

def run_in_dir(ctx, command, directory):
    """Run a command in a specific directory"""
    with ctx.cd(directory):
        ctx.run(command)

@task
def install(ctx):
    """Install all dependencies"""
    run_in_dir(ctx, "hatch env create", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch env create", MCP_SERVER_DIR)

@task
def test(ctx):
    """Run tests for both packages"""
    data_accessor_cmd = 'powershell "$env:PYTHONPATH=\'src\'; hatch run dev:test"'
    mcp_server_cmd = 'powershell "$env:PYTHONPATH=\'src;../data_accessor\'; hatch run dev:test"'
    run_in_dir(ctx, data_accessor_cmd, DATA_ACCESSOR_DIR)
    run_in_dir(ctx, mcp_server_cmd, MCP_SERVER_DIR)

@task
def lint(ctx):
    """Run linting for both packages"""
    run_in_dir(ctx, "hatch run dev:lint", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch run dev:lint", MCP_SERVER_DIR)

@task
def format(ctx):
    """Format code for both packages"""
    run_in_dir(ctx, "hatch run dev:format", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch run dev:format", MCP_SERVER_DIR)

@task
def typecheck(ctx):
    """Type checking for both packages"""
    run_in_dir(ctx, "hatch run dev:typecheck", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch run dev:typecheck", MCP_SERVER_DIR)

@task
def all(ctx):
    """Run all checks (format, lint, typecheck, test)"""
    run_in_dir(ctx, "hatch run dev:all", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch run dev:all", MCP_SERVER_DIR)

@task
def clean(ctx):
    """Clean up generated files"""
    patterns = [
        "**/__pycache__",
        "**/.pytest_cache",
        "**/.coverage",
        "**/htmlcov",
        "**/.mypy_cache",
        "**/dist",
        "**/build",
        "**/*.egg-info"
    ]
    for pattern in patterns:
        ctx.run(f'powershell "Get-ChildItem -Path . -Recurse -Directory -Filter {pattern} | Remove-Item -Recurse -Force"')

@task
def setup(ctx):
    """Development setup (install and setup pre-commit)"""
    install(ctx)
    ctx.run("pre-commit install")

@task
def build(ctx):
    """Build packages"""
    run_in_dir(ctx, "hatch build", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch build", MCP_SERVER_DIR)

@task
def develop(ctx):
    """Install packages in development mode"""
    run_in_dir(ctx, "hatch run dev:pip install -e .", DATA_ACCESSOR_DIR)
    run_in_dir(ctx, "hatch run dev:pip install -e .", MCP_SERVER_DIR)
