#!/bin/bash

# DL+ AI Agent Platform Startup Script
# سكريبت بدء تشغيل منصة DL+ الذكية

echo "=================================="
echo "🤖 DL+ AI Agent Platform"
echo "منصة الوكيل الذكي DL+"
echo "=================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Check if requirements are installed
if ! python3 -c "import dlplus" 2>/dev/null; then
    echo "⚠️  Dependencies not found. Installing..."
    pip install -r requirements.txt
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys"
fi

echo ""
echo "=================================="
echo "🚀 Starting DL+ Server..."
echo "=================================="
echo ""
echo "📡 Server will be available at:"
echo "   - http://localhost:8000"
echo "   - API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 -m uvicorn dlplus.main:app --host 0.0.0.0 --port 8000 --reload
