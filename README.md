# NEOs Sentry App
This application is an interactive dashboard for visualizing and exploring NEOs that are monitored for potential impact risks with Earth.  
It uses data from **NASA's Sentry system** to display the orbits, physical characteristics, and risk assessments of asteroids and comets whose paths bring them close to our planet.
## Downloading and running app
Visit the [releases page](https://gitlab-etu.ing.he-arc.ch/isc/2024-25/niveau-2/2282.1-projet-p2-sp-id/p2sp_uthayendran_bassard/-/releases) and download and `unzip` the project app source code. Then `cd` into the app directory and install its dependencies in a virtual environment in the following way :
```bash
python -m venv venv
source venv/bin/activate  # Windows: \venv\scripts\activate
pip install -r requirements.txt
```
then you can run the app :
```bash
.venv/Scripts/python.exe NEOs_app.py
```
## Cloning this whole repository
To clone this repository, run:
```
git clone https://gitlab-etu.ing.he-arc.ch/isc/2024-25/niveau-2/2282.1-projet-p2-sp-id/p2sp_uthayendran_bassard.git
```
## Membres
- [Uthayendran Kobikan](https://gitlab-etu.ing.he-arc.ch/kobikan.uthayendran)
- [Bassard Grégory](https://gitlab-etu.ing.he-arc.ch/gregory.bassard)