from skyfield.api import load
import plotly.graph_objects as go
import numpy as np
import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import load_solar_system, load_asteroid_orbit, load_asteroid, get_neos1, get_neos2
from NEOs import NEOs

fig = go.Figure()

fig = load_solar_system(fig)

neo_class = NEOs()
neos = neo_class.load_neos(1e-6, -4)

for neo in neos:
    fig = neo.display(fig)

fig.update_layout(
    title='Orbite des Planètes autour du Soleil',
    template='plotly_dark',
    scene = dict(
        xaxis = dict(range=[-500000000, 500000000], visible=False),
        yaxis = dict(range=[-500000000, 500000000], visible=False),
        zaxis = dict(range=[-500000000, 500000000], visible=False)
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