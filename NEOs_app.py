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
            eye=dict(x=0.5, y=0.5, z=0.5)
        )
    ),
    autosize=True,
    paper_bgcolor="#1e1e1e",
    plot_bgcolor="#1e1e1e",
    margin={"t": 0, "r": 0, "b": 0, "l": 0},
    # hovermode=False
)

neos_viewer_fig = load_solar_system(neos_viewer_fig)

neos_viewer_fig.layout.uirevision = True

neo_class = NEOs()
time_current = time.time()

neos = load_neos(1e-6, -4, 3)
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

@app.callback(
    Output("solar-system", "figure"),
    Output("neo-name", "children"),
    Output("neo-summary", "children"),
    Output("neo-data", "children"),
    Input("solar-system", "clickData")
)
def update_orbital_visibility(click_data):
    global selected_neo_name

    if click_data:
        name = neos_viewer_fig.data[click_data["points"][0]["curveNumber"]].name

        if "(neo)" not in name:
            return dash.no_update
        
        for trace in neos_viewer_fig.data:
            if name in trace.name:
                if "Orbite " in trace.name:
                    trace.visible = True
                else:
                    trace.marker.color = "white"
                    trace.marker.size = 8
                    trace.textfont.size = 16
                    trace.textfont.color = "white"
            elif "(neo)" in trace.name:
                if "Orbite " in trace.name:
                    trace.visible = False
                else:
                    trace.marker.color = "gray"
                    trace.marker.size = 4
                    trace.textfont.size = 12
                    trace.textfont.color = "lightgray"
        for neo in neos:
            if neo.name in name:
                if neo.summary is None:
                    neo.get_data_and_summary()

                summary = html.Table(
                    [html.Tr([html.Td(key), html.Td(value)]) for key, value in neo.summary['value'].items()],
                    style={"border": "2px solid black", "width": "100%", "textAlign": "left"}
                )

                data = html.Table(
                    [
                        html.Tr([html.Th("Date"), html.Th("TS"), html.Th("Sigma VI"), html.Th("Energy"), html.Th("PS"), html.Th("IP")])
                    ]
                    + 
                    [
                        html.Tr([html.Td(entry["date"]), html.Td(entry["ts"]), html.Td(entry["sigma_vi"]), html.Td(entry["energy"]), html.Td(entry["ps"]), html.Td(entry["ip"])]) for entry in neo.data
                    ],
                    style={"border": "1px solid black", "width": "100%", "textAlign": "left"}
                )

                # for entry in neo.data:
                #     row = html.Tr([html.Td(entry["date"]), html.Td(entry["ts"]), html.Td(entry["sigma_vi"]), html.Td(entry["energy"]), html.Td(entry["ps"]), html.Td(entry["ip"])])
                #     # data.append(row)
                #     data.children += [row]

                return neos_viewer_fig, f"Name: {name}", summary, data

    return neos_viewer_fig, "Name: N/A", html.H5("N/A"), html.H5("N/A")
server = app.server

port = int(os.environ.get("PORT", 8050))
app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)