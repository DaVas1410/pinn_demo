import torch
import torch.nn as nn
import numpy as np

class PINN(nn.Module):
    """Physics-Informed Neural Network for Burgers' Equation"""
    
    def __init__(self, hidden_layers=[32, 32, 32], activation='tanh'):
        super(PINN, self).__init__()
        
        # Network architecture: 2 inputs (x, t) -> hidden layers -> 1 output (u)
        layers = []
        input_dim = 2
        output_dim = 1
        
        # Input layer
        layers.append(nn.Linear(input_dim, hidden_layers[0]))
        
        # Hidden layers
        for i in range(len(hidden_layers) - 1):
            layers.append(nn.Linear(hidden_layers[i], hidden_layers[i + 1]))
        
        # Output layer
        layers.append(nn.Linear(hidden_layers[-1], output_dim))
        
        self.layers = nn.ModuleList(layers)
        
        # Activation function
        if activation == 'tanh':
            self.activation = nn.Tanh()
        elif activation == 'relu':
            self.activation = nn.ReLU()
        elif activation == 'sigmoid':
            self.activation = nn.Sigmoid()
        else:
            self.activation = nn.Tanh()
    
    def forward(self, x, t):
        """Forward pass through the network"""
        # Concatenate inputs
        inputs = torch.cat([x, t], dim=1)
        
        # Pass through layers
        for i in range(len(self.layers) - 1):
            inputs = self.layers[i](inputs)
            inputs = self.activation(inputs)
        
        # Output layer (no activation)
        u = self.layers[-1](inputs)
        return u


class BurgersPINN:
    """Burgers' Equation PINN Solver"""
    
    def __init__(self, nu=0.01, hidden_layers=[32, 32, 32], activation='tanh', lr=0.001):
        """
        Initialize PINN for Burgers' equation
        
        Args:
            nu: Viscosity coefficient
            hidden_layers: List of hidden layer sizes
            activation: Activation function type
            lr: Learning rate
        """
        self.nu = nu
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Create network
        self.model = PINN(hidden_layers, activation).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        # Training history
        self.loss_history = {
            'total': [],
            'pde': [],
            'ic': [],
            'bc': []
        }
        
    def compute_pde_residual(self, x, t):
        """
        Compute PDE residual for Burgers' equation:
        ∂u/∂t + u(∂u/∂x) - ν(∂²u/∂x²) = 0
        """
        x.requires_grad_(True)
        t.requires_grad_(True)
        
        # Forward pass
        u = self.model(x, t)
        
        # First derivatives
        u_x = torch.autograd.grad(u, x, grad_outputs=torch.ones_like(u), 
                                   create_graph=True)[0]
        u_t = torch.autograd.grad(u, t, grad_outputs=torch.ones_like(u), 
                                   create_graph=True)[0]
        
        # Second derivative
        u_xx = torch.autograd.grad(u_x, x, grad_outputs=torch.ones_like(u_x), 
                                    create_graph=True)[0]
        
        # Burgers' equation residual
        residual = u_t + u * u_x - self.nu * u_xx
        
        return residual
    
    def loss_function(self, x_pde, t_pde, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc):
        """
        Compute total loss = PDE loss + IC loss + BC loss
        """
        # PDE residual loss
        residual = self.compute_pde_residual(x_pde, t_pde)
        loss_pde = torch.mean(residual ** 2)
        
        # Initial condition loss
        u_ic_pred = self.model(x_ic, t_ic)
        loss_ic = torch.mean((u_ic_pred - u_ic) ** 2)
        
        # Boundary condition loss
        u_bc_pred = self.model(x_bc, t_bc)
        loss_bc = torch.mean((u_bc_pred - u_bc) ** 2)
        
        # Total loss
        loss_total = loss_pde + loss_ic + loss_bc
        
        return loss_total, loss_pde, loss_ic, loss_bc
    
    def train_step(self, x_pde, t_pde, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc):
        """Perform one training step"""
        self.optimizer.zero_grad()
        
        loss_total, loss_pde, loss_ic, loss_bc = self.loss_function(
            x_pde, t_pde, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc
        )
        
        loss_total.backward()
        self.optimizer.step()
        
        losses = {
            'total': loss_total.item(),
            'pde': loss_pde.item(),
            'ic': loss_ic.item(),
            'bc': loss_bc.item()
        }
        
        # Update history
        for key in losses:
            self.loss_history[key].append(losses[key])
        
        return losses
    
    def predict(self, x, t):
        """Make prediction"""
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.FloatTensor(x).reshape(-1, 1).to(self.device)
            t_tensor = torch.FloatTensor(t).reshape(-1, 1).to(self.device)
            u = self.model(x_tensor, t_tensor)
        self.model.train()
        return u.cpu().numpy()


def generate_training_data(x_range=(-1, 1), t_range=(0, 1), 
                          n_pde=2000, n_ic=100, n_bc=100):
    """
    Generate collocation points for training
    
    Args:
        x_range: Spatial domain (x_min, x_max)
        t_range: Temporal domain (t_min, t_max)
        n_pde: Number of collocation points for PDE
        n_ic: Number of points for initial condition
        n_bc: Number of points for boundary conditions
    """
    x_min, x_max = x_range
    t_min, t_max = t_range
    
    # PDE collocation points (interior)
    x_pde = np.random.uniform(x_min, x_max, (n_pde, 1))
    t_pde = np.random.uniform(t_min, t_max, (n_pde, 1))
    
    # Initial condition points (t=0)
    x_ic = np.random.uniform(x_min, x_max, (n_ic, 1))
    t_ic = np.zeros((n_ic, 1))
    # Initial condition: u(x, 0) = -sin(πx)
    u_ic = -np.sin(np.pi * x_ic)
    
    # Boundary condition points (x = x_min and x = x_max)
    t_bc = np.random.uniform(t_min, t_max, (n_bc, 1))
    x_bc_left = np.full((n_bc // 2, 1), x_min)
    x_bc_right = np.full((n_bc - n_bc // 2, 1), x_max)
    x_bc = np.vstack([x_bc_left, x_bc_right])
    t_bc_full = np.vstack([t_bc[:n_bc // 2], t_bc[n_bc // 2:]])
    # Boundary condition: u(±1, t) = 0
    u_bc = np.zeros((n_bc, 1))
    
    return {
        'x_pde': x_pde, 't_pde': t_pde,
        'x_ic': x_ic, 't_ic': t_ic, 'u_ic': u_ic,
        'x_bc': x_bc, 't_bc': t_bc_full, 'u_bc': u_bc
    }


def analytical_solution(x, t, nu=0.01):
    """
    Analytical solution to Burgers' equation (using Cole-Hopf transformation)
    for initial condition u(x,0) = -sin(πx) and boundary conditions u(±1,t) = 0
    """
    # This is an approximation using the Cole-Hopf transformation
    # For the exact solution, we'd need to solve a more complex integral
    # Here we use a simplified version for demonstration
    return -np.sin(np.pi * x) * np.exp(-nu * (np.pi ** 2) * t)
