# Educational Features Guide

## Overview

The PINN demo now includes comprehensive educational features to help you understand how Physics-Informed Neural Networks work!

## New Features

### 1. 📍 Collocation Points Visualization

**What it shows:** The actual points where the PINN enforces physics and boundary conditions.

**Understanding it:**
- **Blue dots (PDE Points)**: 2000 random points in the (x,t) domain where Burgers' equation must be satisfied
- **Green squares (IC Points)**: 100 points at t=0 where initial condition u(x,0) = -sin(πx) is enforced
- **Pink diamonds (BC Points)**: 100 points at x=±1 where boundary conditions u(±1,t) = 0 are enforced

**Why it matters:** The PINN doesn't need data everywhere—just at these strategic points! The network learns to interpolate and satisfy physics in between.

### 2. 🎬 Solution Animation

**What it shows:** How the solution u(x,t) evolves over time.

**How to use:**
- Drag the time slider to see solution at any time t
- Click "Play" to animate the evolution
- Watch how the initial sine wave decays due to viscosity

**What to observe:**
- At t=0: Initial condition (negative sine wave)
- Over time: Wave amplitude decreases (diffusion)
- The wave shape changes due to nonlinear advection

### 3. Derivative Visualizations

#### ∂u/∂x: Spatial Derivative

**What it shows:** How fast the solution changes in space.

**Physical meaning:**
- Positive (red): Solution increasing to the right
- Negative (blue): Solution decreasing to the right
- Large magnitude: Steep gradients (shock formation)

**Why it's computed:** Used in the advection term u(∂u/∂x) and computed via automatic differentiation!

#### ∂u/∂t: Time Derivative

**What it shows:** How fast the solution changes in time.

**Physical meaning:**
- Positive: Solution increasing over time
- Negative: Solution decreasing over time
- Near zero: Solution approaching steady state

**Why it's computed:** Left side of Burgers' equation: ∂u/∂t + u(∂u/∂x) = ν(∂²u/∂x²)

#### ∂²u/∂x²: Second Spatial Derivative

**What it shows:** The curvature of the solution.

**Physical meaning:**
- Positive (red): Concave up (diffusion increases u)
- Negative (blue): Concave down (diffusion decreases u)
- Magnitude shows strength of diffusion effect

**Why it's computed:** Diffusion term in Burgers' equation: ν(∂²u/∂x²)

### 4. 🎓 How PINN Works - Step by Step

An interactive guide showing the complete PINN workflow:

1. **Input**: (x, t) coordinates
2. **Forward Pass**: Neural network computes u(x,t)
3. **Automatic Differentiation**: Compute all derivatives
4. **Physics Loss**: Check PDE residual
5. **Data Loss**: Check IC and BC
6. **Backpropagation**: Update weights to reduce loss

**Interactive element:** The network architecture display updates when you change hidden layers!

## How to Use Educational Features

### Toggle Display
- Check/uncheck "Show Educational Features" to hide/show all educational panels
- Useful for focusing on main results or diving deep into learning

### Best Learning Workflow

1. **Before Training:**
   - Look at collocation points to see sampling strategy
   - Check step-by-step guide to understand process

2. **During Training:**
   - Watch loss curves decrease
   - Observe which loss component is largest

3. **After Training:**
   - Use animation to understand solution dynamics
   - Compare derivatives with solution
   - Check if residuals are small everywhere

## Understanding the Plots

### What "Good" Looks Like

**Collocation Points:**
- Evenly distributed across domain ✓
- More points = better accuracy (but slower training)

**Solution Animation:**
- Smooth evolution ✓
- Boundary conditions satisfied (u=0 at edges) ✓
- Initial condition matched at t=0 ✓

**Derivatives:**
- Smooth gradients (no jumps) ✓
- Physically reasonable values ✓
- Second derivative shows diffusion pattern ✓

**Residuals:**
- Mostly blue/green (near zero) ✓
- Red areas indicate physics violations (needs more training)

## Interactive Learning Activities

### Activity 1: Watch Physics Enforcement
1. Train for 100 epochs
2. Look at PDE residual plot - probably has red areas
3. Train 500 more epochs
4. Watch residuals turn blue as physics is learned!

### Activity 2: Understand Derivatives
1. After training, look at ∂u/∂x heatmap
2. Use animation to see solution at t=0.5
3. Notice: where solution slopes up, ∂u/∂x is positive!
4. Where solution is curved, ∂²u/∂x² is non-zero

### Activity 3: Collocation Point Experiment
1. Modify `generate_training_data(n_pde=500)` in backend (fewer points)
2. Retrain and compare accuracy
3. Try `n_pde=5000` (more points)
4. Observe: more points = better accuracy but slower training

### Activity 4: Animation Analysis
1. Train with high viscosity (ν=0.1)
2. Watch animation - solution decays quickly
3. Retrain with low viscosity (ν=0.001)
4. Solution decays slowly, may form shocks

## Advanced: Reading the Math

### The PDE Being Solved
```
∂u/∂t + u(∂u/∂x) = ν(∂²u/∂x²)
```

**In the visualizations:**
- ∂u/∂t is shown in "Time Derivative" plot
- ∂u/∂x is shown in "Spatial Derivative" plot
- ∂²u/∂x² is shown in "Second Spatial Derivative" plot

**The residual** measures: |∂u/∂t + u(∂u/∂x) - ν(∂²u/∂x²)|

If PINN is perfect, all three derivative plots should satisfy this equation everywhere!

### Checking Physics Manually

Pick a point, e.g., (x=0, t=0.5):

1. Read ∂u/∂t from time derivative plot
2. Read u and ∂u/∂x from other plots
3. Read ∂²u/∂x² from second derivative plot
4. Compute: ∂u/∂t + u(∂u/∂x) - ν(∂²u/∂x²)
5. Should be ≈ 0 if PINN learned correctly!

## Tips for Teaching/Learning

### For Students
- Start with step-by-step guide
- Use animation to build intuition
- Experiment with different parameters
- Try to predict what derivatives should look like

### For Instructors
- Use collocation points to explain sampling
- Compare derivatives with finite differences
- Show how automatic differentiation works
- Demonstrate physics-informed vs data-driven learning

### For Researchers
- Visualize where training points are needed
- Identify regions with high residuals (need more points)
- Understand convergence behavior
- Debug training issues

## Troubleshooting

**Q: Derivatives look noisy?**
A: Network needs more training or larger architecture

**Q: Animation shows discontinuities?**
A: Increase number of points in prediction grid (nx, nt)

**Q: Collocation points seem random?**
A: They are! Random sampling helps generalization

**Q: Step-by-step guide not showing network?**
A: Make sure you entered valid hidden layers (e.g., "32,32,32")

## Summary

These educational features transform the PINN demo from a black box into a transparent learning tool. You can now:

✅ See where physics is enforced (collocation points)
✅ Watch solution evolve (animation)
✅ Understand derivatives (automatic differentiation)
✅ Follow the complete process (step-by-step guide)
✅ Verify physics is satisfied (compare derivative plots)

**The goal:** Make PINNs understandable, tangible, and intuitive!
