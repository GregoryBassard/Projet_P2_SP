from skyfield.api import load
from vpython import sphere, vector, curve, color, label, cylinder

# Charger les éphémérides DE440
kernels = load('de440.bsp')

# Identifiants SPICE corrects
planets = {
    'Mercure': 2440,
    'Vénus': 6052,
    'Terre': 6371,
    'Mars': 3390,
    'Jupiter': 69911,
    'Saturne': 58232,
    'Uranus': 25362,
    'Neptune': 24622
}

# Charger le Soleil
sun = kernels['sun']

# Définir l'échelle de temps
ts = load.timescale()
time_now = ts.now()
days_ahead = 365  # Orbites sur 1 an

# Générer une série de dates (un point par jour)
times = ts.linspace(time_now, time_now + days_ahead)

# Créer une scène 3D avec vpython
# Représenter le Soleil
sun_obj = sphere(pos=vector(0, 0, 0), radius=1392000, color=color.yellow)

# Ajouter les orbites des planètes (comme des courbes)
orbits = {}
pid = 0
for name, size in planets.items():
    pid = pid+1
    planet = kernels[pid]
    pos = (planet - sun).at(times).position.km  # Positions relatives au Soleil
    
    # Créer l'orbite de la planète sous forme de courbe
    orbit_curve = curve(
        radius=1000000, color=color.white
    )
    for i in range(len(times)):
        orbit_curve.append(pos=vector(pos[0][i], pos[1][i], pos[2][i]))

    # Représenter la planète
    planet_pos = pos[:, 0]  # Position à l'instant présent
    planet_obj = sphere(pos=vector(planet_pos[0], planet_pos[1], planet_pos[2]), radius=size, color=color.blue)

    # Ajouter un label pour chaque planète
    planet_label = label(pos=planet_obj.pos + vector(0, 0, 0.1), text=name, height=10, color=color.white)

# Garder la fenêtre ouverte
while True:
    pass
