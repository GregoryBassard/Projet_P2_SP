import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import load_solar_system, create_3d_axes, display_neos_with_thread, display_neos_without_thread
from NEOs import NEOs, NEOsDisplayThread
import time

USE_THREAD = True

last_click_timestamp = 0
last_neo_name = ''
time_total = time.time()

fig = go.Figure()

fig.update_layout(
    title='Orbite des Planètes autour du Soleil',
    template='plotly_dark',
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
    display_neos_with_thread(neos)
else:
    for trace in display_neos_without_thread(neos):
        fig.add_trace(trace)

time_current = time.time()

fig = create_3d_axes(fig, 800000000, 'yellow')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(
        id='solar-system',
        figure=fig,
        style={'height': '90vh'}
    )
])
print(f'total loading app time : {round(time.time()-time_total, 3)}s')

@app.callback(
    Output('solar-system', 'figure'),
    Input('solar-system', 'clickData')
)
def update_orbital_visibility(click_data):
    global last_click_timestamp
    global last_neo_name

    if click_data:
        current_time = time.time()
        name = fig.data[click_data['points'][0]['curveNumber']].name

        if '(neo)' not in name:
            return dash.no_update
        
        if last_neo_name == name:
            if current_time - last_click_timestamp < 0.5:
                return dash.no_update

        last_click_timestamp = current_time
        last_neo_name = name
        
        for trace in fig.data:
            if trace.name == f'Orbite {name}':  
                trace.visible = not trace.visible

    return fig

if __name__ == '__main__':
    app.run(debug=False)
