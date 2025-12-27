import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ParticleVisualizations:
    
    def __init__(self, statistics):
        self.stats = statistics
    
    def create_distribution_bar_chart(self):
        distribution = self.stats.get_distribution_per_micrograph()
        
        if distribution.empty:
            return go.Figure()
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(range(len(distribution))),
                y=distribution.values,
                text=distribution.values,
                textposition='auto',
                hovertemplate='<b>Micrograph:</b> %{customdata}<br><b>Particles:</b> %{y}<extra></extra>',
                customdata=distribution.index
            )
        ])
        
        fig.update_layout(
            title='Particle Distribution per Micrograph',
            xaxis_title='Micrograph Index',
            yaxis_title='Number of Particles',
            hovermode='closest',
            height=500
        )
        
        return fig
    
    def create_histogram(self):
        distribution = self.stats.get_distribution_per_micrograph()
        
        if distribution.empty:
            return go.Figure()
        
        fig = go.Figure(data=[
            go.Histogram(
                x=distribution.values,
                nbinsx=30,
                marker_color='lightblue',
                marker_line_color='darkblue',
                marker_line_width=1
            )
        ])
        
        fig.update_layout(
            title='Distribution of Particles per Micrograph',
            xaxis_title='Number of Particles',
            yaxis_title='Frequency',
            height=400
        )
        
        return fig
    
    def create_coordinate_scatter(self, max_points=10000):
        coord_stats = self.stats.get_coordinate_statistics()
        
        if not coord_stats:
            return go.Figure()
        
        df = self.stats.df
        
        x_cols = [col for col in coord_stats.keys() if 'x' in col.lower()]
        y_cols = [col for col in coord_stats.keys() if 'y' in col.lower()]
        
        if not x_cols or not y_cols:
            return go.Figure()
        
        x_col = x_cols[0]
        y_col = y_cols[0]
        
        if len(df) > max_points:
            sample_df = df.sample(n=max_points, random_state=42)
        else:
            sample_df = df
        
        fig = go.Figure(data=[
            go.Scattergl(
                x=sample_df[x_col],
                y=sample_df[y_col],
                mode='markers',
                marker=dict(
                    size=3,
                    color='blue',
                    opacity=0.5
                ),
                text=sample_df.index,
                hovertemplate='<b>X:</b> %{x}<br><b>Y:</b> %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=f'Particle Coordinates ({len(sample_df)} points)',
            xaxis_title=x_col,
            yaxis_title=y_col,
            height=500,
            hovermode='closest'
        )
        
        return fig
    
    def create_heatmap(self, bin_size=100):
        heatmap_data = self.stats.get_heatmap_data(bin_size=bin_size)
        
        if heatmap_data is None:
            return go.Figure()
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data['histogram'].T,
            x=heatmap_data['x_edges'][:-1],
            y=heatmap_data['y_edges'][:-1],
            colorscale='Hot',
            colorbar=dict(title='Particle Count')
        ))
        
        fig.update_layout(
            title='Particle Density Heatmap',
            xaxis_title=heatmap_data['x_col'],
            yaxis_title=heatmap_data['y_col'],
            height=500
        )
        
        return fig
    
    def create_defocus_distribution(self):
        defocus_stats = self.stats.get_defocus_statistics()
        
        if not defocus_stats:
            return go.Figure()
        
        df = self.stats.df
        defocus_cols = list(defocus_stats.keys())
        
        if not defocus_cols:
            return go.Figure()
        
        fig = make_subplots(
            rows=1, cols=len(defocus_cols),
            subplot_titles=[col for col in defocus_cols]
        )
        
        for idx, col in enumerate(defocus_cols, 1):
            fig.add_trace(
                go.Histogram(
                    x=df[col],
                    name=col,
                    nbinsx=30,
                    marker_color='lightgreen'
                ),
                row=1, col=idx
            )
        
        fig.update_layout(
            title='Defocus Distribution',
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_summary_table(self):
        summary = self.stats.get_summary_statistics()
        
        table_data = []
        for key, value in summary.items():
            formatted_key = key.replace('_', ' ').title()
            if isinstance(value, float):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
            table_data.append([formatted_key, formatted_value])
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Value'],
                fill_color='lightblue',
                align='left',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[[row[0] for row in table_data], 
                       [row[1] for row in table_data]],
                fill_color='white',
                align='left',
                font=dict(size=11)
            )
        )])
        
        fig.update_layout(
            title='Summary Statistics',
            height=300
        )
        
        return fig
