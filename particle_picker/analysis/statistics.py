import pandas as pd
import numpy as np
from pathlib import Path

class ParticleStatistics:
    
    def __init__(self, particles_df, micrograph_col='MicrographName'):
        self.df = particles_df
        self.micrograph_col = micrograph_col
        
        if self.micrograph_col not in self.df.columns:
            possible_cols = [col for col in self.df.columns 
                           if 'micrograph' in col.lower() or 'image' in col.lower()]
            if possible_cols:
                self.micrograph_col = possible_cols[0]
    
    def get_distribution_per_micrograph(self):
        if self.micrograph_col not in self.df.columns:
            return pd.Series(dtype=int)
        
        return self.df.groupby(self.micrograph_col).size().sort_values(ascending=False)
    
    def get_coordinate_statistics(self):
        stats = {}
        
        coord_cols = [col for col in self.df.columns 
                     if any(x in col.lower() for x in ['coordinatex', 'coordinatey', '_x', '_y'])]
        
        for col in coord_cols:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                stats[col] = {
                    'mean': float(self.df[col].mean()),
                    'std': float(self.df[col].std()),
                    'min': float(self.df[col].min()),
                    'max': float(self.df[col].max()),
                    'median': float(self.df[col].median())
                }
        
        return stats
    
    def get_defocus_statistics(self):
        stats = {}
        
        defocus_cols = [col for col in self.df.columns if 'defocus' in col.lower()]
        
        for col in defocus_cols:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                stats[col] = {
                    'mean': float(self.df[col].mean()),
                    'std': float(self.df[col].std()),
                    'min': float(self.df[col].min()),
                    'max': float(self.df[col].max())
                }
        
        return stats
    
    def get_summary_statistics(self):
        summary = {
            'total_particles': len(self.df),
            'total_micrographs': 0,
            'avg_particles_per_micrograph': 0,
            'min_particles_per_micrograph': 0,
            'max_particles_per_micrograph': 0,
            'std_particles_per_micrograph': 0
        }
        
        if self.micrograph_col in self.df.columns:
            dist = self.get_distribution_per_micrograph()
            summary['total_micrographs'] = len(dist)
            summary['avg_particles_per_micrograph'] = float(dist.mean())
            summary['min_particles_per_micrograph'] = int(dist.min())
            summary['max_particles_per_micrograph'] = int(dist.max())
            summary['std_particles_per_micrograph'] = float(dist.std())
        
        return summary
    
    def get_heatmap_data(self, bin_size=100):
        coord_x_cols = [col for col in self.df.columns 
                       if 'coordinatex' in col.lower() or col.lower().endswith('_x')]
        coord_y_cols = [col for col in self.df.columns 
                       if 'coordinatey' in col.lower() or col.lower().endswith('_y')]
        
        if not coord_x_cols or not coord_y_cols:
            return None
        
        x_col = coord_x_cols[0]
        y_col = coord_y_cols[0]
        
        x_bins = np.arange(self.df[x_col].min(), self.df[x_col].max() + bin_size, bin_size)
        y_bins = np.arange(self.df[y_col].min(), self.df[y_col].max() + bin_size, bin_size)
        
        hist, x_edges, y_edges = np.histogram2d(
            self.df[x_col],
            self.df[y_col],
            bins=[x_bins, y_bins]
        )
        
        return {
            'histogram': hist,
            'x_edges': x_edges,
            'y_edges': y_edges,
            'x_col': x_col,
            'y_col': y_col
        }
