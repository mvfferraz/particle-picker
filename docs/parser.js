class ParticleParser {
    
    static parseStarFile(content) {
        console.log('Starting STAR file parsing...');
        console.log('File length:', content.length, 'characters');
        
        const lines = content.split('\n').map(line => line.trim());
        console.log('Total lines:', lines.length);
        
        const particles = [];
        let inParticlesSection = false;
        let inLoop = false;
        let headers = [];
        let dataLineCount = 0;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            
            if (line.length === 0) continue;
            
            if (line === 'data_particles' || line.startsWith('data_particles')) {
                console.log('Found data_particles at line', i);
                inParticlesSection = true;
                inLoop = false;
                headers = [];
                continue;
            }
            
            if (inParticlesSection && line === 'loop_') {
                console.log('Found loop_ at line', i);
                inLoop = true;
                continue;
            }
            
            if (inParticlesSection && inLoop && line.startsWith('_rln')) {
                const parts = line.split(/\s+/);
                const headerName = parts[0].replace('_rln', '');
                headers.push(headerName);
                if (headers.length === 1) {
                    console.log('First header:', headerName);
                }
                continue;
            }
            
            if (inParticlesSection && headers.length > 0) {
                if (!line.startsWith('_') && !line.startsWith('data_') && !line.startsWith('loop_') && !line.startsWith('#')) {
                    const values = line.split(/\s+/).filter(v => v.length > 0);
                    
                    if (values.length >= headers.length) {
                        const particle = {};
                        headers.forEach((header, idx) => {
                            if (idx < values.length) {
                                const value = values[idx];
                                particle[header] = isNaN(value) ? value : parseFloat(value);
                            }
                        });
                        particles.push(particle);
                        dataLineCount++;
                        
                        if (dataLineCount === 1) {
                            console.log('First particle:', particle);
                        }
                    }
                }
            }
            
            if (inParticlesSection && line.startsWith('data_') && line !== 'data_particles') {
                console.log('End of particles section at line', i);
                break;
            }
        }
        
        console.log('Headers found:', headers.length, 'headers');
        console.log('Header names:', headers.slice(0, 5), '...');
        console.log('Total particles parsed:', particles.length);
        
        if (particles.length === 0) {
            console.error('ERROR: No particles found!');
            console.log('Debug info:');
            console.log('- inParticlesSection was set:', inParticlesSection);
            console.log('- headers array length:', headers.length);
            console.log('- First 20 lines of file:');
            lines.slice(0, 20).forEach((line, i) => {
                console.log(`  ${i}: "${line}"`);
            });
        }
        
        return particles;
    }
    
    static parseCsvFile(content) {
        return new Promise((resolve, reject) => {
            Papa.parse(content, {
                header: true,
                dynamicTyping: true,
                skipEmptyLines: true,
                complete: (results) => {
                    resolve(results.data);
                },
                error: (error) => {
                    reject(error);
                }
            });
        });
    }
    
    static parseBoxFile(content) {
        const lines = content.split('\n').map(line => line.trim()).filter(line => line);
        const particles = [];
        
        lines.forEach(line => {
            const values = line.split(/\s+/).map(v => parseFloat(v));
            if (values.length >= 4) {
                particles.push({
                    x: values[0],
                    y: values[1],
                    width: values[2],
                    height: values[3]
                });
            }
        });
        
        return particles;
    }
}

class ParticleStatistics {
    
    constructor(particles) {
        this.particles = particles;
        this.micrographCol = this.findMicrographColumn();
    }
    
    findMicrographColumn() {
        if (this.particles.length === 0) return null;
        
        const firstParticle = this.particles[0];
        const possibleCols = [
            'MicrographName', 
            'Micrographs Filename',
            'micrograph', 
            'image', 
            'ImageName',
            '_rlnMicrographName',
            'rlnMicrographName'
        ];
        
        for (const col of possibleCols) {
            if (firstParticle.hasOwnProperty(col)) {
                console.log('Using micrograph column:', col);
                return col;
            }
        }
        
        for (const key in firstParticle) {
            if (key.toLowerCase().includes('micrograph') || 
                key.toLowerCase().includes('image') ||
                key.toLowerCase().includes('filename')) {
                console.log('Auto-detected micrograph column:', key);
                return key;
            }
        }
        
        return null;
    }
    
    getDistributionPerMicrograph() {
        if (!this.micrographCol) return {};
        
        const distribution = {};
        
        this.particles.forEach(particle => {
            const micrograph = particle[this.micrographCol];
            if (micrograph) {
                distribution[micrograph] = (distribution[micrograph] || 0) + 1;
            }
        });
        
        return distribution;
    }
    
    getSummaryStatistics() {
        const distribution = this.getDistributionPerMicrograph();
        const counts = Object.values(distribution);
        
        return {
            totalParticles: this.particles.length,
            totalMicrographs: Object.keys(distribution).length,
            avgParticlesPerMicrograph: counts.length > 0 ? (counts.reduce((a, b) => a + b, 0) / counts.length) : 0,
            minParticlesPerMicrograph: counts.length > 0 ? Math.min(...counts) : 0,
            maxParticlesPerMicrograph: counts.length > 0 ? Math.max(...counts) : 0,
            stdParticlesPerMicrograph: this.calculateStd(counts)
        };
    }
    
    calculateStd(values) {
        if (values.length === 0) return 0;
        const mean = values.reduce((a, b) => a + b, 0) / values.length;
        const squareDiffs = values.map(value => Math.pow(value - mean, 2));
        const avgSquareDiff = squareDiffs.reduce((a, b) => a + b, 0) / squareDiffs.length;
        return Math.sqrt(avgSquareDiff);
    }
    
    getCoordinates() {
        const xCols = ['CoordinateX', 'x', 'X', 'X-Coordinate', '_rlnCoordinateX', 'rlnCoordinateX', 'pos_x', 'posX', 'x_coord'];
        const yCols = ['CoordinateY', 'y', 'Y', 'Y-Coordinate', '_rlnCoordinateY', 'rlnCoordinateY', 'pos_y', 'posY', 'y_coord'];
        
        let xCol = null, yCol = null;
        
        if (this.particles.length > 0) {
            const firstParticle = this.particles[0];
            const availableColumns = Object.keys(firstParticle);
            
            console.log('Available columns in data:', availableColumns);
            
            for (const col of xCols) {
                if (firstParticle.hasOwnProperty(col)) {
                    xCol = col;
                    break;
                }
            }
            
            if (!xCol) {
                for (const col of availableColumns) {
                    if (col.toLowerCase().includes('x') && 
                        (col.toLowerCase().includes('coord') || 
                         col.toLowerCase().includes('pos') ||
                         col === 'x' || col === 'X')) {
                        xCol = col;
                        console.log('Auto-detected X column:', col);
                        break;
                    }
                }
            }
            
            for (const col of yCols) {
                if (firstParticle.hasOwnProperty(col)) {
                    yCol = col;
                    break;
                }
            }
            
            if (!yCol) {
                for (const col of availableColumns) {
                    if (col.toLowerCase().includes('y') && 
                        (col.toLowerCase().includes('coord') || 
                         col.toLowerCase().includes('pos') ||
                         col === 'y' || col === 'Y')) {
                        yCol = col;
                        console.log('Auto-detected Y column:', col);
                        break;
                    }
                }
            }
            
            console.log('Using X column:', xCol);
            console.log('Using Y column:', yCol);
        }
        
        if (!xCol || !yCol) {
            console.warn('Could not find coordinate columns. Available columns:', 
                        this.particles.length > 0 ? Object.keys(this.particles[0]) : 'none');
            return null;
        }
        
        return {
            x: this.particles.map(p => p[xCol]).filter(v => v !== undefined && !isNaN(v)),
            y: this.particles.map(p => p[yCol]).filter(v => v !== undefined && !isNaN(v)),
            xCol,
            yCol
        };
    }
}
