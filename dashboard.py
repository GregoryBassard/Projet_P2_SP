import dash
from dash import dcc, html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from app_import.NEOs import NEOs, load_neos

load_dotenv()
NASA_API_KEY = os.getenv('NASA_API_KEY')

neos = load_neos(1e-6, -4, 0)

for neo in neos:
    neo.get_data_and_summary()

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'}, children=[
    html.H1("NEO Data Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    dcc.Dropdown(id='neo-dropdown', options=[], value=None,
                 style={'width': '300px', 'margin': '0 auto', 'marginBottom': '20px', 'color': 'black'}),
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around'}, children=[
        html.Div(style={'width': '300px', 'border': '1px solid white', 'padding': '10px'}, children=[
            html.H3("Max Diameter", style={'textAlign': 'center'}),
            daq.Tank(id='diameter-tank', showCurrentValue=True, units="meters",
                     color="#ff9e00", height=200, width=100, max=200),
            html.Div(id='diameter-value', style={'textAlign': 'center', 'fontSize': '24px'})
        ]),
        html.Div(style={'width': '300px', 'border': '1px solid white', 'padding': '10px'}, children=[
            html.H3("Relative Velocity", style={'textAlign': 'center'}),
            daq.Gauge(id='velocity-gauge', units="km/h", max=100000,
                      color="#ff9e00", size=175),
            html.Div(id='velocity-value', style={'textAlign': 'center', 'fontSize': '24px'})
        ]),
        html.Div(style={'width': '300px', 'border': '1px solid white', 'padding': '10px'}, children=[
            html.H3("Inclination", style={'textAlign': 'center'}),
            html.Div(id='inclination-value', style={'textAlign': 'center', 'fontSize': '24px', 'marginTop': '80px'})
        ]),
    ])
])

@app.callback(
    [
        Output('diameter-tank', 'value'),
        Output('diameter-value', 'children'),
        Output('velocity-gauge', 'value'),
        Output('velocity-value', 'children'),
        Output('inclination-value', 'children')
    ],
    [Input('interval-component', 'n_intervals'),
     Input('neo-dropdown', 'value')],
)
def update_dashboard(n, selected_neo):
    client = NasaAPINEOClient(NASA_API_KEY)
    neolist = [neo.name for neo in neos]
    df = client.get_selected_neo_details(neolist)
    if selected_neo:
        df = df[df['name'] == selected_neo]
    diameter = df['diameter_max_meters'].iloc[0] if not df.empty and selected_neo else 0
    velocity = df['relative_velocity_km_h'].iloc[0] if not df.empty and selected_neo else 0
    inclination = df['inclination'].iloc[0] if not df.empty and selected_neo else 0
    return (
        diameter, f"{diameter:.2f} meters",
        velocity, f"{velocity:.2f} km/h",
        f"{inclination:.2f} degrees"
    )

@app.callback(
    Output('neo-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown_options(n):
    client = NasaAPINEOClient(NASA_API_KEY)
    neolist = [neo.name for neo in neos]
    df = client.get_selected_neo_details(neolist)
    if not df.empty:
        neo_options = [{'label': neo, 'value': neo} for neo in df['name'].unique()]
    else:
        neo_options = []
    return neo_options

if __name__ == '__main__':
    app.run(debug=True)