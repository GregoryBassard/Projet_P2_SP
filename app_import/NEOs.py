import plotly.graph_objects as go
from astroquery.jplhorizons import Horizons
import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from threading  import Thread
from time import sleep

class NEOs:
    def __init__(self):
        self.summary = None
        self.data = None
    
    def display(self)->go.Scatter3d:
        now = datetime.now()
        stop = now + timedelta(days=1)
        try:
            obj = Horizons(id=self.name, location="500@10", epochs={"start": now.strftime("%Y-%m-%d"), "stop": stop.strftime("%Y-%m-%d"), "step": "1d"})
            vectors = obj.vectors()

            trace = go.Scatter3d(
                x=[vectors['x'][0]*1.496e+8], y=[vectors['y'][0]*1.496e+8], z=[vectors['z'][0]*1.496e+8],
                mode="markers+text",
                marker=dict(size=5, color="white", opacity=0.9),
                text=f"{self.name}",
                textfont=dict(size=12, color="white"),
                name=f"{self.name} (neo)"
            )
            return trace
        except:
            print(f"Erreur lors du chargement du NEO: {self.name}")
        return None
    
    def display_orbital_path(self)->go.Scatter3d:
        now = datetime.now()
        stop = now + timedelta(days=self.get_orbit_date_range() + 1)
        
        try:
            obj = Horizons(id=self.name, location="500@10", epochs={"start": now.strftime("%Y-%m-%d"), "stop": stop.strftime("%Y-%m-%d"), "step": "1d"})

            vectors = obj.vectors()

            trace = go.Scatter3d(
                x=vectors['x']*1.496e+8, y=vectors['y']*1.496e+8, z=vectors['z']*1.496e+8,
                mode="lines",
                line=dict(width=2, color="#fec036"),
                visible=False,
                name=f"orbit {self.name} (neo)"
            )
            return trace
        except:
            print(f"Erreur lors du chargement du NEO {self.name}")
        return None
    
    def get_orbit_date_range(self)->str:
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
    
    def request_neo_data_and_summary(self)->dict:
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
        
        data_summary = {
            "summary": data['summary'],
            "data": data['data']
        }
        return data_summary

    def get_data_and_summary(self)->dict:
        data_summary = self.request_neo_data_and_summary()

        # summary
        summary = pd.DataFrame.from_dict(data_summary['summary'], orient='index', columns=['value'])

        col_drop = ['des', 'ndop', 'nobs', 'ndel', 'nsat', 'fullname', 'pdate', 'cdate', 'darc', 'method']
        summary = summary.drop(col_drop, axis=0, errors='ignore').sort_index().to_dict()

        self.summary = summary

        # data
        self.data = data_summary['data']

    def convert_fractional_date(self, date_str):
        if '.' not in date_str:
            raise ValueError("date format expected : 'YYYY-MM-DD.DD'")
        
        date_part, fraction_part = date_str.split('.')
        
        base_date = datetime.strptime(date_part, "%Y-%m-%d")
        
        fraction = float("0." + fraction_part)
        added_seconds = fraction * 24 * 60 * 60
        
        final_date = base_date + timedelta(seconds=added_seconds)
        return final_date
    
    def get_time_left(self)->relativedelta:
        date = pd.DataFrame(self.data).sort_values(by="date", ascending=True).reset_index(drop=True)["date"][0]
        target_date = self.convert_fractional_date(date)
        current_date = datetime.now()
        time_left = relativedelta(target_date, current_date)

        self.years = str(time_left.years).zfill(2)
        self.months = str(time_left.months).zfill(2)
        self.days = str(time_left.days).zfill(2)
        self.hms = str(time_left.hours).zfill(2) + ":" + str(time_left.minutes).zfill(2) + ":" + str(time_left.seconds).zfill(2)

        return time_left
    
    def isFilter(self, filter_start_date, filter_end_date, filter_ip, filter_diameter, filter_energy)->bool:
        result = True

        neo_date = self.convert_fractional_date(pd.DataFrame(self.data).sort_values(by="date", ascending=True).reset_index(drop=True)["date"][0])
        
        neo_ip_value = float(pd.DataFrame(self.data).sort_values(by="date", ascending=True).reset_index(drop=True)["ip"][0])
        
        neo_ip_label = ""
        if neo_ip_value * 100 < 1.0e-3:
            neo_ip_label = "negligible"
        elif neo_ip_value * 100 < 1.0:
            neo_ip_label = "low"
        else:
            neo_ip_label = "concerning"

        neo_diameter = float(self.summary['value']['diameter'])
                             
        neo_energy = float(self.summary['value']['energy'])

        if neo_date < datetime.strptime(filter_start_date, "%Y-%m-%d") or neo_date > datetime.strptime(filter_end_date, "%Y-%m-%d"):
            result = False
        if neo_ip_label not in filter_ip:
            result = False
        if neo_diameter < float(filter_diameter[0]) or neo_diameter > float(filter_diameter[1]):
            result = False
        if neo_energy < float(filter_energy[0]) or neo_energy > float(filter_energy[1]):
            result = False

        return result

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