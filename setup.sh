#!/bin/bash

# Playwright Studies Portal Setup Script
# This script sets up the complete environment for the portal

echo "🎭 Setting up Playwright Studies Portal..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d" " -f2 | cut -d"." -f1,2)
echo "📍 Python version: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your HUGGINGFACE_TOKEN"
fi

# Initialize database
echo "🗄️  Initializing database..."
python init_data.py

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the portal:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the portal: python main.py"
echo ""
echo "🔑 Don't forget to:"
echo "   • Add your HUGGINGFACE_TOKEN to .env file"
echo "   • Visit http://localhost:7860 once started"
echo ""
echo "🎯 Features available:"
echo "   • Cypress to Playwright migration tools"
echo "   • Best practices guidance"
echo "   • OOP & SOLID principles tutorials" 
echo "   • AI-powered assistance (requires token)"
echo "   • Progress tracking"
