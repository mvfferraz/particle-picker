import pandas as pd
from pathlib import Path

class BoxFileParser:
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = None
        self._parse()
    
    def _parse(self):
        try:
            df = pd.read_csv(
                self.filepath,
                sep=r'\s+',
                header=None,
                names=['x', 'y', 'width', 'height']
            )
            
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.dropna()
            self.data = df
            
        except Exception as e:
            print(f"Error parsing {self.filepath}: {e}")
            self.data = None
    
    def get_particles(self):
        return self.data
    
    def get_statistics(self):
        if self.data is None:
            return {}
        
        return {
            'total_particles': len(self.data),
            'avg_x': self.data['x'].mean(),
            'avg_y': self.data['y'].mean(),
            'avg_width': self.data['width'].mean(),
            'avg_height': self.data['height'].mean()
        }
