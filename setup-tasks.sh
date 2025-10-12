#!/bin/bash

# Music Findr Tasks Setup Script
# This script installs the dependencies needed for the improved tasks.py script

echo "🎵 Setting up Music Findr Task Automation..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."

if command -v pip3 &> /dev/null; then
    pip3 install -r requirements-tasks.txt
elif python3 -m pip --version &> /dev/null; then
    python3 -m pip install -r requirements-tasks.txt
else
    echo "❌ Could not find pip to install dependencies."
    exit 1
fi

# Test the installation
echo "🧪 Testing installation..."
if invoke --list &> /dev/null; then
    echo "✅ Task automation setup completed successfully!"
    echo ""
    echo "🚀 Quick start commands:"
    echo "  inv status    - Show project status"
    echo "  inv test      - Run all tests"
    echo "  inv qa        - Run quality assurance pipeline"
    echo "  inv install   - Install all project dependencies"
    echo ""
    echo "📖 For more information, see TASKS_README.md"
else
    echo "❌ Installation test failed. Please check the error messages above."
    exit 1
fi
