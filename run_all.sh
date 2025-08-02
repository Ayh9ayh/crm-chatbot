#!/bin/bash

echo "🚀 Starting CRM Chatbot Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Setup MongoDB if needed
if [ -f ".env" ]; then
    echo "🗄️ Setting up MongoDB..."
    python setup_mongodb.py
else
    echo "⚠️ Please create .env file with your MongoDB credentials"
    exit 1
fi

# Start backend
echo "🔧 Starting backend server..."
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend..."
streamlit run frontend/app.py

# Cleanup
kill $BACKEND_PID