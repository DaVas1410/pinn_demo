#!/bin/bash

echo "🚀 Setting up PINN Demo Environment"
echo "===================================="

# Create conda environment
echo "📦 Creating conda environment 'pinn'..."
conda create -n pinn python=3.10 -y

# Install dependencies
echo "📥 Installing Python dependencies..."
conda run -n pinn pip install torch numpy scipy flask flask-cors matplotlib

echo ""
echo "✨ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. conda activate pinn"
echo "  2. cd backend"
echo "  3. python app.py"
echo "  4. Open http://localhost:5000 in your browser"
