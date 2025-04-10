import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import load_solar_system, create_3d_axes, display_neos_with_thread, display_neos_without_thread
from NEOs import NEOs
import time

USE_THREAD = False

last_click_timestamp = 0
last_neo_name = ''
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

app.layout = html.Div([
    html.Div([
        html.Div("Filter", style={
            "border": "2px solid black",
            "width": "15%",
            "height": "100vh",
            "fontSize": "2rem",
            "textAlign": "center",
            "paddingTop": "1rem",
        }),

        html.Div([
            dcc.Graph(
                id='solar-system',
                figure=fig,
                style={"height": "100%", "width": "100%"},
                config={"responsive": True}
            )
        ], style={
            "border": "2px solid black",
            "width": "55%",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column"
        }),

        html.Div([
            html.Div("CLICKED NEO INFO", style={
                "border": "2px solid black",
                "height": "50%",
                "fontSize": "2rem",
                "textAlign": "center",
                "paddingTop": "2rem"
            }),
            html.Div("3D VI FOR CLICKED NEO", style={
                "border": "2px solid black",
                "height": "50%",
                "fontSize": "2rem",
                "textAlign": "center",
                "paddingTop": "2rem"
            }),
        ], style={
            "width": "30%",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column"
        })
    ], style={
        "display": "flex",
        "flexDirection": "row"
    })
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
    app.run(debug=True, port=8050, use_reloader=False)
