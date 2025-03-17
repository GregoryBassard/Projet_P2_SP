from vpython import *
import math

# Création de la scène
scene = canvas(title="Terre en 3D avec astéroïdes", width=800, height=600)

# Création de la Terre avec texture
terre = sphere(
    pos=vector(150, 0, 0),  # Distance moyenne de la Terre au Soleil en millions de km (échelle simplifiée)
    radius=0.6,  # Rayon en milliers de km (échelle simplifiée)
    texture=textures.earth,
    shininess=0.5
)
# Création du Soleil au centre de l'écran
soleil = sphere(
    pos=vector(0, 0, 0),
    radius=10,  # Rayon en milliers de km (échelle simplifiée)
    color=color.yellow,
    emissive=True  # Le Soleil émet de la lumière
)

# Liste des astéroïdes
asteroides = []

def creer_asteroide(orbite_rayon, vitesse_orbite, couleur=color.red):
    """Ajoute un astéroïde en orbite autour de la Terre."""
    ast = sphere(
        pos=vector(orbite_rayon, 0, 0),
        radius=0.3,
        color=couleur,
        make_trail=True  # Laisse une trace de mouvement
    )
    asteroides.append({"objet": ast, "rayon": orbite_rayon, "vitesse": vitesse_orbite, "angle": 0})

# Ajout de quelques astéroïdes en orbite
creer_asteroide(15, 0.01, color.yellow)  # Orbite large et lente
creer_asteroide(10, 0.02, color.white)   # Orbite plus proche et rapide

# Animation
while True:
    rate(60)  # Vitesse de l'animation
