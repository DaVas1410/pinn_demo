// API base URL
const API_BASE = 'http://localhost:5000/api';

// State
let trainingInterval = null;
let isTraining = false;

// DOM Elements
const nuSlider = document.getElementById('nu');
const nuValue = document.getElementById('nu-value');
const epochsInput = document.getElementById('epochs');
const lrInput = document.getElementById('lr');
const layersInput = document.getElementById('layers');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const epochSpan = document.getElementById('epoch');
const stateSpan = document.getElementById('state');
const lossTotalSpan = document.getElementById('loss-total');

// Update nu value display
nuSlider.addEventListener('input', (e) => {
    nuValue.textContent = parseFloat(e.target.value).toFixed(3);
});

// Start training
startBtn.addEventListener('click', async () => {
    const nu = parseFloat(nuSlider.value);
    const epochs = parseInt(epochsInput.value);
    const lr = parseFloat(lrInput.value);
    const layers = layersInput.value.split(',').map(x => parseInt(x.trim()));
    
    try {
        const response = await fetch(`${API_BASE}/start_training`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nu, epochs, lr, hidden_layers: layers })
        });
        
        if (response.ok) {
            isTraining = true;
            startBtn.disabled = true;
            stopBtn.disabled = false;
            stateSpan.textContent = 'Training...';
            stateSpan.style.color = '#28a745';
            
            // Start polling for updates
            startPolling();
        } else {
            alert('Failed to start training');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error starting training');
    }
});

// Stop training
stopBtn.addEventListener('click', async () => {
    try {
        await fetch(`${API_BASE}/stop_training`, { method: 'POST' });
        stopPolling();
    } catch (error) {
        console.error('Error:', error);
    }
});

// Polling for training status
function startPolling() {
    if (trainingInterval) {
        clearInterval(trainingInterval);
    }
    
    trainingInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/training_status`);
            const data = await response.json();
            
            // Update status
            epochSpan.textContent = data.current_epoch;
            
            if (data.losses && data.losses.total.length > 0) {
                const latestLoss = data.losses.total[data.losses.total.length - 1];
                lossTotalSpan.textContent = latestLoss.toExponential(3);
                
                // Update loss plot
                updateLossPlot(data.losses);
            }
            
            // Check if training finished
            if (!data.is_training && isTraining) {
                stopPolling();
                stateSpan.textContent = 'Completed';
                stateSpan.style.color = '#007bff';
                
                // Update predictions
                await updatePredictions();
                await updateResiduals();
                await updateCollocationPoints();
                await updateDerivatives();
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 500);
}

function stopPolling() {
    if (trainingInterval) {
        clearInterval(trainingInterval);
        trainingInterval = null;
    }
    isTraining = false;
    startBtn.disabled = false;
    stopBtn.disabled = true;
    stateSpan.textContent = 'Stopped';
    stateSpan.style.color = '#dc3545';
}

// Update predictions
async function updatePredictions() {
    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nx: 100, nt: 100 })
        });
        
        const data = await response.json();
        
        // Plot PINN solution
        plotHeatmap('solution-plot', data.x, data.t, data.u_pred, 'PINN Solution');
        
        // Plot analytical solution
        plotHeatmap('analytical-plot', data.x, data.t, data.u_analytical, 'Numerical Solution');
        
        // Plot error
        plotHeatmap('error-plot', data.x, data.t, data.error, 'Error', 'Reds');
    } catch (error) {
        console.error('Error updating predictions:', error);
    }
}

// Update residuals
async function updateResiduals() {
    try {
        const response = await fetch(`${API_BASE}/residuals`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ n_points: 50 })
        });
        
        const data = await response.json();
        plotHeatmap('residual-plot', data.x, data.t, data.residuals, 'PDE Residual', 'RdBu');
    } catch (error) {
        console.error('Error updating residuals:', error);
    }
}

// Plot heatmap
function plotHeatmap(elementId, x, t, z, title, colorscale = 'Viridis') {
    // Find min/max for proper color scaling
    let zFlat = z.flat();
    let zMin = Math.min(...zFlat);
    let zMax = Math.max(...zFlat);
    
    const trace = {
        x: x,
        y: t,
        z: z,
        type: 'heatmap',
        colorscale: colorscale,
        colorbar: {
            thickness: 15,
            len: 0.7
        },
        // Force proper color scaling
        zmin: zMin,
        zmax: zMax,
        // For symmetric data (like RdBu), center at 0
        zmid: (colorscale === 'RdBu' && Math.abs(zMin) > 0.01) ? 0 : undefined
    };
    
    const layout = {
        title: {
            text: `${title}<br><sub>Range: [${zMin.toFixed(3)}, ${zMax.toFixed(3)}]</sub>`,
            font: { size: 14 }
        },
        xaxis: {
            title: 'x',
            showgrid: true
        },
        yaxis: {
            title: 't',
            showgrid: true
        },
        margin: { l: 60, r: 60, t: 60, b: 60 },
        autosize: true
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot(elementId, [trace], layout, config);
}

// Update loss plot
function updateLossPlot(losses) {
    const traces = [];
    const colors = {
        total: '#667eea',
        pde: '#f093fb',
        ic: '#4facfe',
        bc: '#43e97b'
    };
    
    for (const [key, values] of Object.entries(losses)) {
        if (values.length > 0) {
            traces.push({
                y: values,
                name: key.toUpperCase(),
                type: 'scatter',
                mode: 'lines',
                line: {
                    color: colors[key],
                    width: 2
                }
            });
        }
    }
    
    const layout = {
        title: {
            text: 'Loss Components',
            font: { size: 14 }
        },
        xaxis: {
            title: 'Iteration',
            showgrid: true
        },
        yaxis: {
            title: 'Loss',
            type: 'log',
            showgrid: true
        },
        margin: { l: 60, r: 40, t: 50, b: 60 },
        showlegend: true,
        legend: {
            x: 1,
            y: 1,
            xanchor: 'right'
        },
        autosize: true
    };
    
    const config = {
        responsive: true,
        displayModeBar: false
    };
    
    Plotly.newPlot('loss-plot', traces, layout, config);
}

// Educational features
let animationData = null;
let animationPlaying = false;
let animationTimer = null;

// Show/hide educational features
document.getElementById('show-educational')?.addEventListener('change', (e) => {
    const features = document.querySelectorAll('.educational-feature');
    features.forEach(f => f.style.display = e.target.checked ? 'block' : 'none');
});

// Update collocation points
async function updateCollocationPoints() {
    try {
        const response = await fetch(`${API_BASE}/get_collocation_points`);
        const data = await response.json();
        
        const traces = [
            {
                x: data.pde_points.x,
                y: data.pde_points.t,
                mode: 'markers',
                type: 'scatter',
                name: 'PDE Points',
                marker: { size: 3, color: '#667eea', opacity: 0.6 }
            },
            {
                x: data.ic_points.x,
                y: data.ic_points.t,
                mode: 'markers',
                type: 'scatter',
                name: 'Initial Condition',
                marker: { size: 6, color: '#43e97b', symbol: 'square' }
            },
            {
                x: data.bc_points.x,
                y: data.bc_points.t,
                mode: 'markers',
                type: 'scatter',
                name: 'Boundary Condition',
                marker: { size: 6, color: '#fa709a', symbol: 'diamond' }
            }
        ];
        
        const layout = {
            title: 'Training Points Distribution',
            xaxis: { title: 'x', range: [-1, 1] },
            yaxis: { title: 't', range: [0, 1] },
            margin: { l: 60, r: 40, t: 50, b: 60 },
            showlegend: true,
            height: 350
        };
        
        Plotly.newPlot('collocation-plot', traces, layout, { responsive: true, displayModeBar: false });
    } catch (error) {
        console.error('Error updating collocation points:', error);
    }
}

// Update derivatives
async function updateDerivatives() {
    try {
        const response = await fetch(`${API_BASE}/get_derivatives`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nx: 50, nt: 50 })
        });
        
        const data = await response.json();
        
        plotHeatmap('dudx-plot', data.x, data.t, data.u_x, '∂u/∂x', 'RdBu');
        plotHeatmap('dudt-plot', data.x, data.t, data.u_t, '∂u/∂t', 'RdBu');
        plotHeatmap('dudxx-plot', data.x, data.t, data.u_xx, '∂²u/∂x²', 'RdBu');
        
        // Store for animation
        animationData = data;
        initializeAnimation(data);
    } catch (error) {
        console.error('Error updating derivatives:', error);
    }
}

// Initialize animation
function initializeAnimation(data) {
    const timeSlider = document.getElementById('time-slider');
    const timeValue = document.getElementById('time-value');
    
    if (!timeSlider || !data) return;
    
    timeSlider.max = data.t.length - 1;
    timeSlider.value = 0;
    
    timeSlider.addEventListener('input', (e) => {
        const idx = parseInt(e.target.value);
        timeValue.textContent = data.t[idx].toFixed(2);
        updateAnimationFrame(idx, data);
    });
    
    updateAnimationFrame(0, data);
}

// Update animation frame
function updateAnimationFrame(timeIdx, data) {
    const trace_pinn = {
        x: data.x,
        y: data.u[timeIdx],
        mode: 'lines',
        name: 'PINN',
        line: { color: '#667eea', width: 3 }
    };
    
    const layout = {
        title: `Solution at t=${data.t[timeIdx].toFixed(2)}`,
        xaxis: { title: 'x', range: [-1, 1] },
        yaxis: { title: 'u(x,t)', range: [-1, 1] },
        margin: { l: 60, r: 40, t: 50, b: 60 },
        height: 300
    };
    
    Plotly.newPlot('animation-plot', [trace_pinn], layout, { responsive: true, displayModeBar: false });
}

// Play animation
document.getElementById('play-btn')?.addEventListener('click', function() {
    const timeSlider = document.getElementById('time-slider');
    const playBtn = this;
    
    if (!animationData || !timeSlider) return;
    
    if (animationPlaying) {
        // Stop
        clearInterval(animationTimer);
        animationPlaying = false;
        playBtn.textContent = '▶ Play';
    } else {
        // Play
        animationPlaying = true;
        playBtn.textContent = '⏸ Pause';
        
        animationTimer = setInterval(() => {
            let currentIdx = parseInt(timeSlider.value);
            currentIdx++;
            
            if (currentIdx >= animationData.t.length) {
                currentIdx = 0;
            }
            
            timeSlider.value = currentIdx;
            document.getElementById('time-value').textContent = animationData.t[currentIdx].toFixed(2);
            updateAnimationFrame(currentIdx, animationData);
        }, 100);
    }
});

// Display network architecture
function displayNetworkArchitecture() {
    const layers = layersInput.value.split(',').map(x => parseInt(x.trim()));
    const netViz = document.getElementById('network-viz');
    if (!netViz) return;
    
    const arch = ['Input(2)'].concat(layers.map(l => `Hidden(${l})`)).concat(['Output(1)']);
    netViz.innerHTML = arch.join(' → ');
}

// Update network viz when layers change
layersInput?.addEventListener('change', displayNetworkArchitecture);

// Initialize empty plots
window.addEventListener('load', () => {
    // Initialize empty heatmaps
    const emptyData = Array(50).fill(0).map(() => Array(50).fill(0));
    const emptyX = Array(50).fill(0).map((_, i) => -1 + 2 * i / 49);
    const emptyT = Array(50).fill(0).map((_, i) => i / 49);
    
    plotHeatmap('solution-plot', emptyX, emptyT, emptyData, 'PINN Solution');
    plotHeatmap('analytical-plot', emptyX, emptyT, emptyData, 'Numerical Solution');
    plotHeatmap('error-plot', emptyX, emptyT, emptyData, 'Error', 'Reds');
    plotHeatmap('residual-plot', emptyX, emptyT, emptyData, 'PDE Residual', 'RdBu');
    plotHeatmap('dudx-plot', emptyX, emptyT, emptyData, '∂u/∂x', 'RdBu');
    plotHeatmap('dudt-plot', emptyX, emptyT, emptyData, '∂u/∂t', 'RdBu');
    plotHeatmap('dudxx-plot', emptyX, emptyT, emptyData, '∂²u/∂x²', 'RdBu');
    
    // Initialize empty loss plot
    updateLossPlot({ total: [], pde: [], ic: [], bc: [] });
    
    // Initialize collocation plot
    Plotly.newPlot('collocation-plot', [], {
        title: 'No training data yet',
        xaxis: { title: 'x' },
        yaxis: { title: 't' }
    }, { responsive: true, displayModeBar: false });
    
    // Initialize animation plot
    Plotly.newPlot('animation-plot', [], {
        title: 'Train model to see animation',
        xaxis: { title: 'x' },
        yaxis: { title: 'u' }
    }, { responsive: true, displayModeBar: false });
    
    // Display initial network architecture
    displayNetworkArchitecture();
});
