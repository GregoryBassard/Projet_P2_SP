import dash
from dash import dcc, html
import numpy as np
import plotly.graph_objects as go
from PIL import Image

app = dash.Dash(__name__)

earth_texture_path = r"C:\Users\kobis\Documents\2273.1VisualisationData\p2sp_uthayendran_bassard\image\Equirectangular_projection_SW.jpg"
img = Image.open(earth_texture_path)
img = img.resize((360, 180))
img = np.array(img)

theta = np.linspace(0, 2 * np.pi, img.shape[1])
phi = np.linspace(0, np.pi, img.shape[0])
theta, phi = np.meshgrid(theta, phi)

R = 1
x = R * np.sin(phi) * np.cos(theta)
y = R * np.sin(phi) * np.sin(theta)
z = R * np.cos(phi)

intensity = np.mean(img, axis=2)

sat_x, sat_y, sat_z = 2, 0, 0.5

fig = go.Figure()

fig.add_trace(
    go.Surface(
        x=x, y=y, z=z,
        surfacecolor=intensity,
        colorscale= "ice",
        cmin=0, cmax=255,
        showscale=False
    )
)

fig.add_trace(
    go.Scatter3d(
        x=[sat_x], y=[sat_y], z=[sat_z],
        mode="markers+text",
        marker=dict(size=5, color="red"),
        text=["Satellite"],
        textposition="top center",
        hoverinfo="text+x+y+z"
    )
)

fig.update_layout(
    title="3D Earth with Static Satellite",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode="data",
        camera=dict(eye=dict(x=0, y=0, z=2))  # Center the Earth
    ),
)

app.layout = html.Div([
    html.H1("3D Earth with a Static Satellite"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)