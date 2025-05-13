import dash
from dash import html, dcc, Input, Output
import plotly.graph_objs as go

# Import your custom NEO loader
from app_import.NEOs import load_neos

# Load NEOs and extract data
neos = load_neos(1e-6, -4, 0)
for neo in neos:
    neo.get_data_and_summary()

# Reference objects and their heights (in meters)
REFERENCE_OBJECTS = {
    "Human (avg)": 1.75,
    "Double-decker Bus": 4.4,
    "Giraffe": 5.5,
    "Telephone Pole": 10,
    "Eiffel Tower": 324,
    "Mount Everest": 8848
}

# Precompute options
def get_neo_options():
    return [
        {
            "label": f"{neo.name} ({neo.data['diameter_max_meters']:.2f} m)",
            "value": neo.data['diameter_max_meters']
        }
        for neo in neos if 'diameter_max_meters' in neo.data
    ]

USER_HEIGHTS = get_neo_options()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Height Comparison Visualizer"

app.layout = html.Div([
    html.H1("Height Comparison Tool"),

    dcc.RadioItems(
        id='input-height',
        options=USER_HEIGHTS,
        value=USER_HEIGHTS[0]['value'] if USER_HEIGHTS else None,
        labelStyle={'display': 'block'},
        style={'marginBottom': '20px'}
    ),

    dcc.Graph(id='comparison-graph'),

    html.Div(id='comparison-text')
])


# Callback to update the graph and comparison list
@app.callback(
    Output('comparison-graph', 'figure'),
    Output('comparison-text', 'children'),
    Input('input-height', 'value')
)
def update_graph(user_height):
    if user_height is None or user_height <= 0:
        return go.Figure(), "Please select a valid asteroid."

    labels = ["Asteroid Diameter"] + list(REFERENCE_OBJECTS.keys())
    heights = [user_height] + list(REFERENCE_OBJECTS.values())

    fig = go.Figure(go.Bar(
        x=labels,
        y=heights,
        text=[f"{h:.2f} m" for h in heights],
        textposition='auto'
    ))

    fig.update_layout(
        yaxis_title='Height (meters)',
        xaxis_title='Objects',
        height=500,
        margin=dict(t=40, b=40),
    )

    comparisons = []
    for obj, ref_height in REFERENCE_OBJECTS.items():
        count = user_height / ref_height
        comparisons.append(f"≈ {count:.2f} × {obj}")

    return fig, html.Ul([html.Li(c) for c in comparisons])


# Optional: Dynamically update dropdown (not required unless the NEO list changes)
@app.callback(
    Output('input-height', 'options'),
    Input('input-height', 'value')
)
def update_neo_selection(selected_value):
    return get_neo_options()


if __name__ == '__main__':
    app.run(debug=True)
