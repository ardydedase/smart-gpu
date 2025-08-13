#!/bin/bash

# Smart GPU Package Publishing Script
# This script builds and publishes the smart-gpu package to PyPI

set -e  # Exit on any error

echo "🚀 Smart GPU Package Publishing Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Virtual environment not detected. Please activate your virtual environment first."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install/upgrade build tools
print_status "Installing/upgrading build tools..."
pip install --upgrade build twine

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf dist/ build/ src/*.egg-info/

# Run tests
print_status "Running tests..."
python -m pytest tests/ -v --tb=short

# Build the package
print_status "Building package..."
python -m build

# Check the built package
print_status "Checking package metadata..."
twine check dist/*

# Show package info
print_status "Package built successfully!"
echo "Files created:"
ls -la dist/

echo
print_status "Package contents:"
tar -tzf dist/*.tar.gz | head -20

echo
print_warning "Ready to publish to PyPI!"
echo
echo "To publish to Test PyPI (recommended first):"
echo "  twine upload --repository testpypi dist/*"
echo
echo "To publish to PyPI:"
echo "  twine upload dist/*"
echo
echo "To test install from Test PyPI:"
echo "  pip install --index-url https://test.pypi.org/simple/ smart-gpu"
echo
echo "To test install from PyPI:"
echo "  pip install smart-gpu"
echo
read -p "Do you want to publish to Test PyPI now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Publishing to Test PyPI..."
    twine upload --repository testpypi dist/*
    print_status "Published to Test PyPI successfully!"
    echo
    print_status "You can now test the installation with:"
    echo "  pip install --index-url https://test.pypi.org/simple/ smart-gpu"
fi

echo
print_status "Publishing script completed!"
