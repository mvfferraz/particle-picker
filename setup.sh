#!/bin/bash

echo "=========================================="
echo "Particle Picker Dashboard - Setup"
echo "Author: Matheus Ferraz"
echo "=========================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

if ! command -v make &> /dev/null; then
    echo "Warning: make is not installed"
    echo "Please install make or run manually:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

echo "Installing Particle Picker Dashboard..."
echo ""

make install

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Installation Complete!"
    echo "=========================================="
    echo ""
    echo "To activate the environment:"
    echo "  source venv/bin/activate"
    echo ""
    echo "To run the dashboard:"
    echo "  make run-dashboard"
    echo ""
    echo "To use the CLI:"
    echo "  make run-cli"
    echo ""
    echo "For all commands:"
    echo "  make help"
    echo ""
else
    echo ""
    echo "Installation failed. Please check the errors above."
    exit 1
fi
