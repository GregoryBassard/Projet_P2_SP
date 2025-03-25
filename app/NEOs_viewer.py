from skyfield.api import load
import plotly.graph_objects as go
import numpy as np
import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import load_solar_system, load_asteroid_orbit, load_asteroid, get_neos1, get_neos2

fig = go.Figure()

fig = load_solar_system(fig)

# date_max = '2030-01-01'
# date_min = '2020-01-01'
# dist_max = '0.05LD'
# fullname = '1'
# nea_comet = '1'

neos = get_neos2(1e-6, -4)

for neo in neos.to_dict('records'):
    print(neo['des'])
    fig = load_asteroid(fig, neo['des'])
    # fig = load_asteroid_orbit(fig, neo['des'], '2025-01-01', '2027-01-01', '1d')

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