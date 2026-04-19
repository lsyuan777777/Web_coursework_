#!/bin/bash
# CosmicLens API - Quick Setup Script
# This script helps set up the project on a Unix/Linux/macOS system

set -e  # Exit on error

echo "=============================================="
echo "  🌌 CosmicLens API - Quick Setup"
echo "=============================================="

# Check Python version
echo ""
echo "[1/6] Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 is required but not installed."
    echo "  Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

# Check PostgreSQL
echo ""
echo "[2/6] Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✓ PostgreSQL found"
    echo "  Note: Make sure PostgreSQL is running and you have created the database"
    echo "  Run: createdb cosmiclens"
else
    echo "⚠ PostgreSQL not found in PATH"
    echo "  Please install PostgreSQL and create the database:"
    echo "  - macOS: brew install postgresql && brew services start postgresql"
    echo "  - Ubuntu: sudo apt install postgresql"
    echo "  Then run: createdb cosmiclens"
fi

# Create virtual environment
echo ""
echo "[3/6] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[4/6] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "[5/6] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Copy environment file
echo ""
echo "[6/6] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠ IMPORTANT: Please edit .env and set your database credentials:"
    echo "  DATABASE_USER=your_username"
    echo "  DATABASE_PASSWORD=your_password"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=============================================="
echo "  ✅ Setup Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your database credentials"
echo "2. Create PostgreSQL database: createdb cosmiclens"
echo "3. Download the dataset from Kaggle:"
echo "   https://www.kaggle.com/datasets/ahsanneural/nasa-astronomy-picture-of-the-day-1995-2026"
echo "4. Initialize database: python -m app.scripts.init_db"
echo "5. Run the server: uvicorn app.main:app --reload"
echo ""
echo "API will be available at:"
echo "  - API: http://localhost:8000"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
