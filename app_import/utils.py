from skyfield.api import load
import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons
import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from .NEOs import NEOsDisplayThread

def load_solar_system(fig:go.Figure)->go.Figure:
    # Charger les éphémérides DE440
    kernels = load("de440.bsp")

    planets_data = {
        "name": ["Mercury", "Venus", "Earth", "Mars"],
        "SPICE_ID": [1, 2, 3, 4],
        "color": ["gray", "gray", "blue", "gray"],
        "time": [88, 225, 365, 687]
    }

    # Charger le Soleil
    sun = kernels['sun']

    # Définir l"échelle de temps
    ts = load.timescale()
    time_now = ts.now()

    for i in range(len(planets_data["name"])):
        
        planet = kernels[planets_data['SPICE_ID'][i]]

        # Générer une série de dates (un point par jour)
        times = ts.linspace(time_now, time_now + planets_data['time'][i], planets_data['time'][i])

        pos_orbit = (planet - sun).at(times).position.km
        actual_pos = (planet - sun).at(time_now).position.km

        fig.add_trace(go.Scatter3d(
            x=pos_orbit[0], y=pos_orbit[1], z=pos_orbit[2],
            mode="lines",
            marker=dict(
                size=2,
                color=planets_data['color'][i],
                opacity=0.75
            ),
            line=dict(width=2),
            name=f"Orbit {planets_data['name'][i]}"
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[actual_pos[0]], y=[actual_pos[1]], z=[actual_pos[2]],
            mode="markers+text",
            marker=dict(size=4, color=planets_data['color'][i], opacity=0.9),
            text=planets_data['name'][i],
            name=planets_data['name'][i]
        ))

    # Ajout du Soleil
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers+text",
        marker=dict(size=10, color="yellow", opacity=1),
        text="Soleil",
        name="Soleil"
    ))

    return fig

# Create 3D Axes
def create_3d_axes(fig:go.Figure, axis_length:int, color:str)->go.Figure:
    # X-axis, Y-axis, Z-axis (All Yellow)
        
    fig.add_trace(    
        go.Scatter3d(
            x=[-axis_length, axis_length], y=[0, 0], z=[0, 0],
            mode="lines",
            line=dict(color=color, width=1),
            marker= dict(opacity=0.6),
            name="X-Axis"
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[0, 0], y=[-axis_length, axis_length], z=[0, 0],
            mode="lines",
            line=dict(color=color, width=1),
            marker= dict(opacity=0.6),
            name="Y-Axis"
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[-axis_length, axis_length],
            mode="lines",
            line=dict(color=color, width=1),
            marker= dict(opacity=0.6),
            name="Z-Axis"
        )
    )

    return fig

def display_neos_with_thread(neos:list):
    threads = []
    for neo in neos:
        threads.append(NEOsDisplayThread(neo, "Object"))
        threads.append(NEOsDisplayThread(neo, "Orbital"))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        if thread.result is not None:
            yield thread.result
        else:
            print(f"trace error neo : {thread.neo.name}")

def display_neos_without_thread(neos:list):
    for neo in neos:
        yield neo.display()
        yield neo.display_orbital_path()

def convert_fractional_date(date_str):
    if '.' not in date_str:
        raise ValueError("date format expected : 'YYYY-MM-DD.DD'")
    
    date_part, fraction_part = date_str.split('.')
    
    base_date = datetime.strptime(date_part, "%Y-%m-%d")
    
    fraction = float("0." + fraction_part)
    added_seconds = fraction * 24 * 60 * 60
    
    final_date = base_date + timedelta(seconds=added_seconds)
    return final_date

def get_time_left(date:str)->relativedelta:
    target_date = convert_fractional_date(date)
    current_date = datetime.now()
    time_left = relativedelta(target_date, current_date)
    return time_left


