from skyfield.api import load
import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons

def load_solar_system(fig:go.Figure)->go.Figure:
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

    planet_to_show = ['Mercure', 'Vénus', 'Terre', 'Mars']#, 'Jupiter', 'Saturne', 'Uranus', 'Neptune', 'Pluton']

    for i in range(len(planets_data['name'])):
        if planets_data['name'][i] not in planet_to_show:
            continue
        
        planet = kernels[planets_data['SPICE_ID'][i]]

        # Générer une série de dates (un point par jour)
        times = ts.linspace(time_now, time_now + planets_data['time'][i], planets_data['time'][i])

        pos_orbit = (planet - sun).at(times).position.km
        actual_pos = (planet - sun).at(time_now).position.km

        fig.add_trace(go.Scatter3d(
            x=pos_orbit[0], y=pos_orbit[1], z=pos_orbit[2],
            mode='lines',
            marker=dict(
                size=1,
                color=planets_data['color'][i],
                opacity=0.9
            ),
            line=dict(width=2),
            name=f'Orbite {planets_data['name'][i]}'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[actual_pos[0]], y=[actual_pos[1]], z=[actual_pos[2]],
            mode='markers+text',
            marker=dict(size=4, color=planets_data['color'][i], opacity=0.9),
            text=planets_data['name'][i]
        ))

    # Ajout du Soleil
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=10, color='yellow', opacity=1),
        text='Soleil'
    ))

    return fig

def load_asteroid(fig:go.Figure, asteroid_id:str, start_date:str, stop_date:str, step:str)->go.Figure:

    obj = Horizons(id=asteroid_id, location='500@10', epochs={'start': start_date, 'stop': stop_date, 'step': step})

    vectors = obj.vectors()

    fig.add_trace(go.Scatter3d(
        x=vectors['x']*1.496e+8, y=vectors['y']*1.496e+8, z=vectors['z']*1.496e+8,
        mode='lines',
        marker=dict(size=1, color='white', opacity=0.9),
        line=dict(width=2),
        name=f'Orbite {asteroid_id}'
    ))

    fig.add_trace(go.Scatter3d(
        x=[vectors['x'][0]*1.496e+8], y=[vectors['y'][0]*1.496e+8], z=[vectors['z'][0]*1.496e+8],
        mode='markers+text',
        marker=dict(size=4, color='white', opacity=0.9),
        text=asteroid_id
    ))

    return fig