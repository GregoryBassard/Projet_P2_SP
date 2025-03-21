from skyfield.api import load
import plotly.graph_objects as go
import numpy as np

# Charger les éphémérides DE440
kernels = load('de440.bsp')

# Identifiants SPICE corrects
planets = {
    'Mercure': 1,
    'Vénus': 2,
    'Terre': 3,
    'Mars': 4,
    'Jupiter': 5,
    'Saturne': 6,
    'Uranus': 7,
    'Neptune': 8,
}

planets_data = {
    'name': ['Mercure', 'Vénus', 'Terre', 'Mars', 'Jupiter', 'Saturne', 'Uranus', 'Neptune'],
    'SPICE_ID': [1, 2, 3, 4, 5, 6, 7, 8],
    'color': ['gray', 'orange', 'blue', 'red', 'rosybrown', 'sandybrown', 'cyan', 'blue'],
    'time': [88, 225, 365, 687, 4333, 10759, 30687, 60190],
}

# Charger le Soleil
sun = kernels['sun']

# Définir l'échelle de temps
ts = load.timescale()
time_now = ts.now() + 365
days_ahead = 365  # Orbites sur 1 an

# Création de la figure 3D
fig = go.Figure()

for i in range(len(planets_data['name'])):
    planet = kernels[planets_data['SPICE_ID'][i]]

    # Générer une série de dates (un point par jour)
    times = ts.linspace(time_now, time_now + planets_data['time'][i])

    pos = (planet - sun).at(times).position.km  # Positions relatives au Soleil

    fig.add_trace(go.Scatter3d(
        x=pos[0], y=pos[1], z=pos[2],
        mode='lines',
        marker=dict(
            size=1,
            color=planets_data['color'][i],
            opacity=0.8
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
        marker=dict(size=6, color=planets_data['color'][i]),
        text=planets_data['name'][i]
    ))

# Ajouter le Soleil
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers+text',
    marker=dict(size=12, color='yellow'),
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

fig.show()
