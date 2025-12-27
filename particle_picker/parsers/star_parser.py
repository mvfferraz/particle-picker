import pandas as pd
import re
from pathlib import Path

class StarFileParser:
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.optics_data = None
        self.particles_data = None
        self._parse()
    
    def _parse(self):
        with open(self.filepath, 'r') as f:
            content = f.read()
        
        optics_section = self._extract_section(content, 'data_optics')
        particles_section = self._extract_section(content, 'data_particles')
        
        if optics_section:
            self.optics_data = self._parse_data_block(optics_section)
        
        if particles_section:
            self.particles_data = self._parse_data_block(particles_section)
    
    def _extract_section(self, content, section_name):
        pattern = f'{section_name}(.*?)(?=data_|$)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else None
    
    def _parse_data_block(self, block):
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if not lines or 'loop_' not in lines[0]:
            return None
        
        loop_idx = lines.index('loop_')
        header_lines = []
        data_start_idx = None
        
        for i in range(loop_idx + 1, len(lines)):
            if lines[i].startswith('_'):
                header_lines.append(lines[i])
            else:
                data_start_idx = i
                break
        
        if not header_lines or data_start_idx is None:
            return None
        
        column_names = [self._clean_column_name(h) for h in header_lines]
        data_lines = lines[data_start_idx:]
        
        rows = []
        for line in data_lines:
            if line and not line.startswith('_') and not line.startswith('#'):
                values = line.split()
                if len(values) == len(column_names):
                    rows.append(values)
        
        if not rows:
            return None
        
        df = pd.DataFrame(rows, columns=column_names)
        
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='ignore')
        
        return df
    
    def _clean_column_name(self, header):
        parts = header.split('#')
        name = parts[0].strip()
        if name.startswith('_rln'):
            name = name[4:]
        return name
    
    def get_particles(self):
        return self.particles_data
    
    def get_optics(self):
        return self.optics_data
    
    def get_micrograph_names(self):
        if self.particles_data is not None and 'MicrographName' in self.particles_data.columns:
            return self.particles_data['MicrographName'].unique()
        return []
    
    def get_particles_per_micrograph(self):
        if self.particles_data is not None and 'MicrographName' in self.particles_data.columns:
            return self.particles_data.groupby('MicrographName').size().to_dict()
        return {}
    
    def get_statistics(self):
        if self.particles_data is None:
            return {}
        
        stats = {
            'total_particles': len(self.particles_data),
            'unique_micrographs': len(self.get_micrograph_names()),
            'avg_particles_per_micrograph': 0,
            'min_particles_per_micrograph': 0,
            'max_particles_per_micrograph': 0
        }
        
        particles_per_mic = self.get_particles_per_micrograph()
        if particles_per_mic:
            counts = list(particles_per_mic.values())
            stats['avg_particles_per_micrograph'] = sum(counts) / len(counts)
            stats['min_particles_per_micrograph'] = min(counts)
            stats['max_particles_per_micrograph'] = max(counts)
        
        return stats
