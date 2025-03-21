from skyfield.api import load
import plotly.graph_objects as go
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Charger les éphémérides DE440
kernels = load('de440.bsp')

planets_data = {
    'name': ['Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 'Saturne', 'Uranus', 'Neptune'],
    'SPICE_ID': [1, 2, 3, 4, 5, 6, 7, 8],
    'color': ['gray', 'orange', 'blue', 'red', 'rosybrown', 'sandybrown', 'cyan', 'blue'],
    'time': [88, 225, 365, 687, 4333, 10759, 30687, 60190]
}

# Charger le Soleil
sun = kernels['sun']

# Définir l'échelle de temps
ts = load.timescale()
time_now = ts.now()

# Création de la figure 3D
fig = go.Figure()

for i in range(len(planets_data['name'])):
    planet = kernels[planets_data['SPICE_ID'][i]]

    # Générer une série de dates (un point par jour)
    times = ts.linspace(time_now, time_now + planets_data['time'][i])

    pos = (planet - sun).at(times).position.km

    fig.add_trace(go.Scatter3d(
        x=pos[0], y=pos[1], z=pos[2],
        mode='lines',
        marker=dict(
            size=1,
            color=planets_data['color'][i],
            opacity=0.9
        ),
        line=dict(width=2),
        name=f'Orbite {planets_data['name'][i]}'
    ))

for i in range(len(planets_data['name'])):
    planet = kernels[planets_data['SPICE_ID'][i]]
    pos = (planet - sun).at(time_now).position.km
    
    fig.add_trace(go.Scatter3d(
        x=[pos[0]], y=[pos[1]], z=[pos[2]],
        mode='markers+text',
        marker=dict(size=4, color=planets_data['color'][i], opacity=0.9),
        text=planets_data['name'][i]
    ))

# Ajouter le Soleil
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=10, color='yellow', opacity=1),
    text='Soleil'
))

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