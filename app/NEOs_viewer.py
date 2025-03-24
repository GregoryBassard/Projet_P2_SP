from skyfield.api import load
import plotly.graph_objects as go
import numpy as np
import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import load_solar_system, load_asteroid

fig = go.Figure()

fig = load_solar_system(fig)

fig = load_asteroid(fig, '2025 FC2', '2025-03-23', '2027-05-23', '1d')

fig.update_layout(
    title='Orbite des Planètes autour du Soleil',
    template='plotly_dark',
    scene = dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        zaxis = dict(visible=False)
        )
    )

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='solar-system',
        figure=fig,
        style={'height': '90vh'}
    )
])

if __name__ == '__main__':
    app.run(debug=True)