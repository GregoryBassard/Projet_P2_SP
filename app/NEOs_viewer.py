import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from app.utils import load_solar_system, create_3d_axes, display_neos_with_thread, display_neos_without_thread
from app.NEOs import NEOs
from app.Html import create_layout
import time

USE_THREAD = True

time_total = time.time()

fig = go.Figure()

fig.update_layout(
    title='Orbite des Planètes autour du Soleil',
    template='plotly_dark',
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

neos = neo_class.load_neos(1e-6, -4, 0)
time_current = time.time()

if USE_THREAD:
    for trace in display_neos_with_thread(neos):
        fig.add_trace(trace)
else:
    for trace in display_neos_without_thread(neos):
        fig.add_trace(trace)

time_current = time.time()

fig = create_3d_axes(fig, 800000000, 'yellow')

config = {'displayModeBar': False}

fig._config = config

app = dash.Dash(__name__)

app.layout = create_layout(fig)

print(f'total loading app time : {round(time.time()-time_total, 3)}s')

@app.callback(
    Output('solar-system', 'figure'),
    Output('neo-name', 'children'),
    Output('neo-ps', 'children'),
    Output('neo-ts', 'children'),
    Output('neo-range', 'children'),
    Output('last-obs', 'children'),
    Output('neo-diameter', 'children'),
    Output('neo-ip', 'children'),
    Input('solar-system', 'clickData')
)
def update_orbital_visibility(click_data):
    global selected_neo_name

    if click_data:
        name = fig.data[click_data['points'][0]['curveNumber']].name

        if '(neo)' not in name:
            return dash.no_update
        
        for trace in fig.data:
            if name in trace.name:
                if 'Orbite ' in trace.name:
                    trace.visible = True
                else:
                    trace.marker.color = 'white'
                    trace.marker.size = 8
                    trace.textfont.size = 16
                    trace.textfont.color = 'white'
            elif '(neo)' in trace.name:
                if 'Orbite ' in trace.name:
                    trace.visible = False
                else:
                    trace.marker.color = 'gray'
                    trace.marker.size = 4
                    trace.textfont.size = 12
                    trace.textfont.color = 'lightgray'
        for neo in neos:
            if neo.name in name:
                neo_name = neo.name
                ps = neo.ps
                ts = neo.ts
                range = neo.range
                last_obs = neo.last_obs
                diameter = neo.diameter
                ip = neo.ip

        return fig, f"Name: {neo_name}", f"Palermo Scale: {ps}", f"Torino Scale: {ts}", f"Range: {range}", f"Last Obs: {last_obs}", f"Diameter: {diameter}", f"Impact probability: {ip}"
    return fig, None, None, None, None, None, None, None

server = app.server

if __name__ == '__main__':
    app.run(debug=False, port=8050, use_reloader=False)
