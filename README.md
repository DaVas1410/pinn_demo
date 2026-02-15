# 🧠 Physics-Informed Neural Networks (PINN) Demo

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An interactive web application demonstrating how Physics-Informed Neural Networks solve partial differential equations using deep learning.**

Experience the power of physics-informed machine learning with real-time training visualization, automatic differentiation, and comprehensive educational features.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Usage Guide](#-usage-guide)
- [Architecture](#-architecture)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Tech Stack](#-tech-stack)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 Overview

This application demonstrates **Physics-Informed Neural Networks (PINNs)** - a revolutionary approach that embeds physical laws directly into neural network training. Instead of relying solely on data, PINNs enforce physics through the loss function.

### What Problem Does It Solve?

This demo solves **Burgers' equation**, a fundamental nonlinear PDE that models fluid dynamics:

```
∂u/∂t + u(∂u/∂x) = ν(∂²u/∂x²)
```

Where:
- `u(x,t)` is the velocity field
- `ν` is the kinematic viscosity
- The equation combines advection `u(∂u/∂x)` and diffusion `ν(∂²u/∂x²)`

### Why PINNs Matter

Traditional numerical methods require mesh generation and can be computationally expensive. **PINNs offer advantages:**
- ✅ Mesh-free approach
- ✅ Automatic differentiation via neural networks
- ✅ Can handle complex geometries
- ✅ Incorporates noisy data and physics simultaneously

---

## ✨ Features

### Core Capabilities

- 🎓 **Real-Time Training** - Watch neural network learn PDEs with live loss visualization
- 📊 **10 Interactive Plots** - Comprehensive visualization suite powered by Plotly.js
- ⚖️ **Solution Comparison** - PINN vs numerical finite difference solver
- 📈 **Error Analysis** - Absolute error heatmaps and metrics
- 🔍 **Residual Visualization** - See where physics laws are violated

### Educational Features

- 📍 **Collocation Points** - Visualize 2000+ training points (PDE, IC, BC)
- 🎬 **Solution Animation** - Time-slider to watch wave evolution
- ∂ **Derivative Heatmaps** - Three automatic differentiation visualizations:
  - `∂u/∂x` (spatial derivative)
  - `∂u/∂t` (temporal derivative)  
  - `∂²u/∂x²` (second-order derivative)
- 📚 **Step-by-Step Guide** - Interactive workflow explanation
- 🎛️ **Parameter Controls** - Adjust viscosity, epochs, architecture

---

## 🎬 Demo

### Live Application

**Deployed on Render:** [Your Deployment URL]

### Visual Workflow

1. **Set Parameters** → Viscosity (0.001-0.1), Epochs (500-3000), Network size
2. **Train PINN** → Watch losses decrease in real-time
3. **Compare Solutions** → PINN vs Numerical solver
4. **Explore Physics** → Derivatives, residuals, collocation points
5. **Animate** → See solution evolve over time

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (3.11 recommended)
- Conda or pip
- 2GB RAM minimum

### Installation

```bash
# 1. Clone repository
git clone https://github.com/DaVas1410/pinn_demo.git
cd pinn_demo

# 2. Create virtual environment (Option A: Conda)
conda create -n pinn python=3.11 -y
conda activate pinn

# 2. OR create virtual environment (Option B: venv)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
cd backend
python app.py
```

### Access Application

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🧮 How It Works

### PINN Loss Function

The magic of PINNs lies in the loss function that combines **physics** and **data**:

```python
L_total = λ_PDE · L_PDE + λ_IC · L_IC + λ_BC · L_BC
```

#### 1. Physics Loss (PDE Residual)
```
L_PDE = mean(|∂u/∂t + u(∂u/∂x) - ν(∂²u/∂x²)|²)
```
Enforces Burgers' equation at interior collocation points.

#### 2. Initial Condition Loss
```
L_IC = mean(|u(x, 0) + sin(πx)|²)
```
Enforces initial condition: `u(x,0) = -sin(πx)`

#### 3. Boundary Condition Loss
```
L_BC = mean(|u(-1, t)|² + |u(1, t)|²)
```
Enforces zero Dirichlet boundaries: `u(±1, t) = 0`

### Automatic Differentiation

PyTorch's autograd computes exact derivatives:

```python
u = neural_network(x, t)
u_t = torch.autograd.grad(u, t)[0]      # ∂u/∂t
u_x = torch.autograd.grad(u, x)[0]      # ∂u/∂x
u_xx = torch.autograd.grad(u_x, x)[0]   # ∂²u/∂x²
```

No finite differences needed! 🎉

---

## 📖 Usage Guide

### Basic Workflow

1. **Start Training**
   - Click "Start Training" button
   - Default parameters work well for quick demo

2. **Monitor Progress**
   - Watch **Loss Curves** panel - all losses should decrease
   - Training complete when losses plateau (typically 1000-3000 epochs)

3. **Analyze Results**
   - **PINN Solution**: Neural network prediction
   - **Numerical Solution**: Finite difference reference
   - **Error Heatmap**: Absolute difference between solutions
   - **PDE Residuals**: Where physics is violated (should be near zero)

4. **Explore Educational Features** (toggle on)
   - **Collocation Points**: See where network is trained
   - **Animation**: Play button to watch solution evolve
   - **Derivatives**: Understand how PINN computes gradients

### Parameter Tuning

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| **Viscosity (ν)** | 0.01 | Lower = sharper gradients (harder to learn) |
| **Epochs** | 1000-3000 | More epochs = better accuracy |
| **Learning Rate** | 0.001 | Too high = instability, too low = slow |
| **Hidden Layers** | [64,64,64,64] | Deeper/wider = more capacity |

### Tips for Best Results

- ✅ **Quick demo**: 500 epochs, ν=0.01, [32,32,32]
- ✅ **Best accuracy**: 3000 epochs, ν=0.01, [64,64,64,64]
- ✅ **Low viscosity (ν=0.001)**: Use 3000+ epochs, deeper network
- ⚠️ **High loss?** Increase epochs or network size

---

## 🏗️ Architecture

### Project Structure

```
pinn_demo/
├── backend/                    # Python Flask API
│   ├── app.py                  # 7 REST endpoints
│   ├── pinn_model.py           # PyTorch PINN implementation
│   ├── numerical_solver.py     # Finite difference solver
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # Interactive web UI
│   ├── templates/
│   │   └── index.html          # Main page (10 visualization panels)
│   └── static/
│       ├── app.js              # API calls, plotting, animations
│       └── style.css           # Responsive design
│
├── requirements.txt            # Root dependencies (deployment)
├── runtime.txt                 # Python version specification
├── start.sh                    # Production startup script
└── README.md                   # This file
```

### System Architecture

```
┌─────────────┐      HTTP      ┌─────────────┐
│   Browser   │ ◄────────────► │ Flask API   │
│  (Plotly)   │   JSON/REST    │  (Python)   │
└─────────────┘                └─────────────┘
                                      │
                                      ▼
                         ┌────────────────────────┐
                         │   PINN Model (PyTorch) │
                         │  • Forward pass        │
                         │  • Auto-differentiation│
                         │  • Loss computation    │
                         │  • Backpropagation     │
                         └────────────────────────┘
```

### Neural Network Architecture

```
Input Layer:  [x, t]  (2 neurons)
              ↓
Hidden 1:     [64 neurons] + Tanh activation
              ↓
Hidden 2:     [64 neurons] + Tanh activation
              ↓
Hidden 3:     [64 neurons] + Tanh activation
              ↓
Hidden 4:     [64 neurons] + Tanh activation
              ↓
Output:       [u]    (1 neuron - velocity field)
```

---

## 🌐 API Endpoints

### 1. `POST /api/train`
Start PINN training in background thread.

**Request:**
```json
{
  "viscosity": 0.01,
  "epochs": 1000,
  "learning_rate": 0.001,
  "hidden_layers": [64, 64, 64, 64]
}
```

**Response:**
```json
{
  "status": "training_started",
  "message": "Training started with 1000 epochs"
}
```

### 2. `GET /api/training_status`
Check training progress.

**Response:**
```json
{
  "is_training": true,
  "current_epoch": 523,
  "total_epochs": 1000,
  "current_loss": 0.0023
}
```

### 3. `GET /api/get_losses`
Retrieve loss history.

**Response:**
```json
{
  "total_losses": [0.523, 0.412, ...],
  "pde_losses": [0.321, 0.245, ...],
  "ic_losses": [0.102, 0.089, ...],
  "bc_losses": [0.100, 0.078, ...]
}
```

### 4. `GET /api/get_solution?nx=100&nt=100`
Get PINN predictions on grid.

**Response:**
```json
{
  "x": [-1.0, -0.98, ..., 1.0],
  "t": [0.0, 0.01, ..., 1.0],
  "u_pred": [[...], [...], ...],
  "u_numerical": [[...], [...], ...],
  "error": [[...], [...], ...]
}
```

### 5. `GET /api/get_residuals?nx=50&nt=50`
Get PDE residual heatmap.

**Response:**
```json
{
  "x": [...],
  "t": [...],
  "residuals": [[...], [...], ...]
}
```

### 6. `GET /api/get_collocation_points`
Get training data locations.

**Response:**
```json
{
  "x_pde": [...],
  "t_pde": [...],
  "x_ic": [...],
  "t_ic": [...],
  "x_bc": [...],
  "t_bc": [...]
}
```

### 7. `GET /api/get_derivatives?nx=50&nt=50`
Get derivative visualizations.

**Response:**
```json
{
  "x": [...],
  "t": [...],
  "u_x": [[...], [...], ...],
  "u_t": [[...], [...], ...],
  "u_xx": [[...], [...], ...]
}
```

---

## 🚢 Deployment

### Local Development

```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

### Production (Render.com) - FREE

1. **Push to GitHub** (already done ✅)

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect repository: `DaVas1410/pinn_demo`
   - Settings:
     - **Name**: `pinn-demo`
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd backend && gunicorn app:app`
     - **Instance Type**: Free

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build
   - Get URL: `https://pinn-demo.onrender.com`

### Alternative Platforms

- **Railway.app**: Similar free tier, faster cold starts
- **Fly.io**: Free tier with persistent storage
- **Heroku**: $5/month minimum (no free tier)

**Note**: Free tiers sleep after 15min inactivity (30-60s cold start).

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Core language
- **PyTorch 2.0+** - Deep learning framework with autograd
- **Flask 3.0** - Lightweight web framework
- **NumPy** - Numerical computing
- **SciPy** - Scientific computing (finite differences)
- **Gunicorn** - Production WSGI server

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive design with grid/flexbox
- **JavaScript ES6+** - Modern async/await, fetch API
- **Plotly.js** - Interactive scientific visualizations

### DevOps
- **Git** - Version control
- **Conda/pip** - Package management
- **Render.com** - Cloud deployment

---

## 🐛 Troubleshooting

### Installation Issues

**Problem**: `ModuleNotFoundError: No module named 'torch'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `conda: command not found`
```bash
# Solution: Use venv instead
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Training Issues

**Problem**: Loss stays high (>0.1 after 1000 epochs)
```
Solutions:
1. Increase epochs to 3000
2. Use deeper network: [64, 64, 64, 64]
3. Reduce learning rate to 0.0005
4. Check viscosity isn't too low (<0.001)
```

**Problem**: Solutions look flat/incorrect
```
Solutions:
1. Wait for more epochs (PINN needs time)
2. Check browser console for JavaScript errors
3. Refresh page and retrain
```

**Problem**: Training hangs/freezes
```
Solutions:
1. Refresh browser
2. Restart Flask server
3. Check server logs in terminal
```

### Deployment Issues

**Problem**: Render build fails with PyTorch error
```
Solution: Already fixed with runtime.txt (Python 3.11)
If still fails, check requirements.txt has torch>=2.0.0
```

**Problem**: App works locally but not on Render
```
Solutions:
1. Check Render logs (click "Logs" tab)
2. Verify environment variables (if any)
3. Ensure PORT is not hardcoded in app.py
```

**Problem**: 404 errors on deployed app
```
Solution: Check Start Command is: cd backend && gunicorn app:app
```

---

## 🤝 Contributing

Contributions welcome! This is an educational project.

### Ideas for Enhancement

- [ ] Add more PDEs (heat equation, wave equation, Navier-Stokes)
- [ ] Implement L-BFGS optimizer for faster convergence
- [ ] Add uncertainty quantification
- [ ] Export trained models
- [ ] Multi-GPU training support
- [ ] Add 2D PDEs with contour plots
- [ ] Comparison with FEM/FVM methods

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

**TL;DR**: Free to use, modify, and distribute. Just keep the license notice.

---

## 🙏 Acknowledgments

### Research

- **Raissi et al. (2019)** - [Physics-Informed Neural Networks](https://doi.org/10.1016/j.jcp.2018.10.045)
  - Original PINN paper that pioneered this approach
  
- **Raissi et al. (2017)** - [Hidden Physics Models](https://arxiv.org/abs/1708.07469)
  - Machine learning of linear differential equations

### Tools & Libraries

- **PyTorch Team** - Automatic differentiation framework
- **Plotly.js** - Beautiful interactive visualizations
- **Flask** - Minimalist web framework
- **Render.com** - Free hosting platform

### Inspiration

- **Physics-Informed Machine Learning** community
- **Scientific ML** (SciML) ecosystem
- Countless researchers advancing ML for science

---

## 📚 Further Reading

### Papers
- [Physics-Informed Neural Networks: A Deep Learning Framework](https://www.sciencedirect.com/science/article/pii/S0021999118307125)
- [When and why PINNs fail to train](https://doi.org/10.1016/j.jcp.2021.110768)

### Tutorials
- [DeepXDE Documentation](https://deepxde.readthedocs.io/)
- [PyTorch Autograd Tutorial](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html)

### Courses
- [Stanford CS230: Deep Learning](https://cs230.stanford.edu/)
- [Scientific Machine Learning (MIT)](https://github.com/mitmath/18337)

---

## 📞 Contact & Support

**Issues**: [GitHub Issues](https://github.com/DaVas1410/pinn_demo/issues)  
**Discussions**: [GitHub Discussions](https://github.com/DaVas1410/pinn_demo/discussions)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

*Making physics-informed machine learning accessible to everyone*

[Report Bug](https://github.com/DaVas1410/pinn_demo/issues) · [Request Feature](https://github.com/DaVas1410/pinn_demo/issues) · [Documentation](EDUCATIONAL_FEATURES.md)

</div>
