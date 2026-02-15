# 🧠 Physics-Informed Neural Networks (PINN) Demo

Interactive web application demonstrating how Physics-Informed Neural Networks solve Burgers' equation with real-time training and educational visualizations.

## Features

- 🎓 Real-time neural network training
- 📊 10 interactive visualizations  
- 🎬 Solution animation with time slider
- ∂ Automatic differentiation visualizations
- 📍 Collocation points display
- ⚖️ Comparison with numerical solver

## Quick Start

```bash
git clone https://github.com/yourusername/pinn_demo.git
cd pinn_demo
conda create -n pinn python=3.10 -y
conda activate pinn
pip install -r requirements.txt
cd backend && python app.py
# Open http://localhost:5000
```

## Documentation

- **[EDUCATIONAL_FEATURES.md](EDUCATIONAL_FEATURES.md)** - Learning guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Hosting instructions
- **[ACCURACY_FIX.md](ACCURACY_FIX.md)** - Technical details

## Tech Stack

Python • PyTorch • Flask • JavaScript • Plotly.js • NumPy

## License

MIT
