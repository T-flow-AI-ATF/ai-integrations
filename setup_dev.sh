#!/bin/bash
# Unix/Linux/macOS Development Setup Script for T-Flow AI Medical Triage System

echo "================================"
echo "T-Flow AI Development Setup"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11 or 3.12"
    exit 1
fi

echo "✅ Python is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"
echo "🔧 Installing/updating dependencies..."

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r backend/requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found"
    echo "Please copy .env.example to .env and fill in your API keys:"
    echo "  - GROQ_API_KEY"
    echo "  - SUPABASE_URL"
    echo "  - SUPABASE_ANON_KEY"
    echo ""
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "Please edit .env file with your actual API keys"
    fi
else
    echo "✅ .env file found"
fi

echo ""
echo "================================"
echo "Setup complete! 🎉"
echo "================================"
echo ""
echo "To run the development server:"
echo "  1. Make sure .env file has your API keys"
echo "  2. Run: source venv/bin/activate && cd backend && python run_server.py"
echo ""
echo "To run tests:"
echo "  python test.py"
echo "  python backend/system_check.py"
echo ""
echo "API Documentation will be at: http://localhost:8000/docs"
echo "================================"
