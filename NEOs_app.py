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

load_dotenv(override=True)
if os.getenv('USE_THREAD').lower() == 'true':
    USE_THREAD = True
else:
    USE_THREAD = False

time_total = time.time()

fig = go.Figure()

fig.update_layout(
    title="Orbite des Planetes autour du Soleil",
    template="plotly_dark",
    showlegend=False,
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    )
)

fig = load_solar_system(fig)

fig.layout.uirevision = True

neo_class = NEOs()
time_current = time.time()

neos = load_neos(1e-6, -4, 0)
time_current = time.time()

if USE_THREAD:
    for trace in display_neos_with_thread(neos):
        fig.add_trace(trace)
else:
    for trace in display_neos_without_thread(neos):
        fig.add_trace(trace)

time_current = time.time()

fig = create_3d_axes(fig, 800000000, "yellow")

config = {"displayModeBar": False}

fig._config = config

app = dash.Dash(__name__)

app.layout = create_layout(fig)

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
        name = fig.data[click_data["points"][0]["curveNumber"]].name

        if "(neo)" not in name:
            return dash.no_update
        
        for trace in fig.data:
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
                neo.get_neo_data()

                summary = html.Table(
                    [html.Tr([html.Td(key), html.Td(value)]) for key, value in neo.summary.items()],
                    style={"border": "1px solid black", "width": "100%", "textAlign": "left"}
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

                return fig, f"Name: {name}", summary, data

    return fig, "Name: N/A", html.H5("N/A"), html.H5("N/A")
server = app.server

port = int(os.environ.get("PORT", 8050))
app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)