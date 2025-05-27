import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from app_import.utils import load_solar_system, create_3d_axes, display_neos_with_thread, display_neos_without_thread
from app_import.NEOs import NEOs, load_neos
from app_import.Html import create_layout
import time
import os
import pandas as pd
from dotenv import load_dotenv
from app_import.viz2 import create_palermo_scale_distribution_chart # Import the function

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

time_current = time.time()

neos = load_neos(1e-6, -4, 0)
time_current = time.time()

if USE_THREAD:
    for trace in display_neos_with_thread(neos):
        neos_viewer_fig.add_trace(trace)
else:
    for trace in display_neos_without_thread(neos):
        neos_viewer_fig.add_trace(trace)

for neo in neos:
    neo.get_data_and_summary()
    neo.get_time_left()

time_current = time.time()

neos_viewer_fig = create_3d_axes(neos_viewer_fig, 800000000, "yellow")

config = {"displayModeBar": False}

neos_viewer_fig._config = config

app = dash.Dash(__name__)

# TODO: import viz2 to app
risk_distribution_fig = create_palermo_scale_distribution_chart(neos).figure # Call the function to get the figure

app.layout = create_layout(neos_viewer_fig, risk_distribution_fig, neos)
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
    if "orbit " in trace.name:
        trace.visible = True
    else:
        pass

def hide_orbit(trace:go.Scatter3d):
    if "orbit " in trace.name:
        trace.visible = False
    else:
        pass

@app.callback(
    Output("neos-viewer-fig", "figure"),
    Output("neo-dropdown-component", "value"),
    Output("control-panel-ip-indicator-negligible","style"),
    Output("control-panel-ip-indicator-low","style"),
    Output("control-panel-ip-indicator-concerning","style"),
    Output("control-panel-ip-indicator-tooltip-text","children"),
    Output("control-panel-speed-component","value"),
    Output("control-panel-ps-indicator-component", "value"),
    Output("control-panel-ps-indicator-component", "color"),
    Output("neo-infos-name-value", "children"),
    Output("neo-infos-diameter-value", "children"),
    Output("neo-infos-mass-value", "children"),
    Output("neo-infos-energy-value", "children"),
    Output("neo-infos-first-observation-value", "children"),
    [Input("neos-viewer-fig", "clickData"), Input("neo-dropdown-component", "value"), Input("control-panel-toggle-orbit", "value")]
)
def update_neo(click_data, selected_neo, toggle_orbit):
    global selected_neo_name
    ctx = dash.callback_context
    name = selected_neo_name

    if not ctx.triggered:
        return neos_viewer_fig, selected_neo_name[:-6], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "neos-viewer-fig" and click_data:
        name = neos_viewer_fig.data[click_data["points"][0]["curveNumber"]].name

    elif trigger_id == "neo-dropdown-component" and selected_neo:
        name = selected_neo + " (neo)"

    if "(neo)" not in name:
        return dash.no_update, selected_neo_name[:-6], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
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

    off_style={"box-shadow": "0 0 5px rgb(80,80,80)", "background-color": "rgb(80,80,80)"}
    
    negligible_style = off_style
    low_style = off_style
    concerning_style = off_style
    
    for neo in neos:
        if neo.name == selected_neo_name[:-6]:
            # Impact Probability
            ip = float(pd.DataFrame(neo.data).sort_values(by="date", ascending=True).reset_index(drop=True)["ip"][0])
            if ip * 100 < 1.0e-3:
                negligible_style = {"box-shadow": "0 0 5px rgb(0,255,0)", "background-color": "rgb(0,255,0)"}
            elif ip * 100 < 1.0:
                low_style = {"box-shadow": "0 0 5px rgb(255,170,10)", "background-color": "rgb(255,170,10)"}
            else:
                concerning_style = {"box-shadow": "0 0 5px rgb(255,0,0)", "background-color": "rgb(255,0,0)"}

            # Tooltip
            ip_tool_children = f"{(ip * 100):.7f}% or 1 in ~{int(1/ip)} chance that he will strike"

            # Speed
            speed = float(neo.summary['value']['v_imp']) * 3600

            # PS
            ps = float(pd.DataFrame(neo.data).sort_values(by="date", ascending=True).reset_index(drop=True)["ps"][0])
            if ps > 0:
                ps_color = "#fe3636"
            elif ps > -2:
                ps_color = "#feb836"
            elif ps > -5:
                ps_color = "#f1fe36"
            else:
                ps_color = "#57fe36"

            # Neo Infos
            neo_infos = neo.summary['value']
            neo_infos_name = selected_neo_name[:-6]
            neo_infos_diameter = f"{float(neo_infos['diameter']):.3f} km"
            neo_infos_mass = f"{float(neo_infos['mass']):.0f} kg"
            neo_infos_energy = f"{float(neo_infos['energy']):.3f} Mt TNT"
            neo_infos_first_observation = neo_infos['first_obs']
    

    return neos_viewer_fig, selected_neo_name[:-6], negligible_style, low_style, concerning_style, ip_tool_children, speed, ps, ps_color, neo_infos_name, neo_infos_diameter, neo_infos_mass, neo_infos_energy, neo_infos_first_observation

@app.callback(
    Output("control-panel-time-left-year-component", "value"),
    Output("control-panel-time-left-month-component", "value"),
    Output("control-panel-time-left-day-component", "value"),
    Output("control-panel-time-left-hour-minute-second-component", "value"),
    Input("interval", "n_intervals")
)
def update_time_left(n_intervals):

    if selected_neo_name == "Select a NEO    ":
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    for neo in neos:
        if neo.name == selected_neo_name[:-6]:
            neo.get_time_left()
            return neo.years, neo.months, neo.days, neo.hms
    return "00", "00", "00", "00:00:00"

@app.callback(
    Output("neos-viewer-fig", "figure", allow_duplicate=True),
    Input("panel-side-options-checklist", "value"),
    prevent_initial_call=True
)
def update_fig_with_options(value):
    for trace in neos_viewer_fig.data:
        if "Axis" in trace.name:
            if "3axis" in value:
                trace.visible = True
            else:
                trace.visible = False
        if "neo" in trace.name:
            if "neo_name" not in value:
                trace.textfont.size = 1
            else:
                trace.textfont.size = 12
        if trace.name in ["Mercury", "Venus", "Mars"] or trace.name in ["Orbit Mercury", "Orbit Venus", "Orbit Mars"]:
            if "only_earth" in value:
                trace.visible = False
            else:
                trace.visible = True


    return neos_viewer_fig

@app.callback(
    Output("neos-viewer-fig", "figure", allow_duplicate=True),
    Output("neo-dropdown-component", "options", allow_duplicate=True),
    Output("neo-dropdown-component", "value", allow_duplicate=True),
    Input("neos-filter-start-date-picker", "date"),
    Input("neos-filter-end-date-picker", "date"),
    Input("neos-filter-impact-probability", "value"),
    Input("neos-filter-diameter-slider", "value"),
    Input("neos-filter-energy-slider", "value"),
    prevent_initial_call=True
)
def update_fig_from_filter(filter_start_date, filter_end_date, filter_ip, filter_diameter, filter_energy):
    global selected_neo_name
    neos_filtered = []

    for neo in neos:
        if neo.isFilter(filter_start_date, filter_end_date, filter_ip, filter_diameter, filter_energy):
            neos_filtered.append(neo.name)

    for trace in neos_viewer_fig.data:
        if "neo" in trace.name and "orbit " not in trace.name:
            if trace.name[:-6] in selected_neo_name:
                if trace.name[:-6] in neos_filtered:
                    highlight_neo(trace)
                else:
                    unhighlight_neo(trace)
            if trace.name[:-6] in neos_filtered:
                trace.visible = True
            else:
                trace.visible = False
        elif "orbit " in trace.name:
            if trace.name[6:-6] in selected_neo_name:
                if trace.name[6:-6] in neos_filtered:
                    show_orbit(trace)
                else:
                    hide_orbit(trace)

    if selected_neo_name[:-6] not in neos_filtered:
        selected_neo_name = "Select a NEO    "

    options=[
        {"label": f"{neo_name}", "value": neo_name} for neo_name in neos_filtered
    ]
    return neos_viewer_fig, options, selected_neo_name


server = app.server
port = int(os.environ.get("PORT", 8050))
app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)