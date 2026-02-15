"""
Numerical solver for Burgers' equation using finite differences
"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def solve_burgers_numerical(nx=100, nt=100, nu=0.01, x_range=(-1, 1), t_range=(0, 1)):
    """
    Solve Burgers' equation using Crank-Nicolson finite difference method
    
    Args:
        nx: Number of spatial grid points
        nt: Number of temporal grid points
        nu: Viscosity coefficient
        x_range: Spatial domain
        t_range: Temporal domain
    
    Returns:
        x, t, U where U[i,j] = u(x[j], t[i])
    """
    # Grid
    x = np.linspace(x_range[0], x_range[1], nx)
    t = np.linspace(t_range[0], t_range[1], nt)
    dx = x[1] - x[0]
    dt = t[1] - t[0]
    
    # Initialize solution
    U = np.zeros((nt, nx))
    
    # Initial condition: u(x, 0) = -sin(πx)
    U[0, :] = -np.sin(np.pi * x)
    
    # Boundary conditions: u(-1, t) = u(1, t) = 0
    U[:, 0] = 0
    U[:, -1] = 0
    
    # Time stepping with simple explicit scheme for demonstration
    # For better accuracy, would use implicit or Crank-Nicolson
    r = nu * dt / (dx**2)
    
    for n in range(nt - 1):
        u_old = U[n, :].copy()
        
        # Interior points using FTCS (Forward Time Central Space)
        for i in range(1, nx - 1):
            # Advection term: -u * du/dx (using upwind)
            if u_old[i] > 0:
                du_dx = (u_old[i] - u_old[i-1]) / dx
            else:
                du_dx = (u_old[i+1] - u_old[i]) / dx
            
            # Diffusion term: nu * d2u/dx2
            d2u_dx2 = (u_old[i+1] - 2*u_old[i] + u_old[i-1]) / (dx**2)
            
            # Update
            U[n+1, i] = u_old[i] + dt * (-u_old[i] * du_dx + nu * d2u_dx2)
        
        # Ensure boundary conditions
        U[n+1, 0] = 0
        U[n+1, -1] = 0
    
    return x, t, U


if __name__ == "__main__":
    # Test the numerical solver
    x, t, U = solve_burgers_numerical(nx=50, nt=50, nu=0.01)
    
    print(f"Numerical solution computed:")
    print(f"Grid: {len(x)} x {len(t)}")
    print(f"u(0, 0) = {U[0, len(x)//2]:.6f} (should be 0)")
    print(f"u(0.5, 0) = {U[0, int(0.75*len(x))]:.6f}")
    print(f"Min: {U.min():.6f}, Max: {U.max():.6f}")
    
    # Check initial condition
    x_mid = len(x) // 2
    print(f"\nInitial condition at x=0:")
    print(f"  Numerical: {U[0, x_mid]:.6f}")
    print(f"  Analytical: {-np.sin(np.pi * x[x_mid]):.6f}")
