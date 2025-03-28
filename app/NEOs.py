from skyfield.api import load
import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons
import requests
import pandas as pd
from datetime import datetime, timedelta

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
    
    def display(self, fig:go.Figure)->go.Figure:
        now = datetime.now()
        stop = now + timedelta(days=1)
        
        try:
            obj = Horizons(id=self.name, location='500@10', epochs={'start': now.strftime('%Y-%m-%d'), 'stop': stop.strftime('%Y-%m-%d'), 'step': '1d'})
            vectors = obj.vectors()

            fig.add_trace(go.Scatter3d(
                x=[vectors['x'][0]*1.496e+8], y=[vectors['y'][0]*1.496e+8], z=[vectors['z'][0]*1.496e+8],
                mode='markers+text',
                marker=dict(size=4, color='white', opacity=0.9),
                text=self.name,
                name=self.name
            ))
        except:
            print(f"Erreur lors du chargement de l'astéroïde {self.name}")

        return fig
    
    def load_neos(self, ip_min:str, ps_min:str)->list:
        try:
            url = f'https://ssd-api.jpl.nasa.gov/sentry.api?ip-min={ip_min}&ps-min={ps_min}'
            r = requests.get(url)
            data = r.json()['data']
        except Exception as e:
            print(f'Erreur lors du chargement des NEOs: {e}')
            return []
        neos = []
        for neo in data:
            n = NEOs()
            n.setattributes(neo['des'], neo['ps_cum'], neo['ts_max'], neo['range'], neo['last_obs'], neo['diameter'], neo['ip'])
            neos.append(n)
        return neos
    
    def get_orbite_date_range(self):
        pass