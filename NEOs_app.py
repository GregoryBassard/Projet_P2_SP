import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from app_import.utils import load_solar_system, create_3d_axes, display_neos_with_thread, display_neos_without_thread
from app_import.NEOs import NEOs, load_neos
from app_import.Html import create_layout
import time
import os
from dotenv import load_dotenv

USE_THREAD = False

selected_neo_name = "Select a NEO    "

load_dotenv(override=True)
use_thread_env = os.getenv("USE_THREAD")
if use_thread_env is not None:
    if str(use_thread_env).lower() == 'true':
        USE_THREAD = True

time_total = time.time()

neos_viewer_fig = go.Figure()

neos_viewer_fig.update_layout(
    title="3D NEOs Viewer",
    template="plotly_dark",
    showlegend=False,
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(
            eye=dict(x=0.3, y=0.3, z=0.3)
        )
    ),
    autosize=True,
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    margin={"t": 0, "r": 0, "b": 0, "l": 0},
    hovermode=False
)

neos_viewer_fig = load_solar_system(neos_viewer_fig)

neos_viewer_fig.layout.uirevision = True

neo_class = NEOs()
time_current = time.time()

neos = load_neos(1e-6, -4, 5)
time_current = time.time()

if USE_THREAD:
    for trace in display_neos_with_thread(neos):
        neos_viewer_fig.add_trace(trace)
else:
    for trace in display_neos_without_thread(neos):
        neos_viewer_fig.add_trace(trace)

time_current = time.time()

neos_viewer_fig = create_3d_axes(neos_viewer_fig, 800000000, "yellow")

config = {"displayModeBar": False}

neos_viewer_fig._config = config

app = dash.Dash(__name__)

app.layout = create_layout(neos_viewer_fig, neos)
app.title = "NEOs Viewer"

print(f"total loading app time : {round(time.time()-time_total, 3)}s")

def highlight_neo(trace:go.Scatter3d):
    trace.marker.color = "#fec036"
    trace.marker.size = 6
    trace.textfont.size = 14
    trace.textfont.color = "#fec036"

def unhighlight_neo(trace:go.Scatter3d):
    trace.marker.color = "white"
    trace.marker.size = 5
    trace.textfont.size = 12
    trace.textfont.color = "white"

def show_orbit(trace:go.Scatter3d):
    if "Orbite " in trace.name:
        trace.visible = True
    else:
        pass

def hide_orbit(trace:go.Scatter3d):
    if "Orbite " in trace.name:
        trace.visible = False
    else:
        pass

@app.callback(
    Output("neos-viewer-fig", "figure"),
    Output("neo-dropdown-component", "value"),
    [Input("neos-viewer-fig", "clickData"), Input("neo-dropdown-component", "value"), Input("control-panel-toggle-orbit", "value")]
)
def update_neo(click_data, selected_neo, toggle_orbit):
    global selected_neo_name
    ctx = dash.callback_context
    name = selected_neo_name

    if not ctx.triggered:
        return neos_viewer_fig, selected_neo_name[:-6]

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "neos-viewer-fig" and click_data:
        name = neos_viewer_fig.data[click_data["points"][0]["curveNumber"]].name

    elif trigger_id == "neo-dropdown-component" and selected_neo:
        name = selected_neo + " (neo)"

    if "(neo)" not in name:
        return dash.no_update, selected_neo_name[:-6]
    
    selected_neo_name = name
    
    for trace in neos_viewer_fig.data:
        if name in trace.name:
            if toggle_orbit:
                show_orbit(trace)
                highlight_neo(trace)
            else:
                hide_orbit(trace)
                highlight_neo(trace)
        elif "(neo)" in trace.name:
            hide_orbit(trace)
            unhighlight_neo(trace)

    return neos_viewer_fig, selected_neo_name[:-6]

server = app.server

port = int(os.environ.get("PORT", 8050))
app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)