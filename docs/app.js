let currentData = null;
let currentStats = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const alerts = document.getElementById('alerts');
const statsSection = document.getElementById('statsSection');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

function handleFile(file) {
    const maxSize = 50 * 1024 * 1024;
    
    if (file.size > maxSize) {
        showAlert('File too large. Maximum size is 50MB.', 'error');
        return;
    }
    
    const ext = file.name.split('.').pop().toLowerCase();
    const validExtensions = ['star', 'csv', 'box', 'txt'];
    
    if (!validExtensions.includes(ext)) {
        showAlert('Invalid file type. Please upload .star, .csv, or .box files.', 'error');
        return;
    }
    
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatBytes(file.size);
    document.getElementById('fileType').textContent = ext.toUpperCase();
    fileInfo.style.display = 'block';
    
    showAlert('Processing file...', 'success');
    
    const reader = new FileReader();
    reader.onload = (e) => {
        processFile(e.target.result, ext);
    };
    reader.onerror = () => {
        showAlert('Error reading file.', 'error');
    };
    reader.readAsText(file);
}

async function processFile(content, fileType) {
    try {
        let particles;
        
        if (fileType === 'star') {
            particles = ParticleParser.parseStarFile(content);
        } else if (fileType === 'csv') {
            particles = await ParticleParser.parseCsvFile(content);
        } else if (fileType === 'box') {
            particles = ParticleParser.parseBoxFile(content);
        }
        
        if (!particles || particles.length === 0) {
            showAlert('No particle data found in file.', 'error');
            return;
        }
        
        currentData = particles;
        currentStats = new ParticleStatistics(particles);
        
        showAlert(`Successfully loaded ${particles.length.toLocaleString()} particles!`, 'success');
        
        displayStatistics();
        createVisualizations();
        
        statsSection.style.display = 'block';
        statsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error processing file:', error);
        showAlert('Error processing file: ' + error.message, 'error');
    }
}

function displayStatistics() {
    const summary = currentStats.getSummaryStatistics();
    const statsGrid = document.getElementById('statsGrid');
    
    statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-label">Total Particles</div>
            <div class="stat-value">${summary.totalParticles.toLocaleString()}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Total Micrographs</div>
            <div class="stat-value">${summary.totalMicrographs.toLocaleString()}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Average per Micrograph</div>
            <div class="stat-value">${summary.avgParticlesPerMicrograph.toFixed(1)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Min per Micrograph</div>
            <div class="stat-value">${summary.minParticlesPerMicrograph}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Max per Micrograph</div>
            <div class="stat-value">${summary.maxParticlesPerMicrograph}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Std Deviation</div>
            <div class="stat-value">${summary.stdParticlesPerMicrograph.toFixed(1)}</div>
        </div>
    `;
}

function createVisualizations() {
    createDistributionChart();
    createHistogramChart();
    createScatterChart();
}

function createDistributionChart() {
    const distribution = currentStats.getDistributionPerMicrograph();
    const micrographs = Object.keys(distribution);
    const counts = Object.values(distribution);
    
    const sortedIndices = counts
        .map((value, index) => ({ value, index }))
        .sort((a, b) => b.value - a.value)
        .map(item => item.index);
    
    const sortedMicrographs = sortedIndices.map(i => micrographs[i]);
    const sortedCounts = sortedIndices.map(i => counts[i]);
    
    const displayLimit = 50;
    const displayMicrographs = sortedMicrographs.slice(0, displayLimit);
    const displayCounts = sortedCounts.slice(0, displayLimit);
    
    const data = [{
        type: 'bar',
        x: displayMicrographs.map((_, i) => i),
        y: displayCounts,
        text: displayCounts,
        textposition: 'auto',
        customdata: displayMicrographs,
        hovertemplate: '<b>Micrograph:</b> %{customdata}<br><b>Particles:</b> %{y}<extra></extra>',
        marker: {
            color: displayCounts,
            colorscale: 'Viridis'
        }
    }];
    
    const layout = {
        title: `Particle Distribution per Micrograph (Top ${displayLimit})`,
        xaxis: { title: 'Micrograph Index' },
        yaxis: { title: 'Number of Particles' },
        height: 500
    };
    
    Plotly.newPlot('distributionChart', data, layout, { responsive: true });
}

function createHistogramChart() {
    const distribution = currentStats.getDistributionPerMicrograph();
    const counts = Object.values(distribution);
    
    const data = [{
        type: 'histogram',
        x: counts,
        nbinsx: 30,
        marker: {
            color: 'rgba(102, 126, 234, 0.7)',
            line: {
                color: 'rgba(102, 126, 234, 1)',
                width: 1
            }
        }
    }];
    
    const layout = {
        title: 'Distribution of Particles per Micrograph',
        xaxis: { title: 'Number of Particles' },
        yaxis: { title: 'Frequency' },
        height: 400
    };
    
    Plotly.newPlot('histogramChart', data, layout, { responsive: true });
}

function createScatterChart() {
    const coords = currentStats.getCoordinates();
    
    if (!coords) {
        document.getElementById('scatterChart').innerHTML = 
            '<p style="text-align: center; padding: 40px; color: #666;">No coordinate data available</p>';
        return;
    }
    
    const maxPoints = 10000;
    let x = coords.x;
    let y = coords.y;
    
    if (x.length > maxPoints) {
        const indices = [];
        for (let i = 0; i < maxPoints; i++) {
            indices.push(Math.floor(Math.random() * x.length));
        }
        x = indices.map(i => x[i]);
        y = indices.map(i => y[i]);
    }
    
    const data = [{
        type: 'scattergl',
        mode: 'markers',
        x: x,
        y: y,
        marker: {
            size: 3,
            color: 'rgba(102, 126, 234, 0.5)'
        },
        hovertemplate: '<b>X:</b> %{x}<br><b>Y:</b> %{y}<extra></extra>'
    }];
    
    const layout = {
        title: `Particle Coordinates (${x.length.toLocaleString()} points)`,
        xaxis: { title: coords.xCol },
        yaxis: { title: coords.yCol },
        height: 500
    };
    
    Plotly.newPlot('scatterChart', data, layout, { responsive: true });
}

function showAlert(message, type) {
    alerts.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    
    setTimeout(() => {
        alerts.innerHTML = '';
    }, 5000);
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
