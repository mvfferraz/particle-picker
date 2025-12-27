import sys
from pathlib import Path
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent))

from parsers.star_parser import StarFileParser
from parsers.csv_parser import CSVParticleParser
from parsers.box_parser import BoxFileParser
from analysis.statistics import ParticleStatistics
from visualization.plots import ParticleVisualizations

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Particle Picker Statistics Dashboard", className="text-center my-4"),
            html.P("Analyze particle picking results from .star, .csv, or .box files", 
                   className="text-center text-muted")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Load Data", className="card-title"),
                    dbc.Input(
                        id="file-path",
                        placeholder="Enter file path (e.g., data/10017/ground_truth/empiar-10017_particles_selected.star)",
                        type="text",
                        className="mb-3"
                    ),
                    dbc.RadioItems(
                        id="file-type",
                        options=[
                            {"label": ".star (RELION)", "value": "star"},
                            {"label": ".csv (Coordinates)", "value": "csv"},
                            {"label": ".box (EMAN2)", "value": "box"}
                        ],
                        value="star",
                        className="mb-3"
                    ),
                    dbc.Button("Load File", id="load-button", color="primary", className="w-100"),
                    html.Div(id="load-status", className="mt-3")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    html.Div(id="dashboard-content")
    
], fluid=True)

@app.callback(
    [Output("load-status", "children"),
     Output("dashboard-content", "children")],
    Input("load-button", "n_clicks"),
    [State("file-path", "value"),
     State("file-type", "value")],
    prevent_initial_call=True
)
def load_and_analyze(n_clicks, filepath, file_type):
    if not filepath:
        return dbc.Alert("Please enter a file path", color="warning"), None
    
    filepath = Path(filepath)
    
    if not filepath.exists():
        return dbc.Alert(f"File not found: {filepath}", color="danger"), None
    
    try:
        if file_type == "star":
            parser = StarFileParser(filepath)
            particles_df = parser.get_particles()
        elif file_type == "csv":
            parser = CSVParticleParser(filepath)
            particles_df = parser.get_particles()
        elif file_type == "box":
            parser = BoxFileParser(filepath)
            particles_df = parser.get_particles()
        else:
            return dbc.Alert("Invalid file type", color="danger"), None
        
        if particles_df is None or particles_df.empty:
            return dbc.Alert("No particle data found in file", color="warning"), None
        
        stats = ParticleStatistics(particles_df)
        viz = ParticleVisualizations(stats)
        
        summary = stats.get_summary_statistics()
        
        dashboard = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Summary", className="card-title"),
                            dcc.Graph(figure=viz.create_summary_table())
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Particle Distribution", className="card-title"),
                            dcc.Graph(figure=viz.create_distribution_bar_chart())
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Distribution Histogram", className="card-title"),
                            dcc.Graph(figure=viz.create_histogram())
                        ])
                    ])
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Coordinate Scatter Plot", className="card-title"),
                            dcc.Graph(figure=viz.create_coordinate_scatter())
                        ])
                    ])
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Particle Density Heatmap", className="card-title"),
                            dcc.Graph(figure=viz.create_heatmap(bin_size=200))
                        ])
                    ])
                ], width=12)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Defocus Distribution", className="card-title"),
                            dcc.Graph(figure=viz.create_defocus_distribution())
                        ])
                    ])
                ], width=12)
            ], className="mb-4")
        ], fluid=True)
        
        status = dbc.Alert(
            f"Successfully loaded {summary['total_particles']} particles from {summary['total_micrographs']} micrographs",
            color="success"
        )
        
        return status, dashboard
        
    except Exception as e:
        return dbc.Alert(f"Error loading file: {str(e)}", color="danger"), None

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
