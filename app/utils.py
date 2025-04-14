from skyfield.api import load
import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons
import requests
import pandas as pd
from NEOs import NEOsDisplayThread

def load_solar_system(fig:go.Figure)->go.Figure:
    # Charger les éphémérides DE440
    kernels = load("de440.bsp")

    planets_data = {
        "name": ["Mercure", "Vénus", "Terre", "Mars", "Jupiter", "Saturne", "Uranus", "Neptune"],
        "SPICE_ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 301],
        "color": ["gray", "orange", "blue", "red", "rosybrown", "sandybrown", "cyan", "blue", "gray", "white"],
        "time": [88, 225, 365, 687, 4333, 10759, 30687, 60190, 90560, 28]
    }

    # Charger le Soleil
    sun = kernels["sun"]

    # Définir l"échelle de temps
    ts = load.timescale()
    time_now = ts.now()

    planet_to_show = ["Mercure", "Vénus", "Terre", "Mars"]#, "Jupiter", "Saturne", "Uranus", "Neptune", "Pluton"]

    for i in range(len(planets_data)):
        if planets_data["name"][i] not in planet_to_show:
            continue
        
        planet = kernels[planets_data["SPICE_ID"][i]]

        # Générer une série de dates (un point par jour)
        times = ts.linspace(time_now, time_now + planets_data["time"][i], planets_data["time"][i])

        pos_orbit = (planet - sun).at(times).position.km
        actual_pos = (planet - sun).at(time_now).position.km

        fig.add_trace(go.Scatter3d(
            x=pos_orbit[0], y=pos_orbit[1], z=pos_orbit[2],
            mode="lines",
            marker=dict(
                size=2,
                color=planets_data["color"][i],
                opacity=0.9
            ),
            line=dict(width=2),
            name=f"Orbite {planets_data["name"][i]}"
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[actual_pos[0]], y=[actual_pos[1]], z=[actual_pos[2]],
            mode="markers+text",
            marker=dict(size=4, color=planets_data["color"][i], opacity=0.9),
            text=planets_data["name"][i],
            name=planets_data["name"][i]
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

def load_asteroid(fig:go.Figure, asteroid_id:str)->go.Figure:
    # Récupérer les données actuelles de l"astéroïde
    try:
        obj = Horizons(id=asteroid_id, location="500@10", epochs={"start": "2025-03-24", "stop": "2025-03-25", "step": "1d"})
        vectors = obj.vectors()

        fig.add_trace(go.Scatter3d(
            x=[vectors["x"][0]*1.496e+8], y=[vectors["y"][0]*1.496e+8], z=[vectors["z"][0]*1.496e+8],
            mode="markers+text",
            marker=dict(size=4, color="white", opacity=0.9),
            text=asteroid_id,
            name=asteroid_id
        ))
    except:
        print(f"Erreur lors du chargement de lastéroïde {asteroid_id}")

    return fig

def load_asteroid_orbit(fig:go.Figure, asteroid_id:str, start_date:str, stop_date:str, step:str)->go.Figure:

    obj = Horizons(id=asteroid_id, location="500@10", epochs={"start": start_date, "stop": stop_date, "step": step})

    vectors = obj.vectors()

    fig.add_trace(go.Scatter3d(
        x=vectors["x"]*1.496e+8, y=vectors["y"]*1.496e+8, z=vectors["z"]*1.496e+8,
        mode="lines",
        marker=dict(size=2, color="white", opacity=0.9),
        line=dict(width=2),
        name=f"Orbite {asteroid_id}"
    ))

    return fig

def get_neos1(date_max:str, date_min:str, dist_max:str, fullname:str, nea_comet:str)->pd.DataFrame:
    url = f"https://ssd-api.jpl.nasa.gov/cad.api?dist-max={dist_max}&date-min={date_min}&date-max={date_max}&fullname={fullname}&nea-comet={nea_comet}"
    r = requests.get(url)
    data = r.json()
    columns = data["fields"]
    df = pd.DataFrame(data["data"], columns=columns)
    return df

def get_neos2(ip_min:str, ps_min:str)->pd.DataFrame:
    url = f"https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={ip_min}&ps-min={ps_min}"
    r = requests.get(url)
    data = r.json()["data"]
    df = pd.DataFrame(data)
    return df

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

