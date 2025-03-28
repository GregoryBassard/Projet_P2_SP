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
    scene=dict(
        xaxis=dict(range=[-500000000, 500000000], visible=False),
        yaxis=dict(range=[-500000000, 500000000], visible=False),
        zaxis=dict(range=[-500000000, 500000000], visible=False)
    )
)

# Create 3D Axes
def create_3d_axes():
    axis_length = 500000000  # Length of the axes to match the scale of the solar system

    # X-axis, Y-axis, Z-axis (All Yellow)
    x_axis = go.Scatter3d(
        x=[-axis_length, axis_length], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='yellow', width=1),
        marker= dict(opacity=0.6),
        name='X-Axis'
    )

    y_axis = go.Scatter3d(
        x=[0, 0], y=[-axis_length, axis_length], z=[0, 0],
        mode='lines',
        line=dict(color='yellow', width=1),
        marker= dict(opacity=0.6),
        name='Y-Axis'
    )

    z_axis = go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-axis_length, axis_length],
        mode='lines',
        line=dict(color='yellow', width=1),
        marker= dict(opacity=0.6),
        name='Z-Axis'
    )

    return [x_axis, y_axis, z_axis]

# Add 3D axes to the figure
axes = create_3d_axes()
for axis in axes:
    fig.add_trace(axis)

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
