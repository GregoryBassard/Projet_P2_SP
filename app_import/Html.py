from dash import dcc, html
import plotly.graph_objects as go
from app_import.NEOs import NEOs
import dash_daq as daq

def create_layout(neos_viewer_fig:go.Figure, neos:list) -> html.Div:
    app_title = html.P(
        id="app_title", children=["Neo Info"]
    )

    neo_dropdown = dcc.Dropdown(
        id="neo-dropdown-component",
        options=[
            {"label": f"{neo.name}", "value": neo.name} for neo in neos
        ],
        clearable=False,
        value="Select a NEO",
        placeholder="Select a NEO",
    )

    neo_infos = html.Div(
        id="panel-side-neo-infos",
        children=[
            html.P(
                id="panel-side-neo-infos-NEO-name",
                children=["NEO Name : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
            html.P(
                id="panel-side-neo-infos-NEO-diameter",
                children=["Diameter : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
            html.P(
                id="panel-side-neo-infos-NEO-mass",
                children=["Mass : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
            html.P(
                id="panel-side-neo-infos-NEO-energy",
                children=["Energy : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
            html.P(
                id="panel-side-neo-infos-NEO-first-observation",
                children=["First Observation : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
            html.P(
                id="panel-side-neo-infos-NEO-brightness",
                children=["Brightness : "],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "left"}
            ),
        ]
    )

    side_panel_layout = html.Div(
        id="panel-side",
        children=[
            app_title,
            neo_infos
        ],
    )

    orbit_toggle = daq.ToggleSwitch(
        id="control-panel-toggle-orbit",
        value=True,
        label=["Hide orbit", "Show orbit"],
        color="#ffe102",
        style={"color": "#black"}
    )

    neos_viewer = html.Div(
        id="neos-viewer",
        children=[
            html.Div(id="neos-viewer-header", children=[
                html.Div(id="neo-dropdown", children=neo_dropdown),
                orbit_toggle
            ]),
            dcc.Graph(
                id="neos-viewer-fig",
                figure=neos_viewer_fig,
                style={"height": "100%", "width": "100%"}
	        ),
        ]
    )

    time_left = html.Div(
        id="control-panel-time-left",
        children=[
            html.P(
                id="control-panel-time-left-text",
                children=["Time left"],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}
            ),
            html.Div(
                id="control-panel-time-left-components",
                children=[
                    daq.LEDDisplay(
                        id="control-panel-time-left-year-component",
                        value="000",
                        label="Year",
                        size=40,
                        color="#fec036",
                        backgroundColor="#2b2b2b",
                    ),
                    daq.LEDDisplay(
                        id="control-panel-time-left-month-component",
                        value="00",
                        label="Month",
                        size=40,
                        color="#fec036",
                        backgroundColor="#2b2b2b",
                    ),
                    daq.LEDDisplay(
                        id="control-panel-time-left-day-component",
                        value="00",
                        label="Day",
                        size=40,
                        color="#fec036",
                        backgroundColor="#2b2b2b",
                    ),
                    daq.LEDDisplay(
                        id="control-panel-time-left-hour-minute-second-component",
                        value="00:00:00",
                        label="HH:MM:SS",
                        size=40,
                        color="#fec036",
                        backgroundColor="#2b2b2b",
                    )
                ]
            )
        ],
    )

    impact_probability_indicator = html.Div(
        id="control-panel-ip-indicator",
        children=[
            html.P(
                id="control-panel-impact-probability-text",
                className="tooltip",
                children=[
                    "Impact Probability",
                    html.Span(
                        className="tooltiptext",
                        children=[
                            "Impact probability classification :",
                            html.Br(),
                            "negligible (< 0.001%)",
                            html.Br(),
                            "low (0.001% - 0.1%)",
                            html.Br(),
                            "concerning (> 1%)"
                        ]
                    )
                ],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}
            ),
            html.Div(
                id="control-panel-ip-indicator-wrapper",
                className="tooltip",
                children=[
                    html.Span( 
                        "N/A% or ~ 1 in N/A chance that he will strike",
                        id="control-panel-ip-indicator-tooltip-text",
                        className="tooltiptext",
                        style={"margin-top": "8.5rem", "font-weight": "bold"}
                    ),
                    html.Div(
                        children=[
                            html.Span("negligible", style={"text-align": "center", "color": "white", "font-size": "12px"}),
                            html.Div(
                                id="control-panel-ip-indicator-negligible",
                                style={"box-shadow": "0 0 5px rgb(80,80,80)", "background-color": "rgb(80,80,80)"}
                            ),
                        ],
                        style={"display": "grid", "alignItems": "center", "margin": "10px"}
                    ),
                    html.Div(
                        children=[
                            html.Span("low", style={"text-align": "center", "color": "white", "font-size": "12px"}),
                            html.Div(
                                id="control-panel-ip-indicator-low",
                                style={"box-shadow": "0 0 5px rgb(80,80,80)", "background-color": "rgb(80,80,80)"}
                            ),
                        ],
                        style={"display": "grid", "alignItems": "center", "margin": "10px"}
                    ),
                    html.Div(
                        children=[
                            html.Span("concerning", style={"text-align": "center", "color": "white", "font-size": "12px"}),
                            html.Div(
                                id="control-panel-ip-indicator-concerning",
                                style={"box-shadow": "0 0 5px rgb(80,80,80)", "background-color": "rgb(80,80,80)"}
                            )
                        ],
                        style={"display": "grid", "alignItems": "center", "margin": "10px"}
                    ),
                ]
            )
        ]
    )

    speed = html.Div(
        id="control-panel-speed",
        children=[
            daq.Gauge(
                id="control-panel-speed-component",
                label={"label": "Impact Velocity", "style": {"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}},
                min=0,
                max=150000,
                showCurrentValue=True,
                value=3600,
                size=175,
                digits=0,
                units="km/h",
                color="#fec036",
                scale={"labelInterval": 5, "interval": 10000}
            )
        ],
        n_clicks=0,
    )

    ps_indicator = html.Div(
        id="control-panel-ps-indicator",
        children=[
            daq.Tank(
                id="control-panel-ps-indicator-component",
                label={"label": "Palermo Scale (Hazardous)", "style": {"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}},
                value=-1,
                min=-10,
                max=1,
                width=80,
                color="#fec036",
                showCurrentValue=True,
            )
        ]
    )

    panel_lower = html.Div(
        id="control-panel", #panel-lower
        children=[
            html.P(
                id="control-panel-title",
                children=["Selected Neo Next Possible Impact Dashboard"],
                style={"color": "#fff", "fontSize": 22, "fontWeight": "bold", "textAlign": "center"}
            ),
            html.Div(
                id="control-panel-0", #panel-lower-0
                children=[speed, time_left, ps_indicator, impact_probability_indicator],
            )
        ]
    )

    control_panel = html.Div(
        id="control-panel-wrapper",
        children=[
            panel_lower
        ],
    )

    main_panel = html.Div(
        id="panel-main",
        children=[
            dcc.Interval(id="interval", interval=1000, n_intervals=0),
            neos_viewer,
            control_panel
        ],
    )

    root_layout = html.Div(
        id="root",
        children=[
            side_panel_layout,
            main_panel
        ],
    )

    return root_layout