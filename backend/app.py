from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import torch
import numpy as np
from pinn_model import BurgersPINN, generate_training_data
from numerical_solver import solve_burgers_numerical
import threading
import time

app = Flask(__name__, template_folder='../frontend/templates', 
            static_folder='../frontend/static')
CORS(app)

# Global variables for training state
training_state = {
    'is_training': False,
    'current_epoch': 0,
    'pinn': None,
    'training_data': None,
    'stop_requested': False
}

def train_worker(epochs, nu, hidden_layers, lr):
    """Background worker for training"""
    global training_state
    
    # Initialize PINN
    pinn = BurgersPINN(nu=nu, hidden_layers=hidden_layers, lr=lr)
    training_state['pinn'] = pinn
    
    # Generate training data
    data = generate_training_data()
    training_state['training_data'] = data
    
    # Convert to tensors
    device = pinn.device
    x_pde = torch.FloatTensor(data['x_pde']).to(device)
    t_pde = torch.FloatTensor(data['t_pde']).to(device)
    x_ic = torch.FloatTensor(data['x_ic']).to(device)
    t_ic = torch.FloatTensor(data['t_ic']).to(device)
    u_ic = torch.FloatTensor(data['u_ic']).to(device)
    x_bc = torch.FloatTensor(data['x_bc']).to(device)
    t_bc = torch.FloatTensor(data['t_bc']).to(device)
    u_bc = torch.FloatTensor(data['u_bc']).to(device)
    
    # Training loop
    for epoch in range(epochs):
        if training_state['stop_requested']:
            break
            
        losses = pinn.train_step(x_pde, t_pde, x_ic, t_ic, u_ic, x_bc, t_bc, u_bc)
        
        training_state['current_epoch'] = epoch + 1
        
        # Small delay to allow API calls
        if epoch % 10 == 0:
            time.sleep(0.01)
    
    training_state['is_training'] = False
    training_state['stop_requested'] = False


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/start_training', methods=['POST'])
def start_training():
    """Start PINN training"""
    global training_state
    
    if training_state['is_training']:
        return jsonify({'error': 'Training already in progress'}), 400
    
    # Get parameters from request
    params = request.json
    epochs = params.get('epochs', 1000)
    nu = params.get('nu', 0.01)
    hidden_layers = params.get('hidden_layers', [32, 32, 32])
    lr = params.get('lr', 0.001)
    
    # Reset state
    training_state['is_training'] = True
    training_state['current_epoch'] = 0
    training_state['stop_requested'] = False
    
    # Start training in background thread
    thread = threading.Thread(target=train_worker, 
                             args=(epochs, nu, hidden_layers, lr))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'Training started'})


@app.route('/api/stop_training', methods=['POST'])
def stop_training():
    """Stop PINN training"""
    global training_state
    training_state['stop_requested'] = True
    return jsonify({'status': 'Stop requested'})


@app.route('/api/training_status', methods=['GET'])
def training_status():
    """Get current training status"""
    global training_state
    
    status = {
        'is_training': training_state['is_training'],
        'current_epoch': training_state['current_epoch'],
        'losses': None
    }
    
    if training_state['pinn'] is not None:
        # Get recent losses
        history = training_state['pinn'].loss_history
        status['losses'] = {
            'total': history['total'][-100:] if len(history['total']) > 0 else [],
            'pde': history['pde'][-100:] if len(history['pde']) > 0 else [],
            'ic': history['ic'][-100:] if len(history['ic']) > 0 else [],
            'bc': history['bc'][-100:] if len(history['bc']) > 0 else []
        }
    
    return jsonify(status)


@app.route('/api/predict', methods=['POST'])
def predict():
    """Get PINN predictions"""
    global training_state
    
    if training_state['pinn'] is None:
        return jsonify({'error': 'Model not trained yet'}), 400
    
    # Get grid parameters
    params = request.json
    nx = params.get('nx', 100)
    nt = params.get('nt', 100)
    x_range = params.get('x_range', [-1, 1])
    t_range = params.get('t_range', [0, 1])
    
    # Get PINN prediction
    x = np.linspace(x_range[0], x_range[1], nx)
    t = np.linspace(t_range[0], t_range[1], nt)
    X, T = np.meshgrid(x, t)
    x_flat = X.flatten()
    t_flat = T.flatten()
    
    u_pred = training_state['pinn'].predict(x_flat, t_flat)
    U_pred = u_pred.reshape(nt, nx)
    
    # Get numerical solution for comparison
    x_num, t_num, U_numerical = solve_burgers_numerical(
        nx=nx, nt=nt, nu=training_state['pinn'].nu,
        x_range=x_range, t_range=t_range
    )
    
    # Compute error
    error = np.abs(U_pred - U_numerical)
    
    return jsonify({
        'x': x.tolist(),
        't': t.tolist(),
        'u_pred': U_pred.tolist(),
        'u_analytical': U_numerical.tolist(),
        'error': error.tolist()
    })


@app.route('/api/residuals', methods=['POST'])
def get_residuals():
    """Get PDE residuals on a grid"""
    global training_state
    
    if training_state['pinn'] is None:
        return jsonify({'error': 'Model not trained yet'}), 400
    
    params = request.json
    n_points = params.get('n_points', 50)
    
    # Create grid
    x = np.linspace(-1, 1, n_points)
    t = np.linspace(0, 1, n_points)
    X, T = np.meshgrid(x, t)
    
    x_flat = torch.FloatTensor(X.flatten()).reshape(-1, 1).to(training_state['pinn'].device)
    t_flat = torch.FloatTensor(T.flatten()).reshape(-1, 1).to(training_state['pinn'].device)
    
    # Compute residuals
    residuals = training_state['pinn'].compute_pde_residual(x_flat, t_flat)
    residuals_np = residuals.detach().cpu().numpy().reshape(n_points, n_points)
    
    return jsonify({
        'x': x.tolist(),
        't': t.tolist(),
        'residuals': residuals_np.tolist()
    })


@app.route('/api/get_collocation_points', methods=['GET'])
def get_collocation_points():
    """Get the collocation points used for training"""
    global training_state
    
    if training_state['training_data'] is None:
        return jsonify({'error': 'No training data available'}), 400
    
    data = training_state['training_data']
    
    return jsonify({
        'pde_points': {
            'x': data['x_pde'].flatten().tolist()[:500],  # Limit for performance
            't': data['t_pde'].flatten().tolist()[:500]
        },
        'ic_points': {
            'x': data['x_ic'].flatten().tolist(),
            't': data['t_ic'].flatten().tolist()
        },
        'bc_points': {
            'x': data['x_bc'].flatten().tolist(),
            't': data['t_bc'].flatten().tolist()
        }
    })


@app.route('/api/get_derivatives', methods=['POST'])
def get_derivatives():
    """Get derivatives computed by the network"""
    global training_state
    
    if training_state['pinn'] is None:
        return jsonify({'error': 'Model not trained yet'}), 400
    
    params = request.json
    nx = params.get('nx', 50)
    nt = params.get('nt', 50)
    
    # Create grid
    x = np.linspace(-1, 1, nx)
    t = np.linspace(0, 1, nt)
    X, T = np.meshgrid(x, t)
    
    x_tensor = torch.FloatTensor(X.flatten()).reshape(-1, 1).to(training_state['pinn'].device)
    t_tensor = torch.FloatTensor(T.flatten()).reshape(-1, 1).to(training_state['pinn'].device)
    
    x_tensor.requires_grad_(True)
    t_tensor.requires_grad_(True)
    
    # Compute u and derivatives
    u = training_state['pinn'].model(x_tensor, t_tensor)
    
    u_x = torch.autograd.grad(u, x_tensor, grad_outputs=torch.ones_like(u), 
                               create_graph=True)[0]
    u_t = torch.autograd.grad(u, t_tensor, grad_outputs=torch.ones_like(u), 
                               create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x_tensor, grad_outputs=torch.ones_like(u_x), 
                                create_graph=True)[0]
    
    # Convert to numpy
    u_np = u.detach().cpu().numpy().reshape(nt, nx)
    u_x_np = u_x.detach().cpu().numpy().reshape(nt, nx)
    u_t_np = u_t.detach().cpu().numpy().reshape(nt, nx)
    u_xx_np = u_xx.detach().cpu().numpy().reshape(nt, nx)
    
    return jsonify({
        'x': x.tolist(),
        't': t.tolist(),
        'u': u_np.tolist(),
        'u_x': u_x_np.tolist(),
        'u_t': u_t_np.tolist(),
        'u_xx': u_xx_np.tolist()
    })


if __name__ == '__main__':
    import os
    # Use PORT environment variable for deployment platforms (Render, Railway, etc.)
    port = int(os.environ.get('PORT', 5000))
    # Set debug=False for production
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
