# PINN Demonstration Applet

An interactive web application demonstrating how Physics-Informed Neural Networks (PINNs) solve partial differential equations, specifically **Burgers' equation**.

## 🎯 What This Demo Shows

This applet demonstrates:
- How PINNs embed physical laws (PDEs) into neural network training
- Real-time training visualization with loss components (PDE, IC, BC)
- Comparison between PINN predictions and numerical solutions
- PDE residual visualization showing where physics is satisfied
- Interactive parameter tuning (viscosity, network architecture, learning rate)

### 🎓 New Educational Features!
- **Collocation Points Visualization**: See where the PINN enforces physics (2000 PDE points, 100 IC, 100 BC)
- **Solution Animation**: Watch the wave evolve over time with interactive slider
- **Derivative Visualizations**: See ∂u/∂x, ∂u/∂t, ∂²u/∂x² computed by automatic differentiation
- **Interactive Comparison**: Slide through time to compare PINN with numerical solver
- **Step-by-Step Guide**: Understand the complete PINN workflow from input to backprop

See [EDUCATIONAL_FEATURES.md](EDUCATIONAL_FEATURES.md) for detailed guide!

## 🔬 Burgers' Equation

The demo solves the 1D viscous Burgers' equation:

```
∂u/∂t + u(∂u/∂x) = ν(∂²u/∂x²)
```

With:
- Initial condition: `u(x, 0) = -sin(πx)`
- Boundary conditions: `u(±1, t) = 0`
- Domain: `x ∈ [-1, 1]`, `t ∈ [0, 1]`

## 🚀 Setup

### 1. Create Conda Environment

```bash
cd pinn_demo
conda create -n pinn python=3.10 -y
conda activate pinn
```

### 2. Install Dependencies

```bash
cd backend
pip install torch numpy scipy flask flask-cors matplotlib
```

Or use the setup script:
```bash
bash setup.sh
conda activate pinn
```

### 3. Run the Application

```bash
cd backend
python app.py
```

The server will start at `http://localhost:5000`

Open your browser and navigate to `http://localhost:5000` to use the interactive demo!

## 💻 Usage

1. **Adjust Parameters**:
   - **Viscosity (ν)**: Controls diffusion (0.001 - 0.1). Lower values make the problem more nonlinear
   - **Epochs**: Number of training iterations (100 - 10000)
   - **Learning Rate**: Optimizer learning rate (0.0001 - 0.1)
   - **Hidden Layers**: Network architecture (e.g., "32,32,32")

2. **Start Training**: Click "Start Training" to begin PINN training

3. **Monitor Progress**:
   - Watch loss curves decrease in real-time
   - See current epoch and loss values
   - Observe solution evolution

4. **View Results** (after training):
   - **PINN Solution**: Neural network prediction
   - **Analytical Solution**: Ground truth
   - **Error**: Absolute difference
   - **PDE Residual**: Shows where physics is violated

## 📊 Understanding the Visualizations

### Loss Components
- **Total Loss**: Sum of all loss terms
- **PDE Loss**: Physics equation residual (how well PDE is satisfied)
- **IC Loss**: Initial condition error
- **BC Loss**: Boundary condition error

### Heatmaps
- **Solution u(x,t)**: Shows how the solution evolves in space and time
- **Residual**: Red/blue shows where PDE is violated (should approach 0)
- **Error**: Difference from analytical solution

## 🧠 How PINNs Work

1. **Network Input**: Spatial and temporal coordinates (x, t)
2. **Network Output**: Solution u(x, t)
3. **Loss Function**:
   ```
   Loss = MSE(PDE_residual) + MSE(IC_error) + MSE(BC_error)
   ```
4. **Training**: Backpropagation minimizes all loss components simultaneously
5. **Result**: Network learns to satisfy both data and physics constraints

## 🎓 Key Concepts

- **Collocation Points**: Random points in (x,t) domain where PDE is enforced
- **Automatic Differentiation**: Used to compute derivatives (∂u/∂x, ∂u/∂t, ∂²u/∂x²)
- **Physics-Informed Loss**: Combines data-driven and physics-driven objectives

## 🛠️ Project Structure

```
pinn_demo/
├── backend/
│   ├── app.py              # Flask API server
│   ├── pinn_model.py       # PINN implementation
│   └── requirements.txt    # Python dependencies
└── frontend/
    ├── templates/
    │   └── index.html      # Main HTML page
    └── static/
        ├── style.css       # Styling
        └── app.js          # Frontend logic
```

## 📚 References

- [Physics-Informed Neural Networks (Raissi et al., 2019)](https://www.sciencedirect.com/science/article/pii/S0021999118307125)
- [Burgers' Equation](https://en.wikipedia.org/wiki/Burgers%27_equation)

## ⚡ Tips

- Start with default parameters to see basic behavior
- Lower viscosity (ν) makes the problem harder (more nonlinear)
- More epochs generally improve accuracy but take longer
- Try different network architectures (e.g., "64,64,64,64" for deeper network)
- Watch the residual plot - it should become mostly blue (near zero) when trained well

## 🐛 Troubleshooting

- **Training too slow**: Reduce epochs or use simpler network architecture
- **Poor accuracy**: Increase epochs, adjust learning rate, or use deeper network
- **NaN losses**: Reduce learning rate or increase viscosity
- **High residuals**: Train longer or increase network capacity

---

Built with ❤️ using PyTorch, Flask, and Plotly.js
