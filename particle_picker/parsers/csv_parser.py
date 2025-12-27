import pandas as pd
from pathlib import Path

class CSVParticleParser:
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = None
        self._parse()
    
    def _parse(self):
        try:
            df = pd.read_csv(self.filepath)
            
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_numeric(df[col], errors='ignore')
                    except:
                        pass
            
            self.data = df
            
        except Exception as e:
            print(f"Error parsing CSV {self.filepath}: {e}")
            self.data = None
    
    def get_particles(self):
        return self.data
    
    def get_micrograph_names(self):
        if self.data is not None:
            micrograph_cols = [col for col in self.data.columns 
                             if 'micrograph' in col.lower() or 'image' in col.lower()]
            if micrograph_cols:
                return self.data[micrograph_cols[0]].unique()
        return []
    
    def get_particles_per_micrograph(self):
        if self.data is not None:
            micrograph_cols = [col for col in self.data.columns 
                             if 'micrograph' in col.lower() or 'image' in col.lower()]
            if micrograph_cols:
                return self.data.groupby(micrograph_cols[0]).size().to_dict()
        return {}
    
    def get_statistics(self):
        if self.data is None:
            return {}
        
        stats = {
            'total_particles': len(self.data),
            'columns': list(self.data.columns)
        }
        
        coord_cols = [col for col in self.data.columns 
                     if any(x in col.lower() for x in ['x', 'y', 'coordinate'])]
        
        for col in coord_cols:
            if pd.api.types.is_numeric_dtype(self.data[col]):
                stats[f'{col}_mean'] = float(self.data[col].mean())
                stats[f'{col}_std'] = float(self.data[col].std())
        
        micrograph_cols = [col for col in self.data.columns 
                         if 'micrograph' in col.lower() or 'image' in col.lower()]
        if micrograph_cols:
            stats['unique_micrographs'] = len(self.data[micrograph_cols[0]].unique())
        
        return stats
