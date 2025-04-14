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

    def __str__(self):
        return f"{self.name}\n\t - Palermo Scale: {self.ps}\n\t - Torino Scale: {self.ts}\n\t - Range: {self.range}\n\t - Last Obs: {self.last_obs}\n\t - Diameter: {self.diameter}\n\t - Impact probability: {self.ip}"
    
    def setattributes(self, name:str, ps:str, ts:str, range:str, last_obs:str, diameter:str, ip:str):
        self.name = name
        self.ps = ps
        self.ts = ts
        self.range = range
        self.last_obs = last_obs
        self.diameter = diameter
        self.ip = ip
    
    def display(self)->go.Scatter3d:
        now = datetime.now()
        stop = now + timedelta(days=1)
        try:
            obj = Horizons(id=self.name, location="500@10", epochs={"start": now.strftime("%Y-%m-%d"), "stop": stop.strftime("%Y-%m-%d"), "step": "1d"})
            vectors = obj.vectors()

            trace = go.Scatter3d(
                x=[vectors["x"][0]*1.496e+8], y=[vectors["y"][0]*1.496e+8], z=[vectors["z"][0]*1.496e+8],
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
                x=vectors["x"]*1.496e+8, y=vectors["y"]*1.496e+8, z=vectors["z"]*1.496e+8,
                mode="lines",
                line=dict(width=2, color="white"),
                visible=False,
                name=f"Orbite {self.name} (neo)"
            )
            return trace
        except:
            print(f"Erreur lors du chargement du NEO {self.name}")
        return None
    
    def load_neos(self, ip_min:str, ps_min:str, limit:int)->list:
        try:
            url = f"https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={ip_min}&ps-min={ps_min}"
            r = requests.get(url)
            data = r.json()["data"]
        except Exception as e:
            print(f"Erreur lors du chargement des NEOs: {e}")
            return []
        neos = []
        if limit > 0:
            data = data[:limit]
        for neo in data:
            n = NEOs()
            n.setattributes(neo["des"], neo["ps_cum"], neo["ts_max"], neo["range"], neo["last_obs"], neo["diameter"], neo["ip"])
            neos.append(n)
        return neos
    
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
        
        orbit_element = pd.DataFrame(data["orbit"]["elements"])
        return int(orbit_element[orbit_element["title"] == "sidereal orbital period"]["value"].iloc[0])

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