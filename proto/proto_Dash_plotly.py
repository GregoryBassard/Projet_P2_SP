from skyfield.api import load
import plotly.graph_objects as go
import numpy as np
import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output

# Charger les éphémérides DE440
kernels = load('de440.bsp')

planets_data = {
    'name': ['Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 'Saturne', 'Uranus', 'Neptune'],
    'SPICE_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 301],
    'color': ['gray', 'orange', 'blue', 'red', 'rosybrown', 'sandybrown', 'cyan', 'blue', 'gray', 'white'],
    'time': [88, 225, 365, 687, 4333, 10759, 30687, 60190, 90560, 28]
}

# Charger le Soleil
sun = kernels['sun']

# Définir l'échelle de temps
ts = load.timescale()
time_now = ts.now()

# Création de la figure 3D
fig = go.Figure()

planet_show = ['Mercure', 'Vénus', 'Terre', 'Mars']#, 'Jupiter', 'Saturne', 'Uranus', 'Neptune', 'Pluton']

for i in range(len(planets_data['name'])):
    if planets_data['name'][i] not in planet_show:
        continue
    
    planet = kernels[planets_data['SPICE_ID'][i]]

    # Générer une série de dates (un point par jour)
    times = ts.linspace(time_now, time_now + planets_data['time'][i], planets_data['time'][i])
    # print(f'{planets_data['name'][i]}: {times[0].utc_jpl()} -> {times[-1].utc_jpl()}')
    # print(f'Nombre de points: {len(times)}')

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
    if planets_data['name'][i] not in planet_show:
        continue

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

# ajout NEO
from astroquery.jplhorizons import Horizons

# ID de l'astéroïde et date d'observation
obj = Horizons(id='2025 FC2', location='500@10', epochs={'start': '2025-03-23', 'stop': '2027-05-23', 'step': '1d'})

# Récupérer les coordonnées héliocentriques
vectors = obj.vectors()

fig.add_trace(go.Scatter3d(
    x=vectors['x']*1.496e+8, y=vectors['y']*1.496e+8, z=vectors['z']*1.496e+8,
    mode='lines',
    marker=dict(size=1, color='white', opacity=0.9),
    line=dict(width=2),
    name='Orbite 2025 FC2'
))

fig.add_trace(go.Scatter3d(
    x=[vectors['x'][0]*1.496e+8], y=[vectors['y'][0]*1.496e+8], z=[vectors['z'][0]*1.496e+8],
    mode='markers+text',
    marker=dict(size=4, color='white', opacity=0.9),
    text='2025 FC2'
))


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