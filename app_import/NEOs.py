from skyfield.api import load
import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons
import requests
import pandas as pd
from datetime import datetime, timedelta
from threading  import Thread
from time import sleep

class NEOs:
    def __init__(self):
        pass
    
    def display(self)->go.Scatter3d:
        now = datetime.now()
        stop = now + timedelta(days=1)
        try:
            obj = Horizons(id=self.name, location="500@10", epochs={"start": now.strftime("%Y-%m-%d"), "stop": stop.strftime("%Y-%m-%d"), "step": "1d"})
            vectors = obj.vectors()

            trace = go.Scatter3d(
                x=[vectors['x'][0]*1.496e+8], y=[vectors['y'][0]*1.496e+8], z=[vectors['z'][0]*1.496e+8],
                mode="markers+text",
                marker=dict(size=4, color="gray", opacity=0.9),
                text=f"{self.name} (neo)",
                textfont=dict(size=12, color="lightgray"),
                name=f"{self.name} (neo)"
            )
            return trace
        except:
            print(f"Erreur lors du chargement du NEO: {self.name}")
        return None
    
    def display_orbital_path(self)->go.Scatter3d:
        now = datetime.now()
        stop = now + timedelta(days=self.get_orbite_date_range())
        
        try:
            obj = Horizons(id=self.name, location="500@10", epochs={"start": now.strftime("%Y-%m-%d"), "stop": stop.strftime("%Y-%m-%d"), "step": "1d"})

            vectors = obj.vectors()

            trace = go.Scatter3d(
                x=vectors['x']*1.496e+8, y=vectors['y']*1.496e+8, z=vectors['z']*1.496e+8,
                mode="lines",
                line=dict(width=2, color="white"),
                visible=False,
                name=f"Orbite {self.name} (neo)"
            )
            return trace
        except:
            print(f"Erreur lors du chargement du NEO {self.name}")
        return None
    
    def get_orbite_date_range(self)->str:
        try:
            url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?des={self.name}"
            r = requests.get(url)
            while r.status_code == 503:
                print(f"API Service Unavailable  (NEO {self.name}): retry in 500ms")
                sleep(0.5)
                r = requests.get(url)

            data = r.json()
        except Exception as e:
            print(f"Erreur lors du chargement des données du NEO {self.name}: {e}")
        
        orbit_element = pd.DataFrame(data['orbit']['elements'])
        return int(orbit_element[orbit_element['title'] == 'sidereal orbital period']['value'].iloc[0])
    
    def get_neo_data(self)->dict:
        try:
            url = f"https://ssd-api.jpl.nasa.gov/sentry.api?des={self.name}"
            r = requests.get(url)
            while r.status_code == 503:
                print(f"API Service Unavailable  (NEO {self.name}): retry in 500ms")
                sleep(0.5)
                r = requests.get(url)

            data = r.json()
        except Exception as e:
            print(f"Erreur lors du chargement des données du NEO {self.name}: {e}")
        
        self.summary = data['summary']
        self.data = data['data']
        return data

class NEOsDisplayThread(Thread):
    def __init__(self, neo:NEOs, methode:str):
        Thread.__init__(self)
        self.neo = neo
        self.methode = methode
        self.result = None
    
    def run(self) -> None:
        if self.methode == "Orbital":
            self.result = self.neo.display_orbital_path()
        elif self.methode == "Object":
            self.result = self.neo.display()

def load_neos(ip_min:str, ps_min:str, limit:int)->list:
    try:
        url = f"https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={ip_min}&ps-min={ps_min}"
        r = requests.get(url)
        data = r.json()['data']
    except Exception as e:
        print(f"Erreur lors du chargement des NEOs: {e}")
        return []
    neos = []
    if limit > 0:
        data = data[:limit]
    for neo in data:
        n = NEOs()
        n.name = neo['des']
        neos.append(n)
    return neos