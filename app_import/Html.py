from dash import dcc, html
import plotly.graph_objects as go
from app_import.NEOs import NEOs
import dash_daq as daq

def create_layout(neos_viewer_fig:go.Figure, neos:list) -> html.Div:
    app_title = html.P(
        id="app_title", children=["Neos Viewer Dashboard"]
    )

    neo_dropdown = dcc.Dropdown(
        id="neo-dropdown-component",
        options=[
            {"label": f"{neo.name}", "value": neo.name} for neo in neos
        ],
        clearable=False,
        value="h45-k1",
    )

    side_panel_layout = html.Div(
        id="panel-side",
        children=[
            app_title,
            html.Div(id="neo-dropdown", children=neo_dropdown)
        ],
    )

    orbit_toggle = daq.ToggleSwitch(
        id="control-panel-toggle-orbit",
        value=True,
        label=["Hide orbit", "Show orbit"],
        color="#ffe102",
        style={"color": "#black"},
    )

    neos_viewer = html.Div(
        id="neos-viewer",
        children=[
            orbit_toggle,
            dcc.Graph(
                id="neos-viewer-fig",
                figure=neos_viewer_fig,
                style={"height": "100%", "width": "100%"}
	        ),
        ]
    )

    main_panel = html.Div(
        id="panel-main",
        children=[
            dcc.Interval(id="interval", interval=1 * 2000, n_intervals=0),
            neos_viewer
        ],
    )

    root_layout = html.Div(
        id="root",
        children=[
            side_panel_layout,
            main_panel,
        ],
    )

    return root_layout