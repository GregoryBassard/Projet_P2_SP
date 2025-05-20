from dash import dcc, html
import plotly.graph_objects as go
from app_import.NEOs import NEOs
import dash_daq as daq

def create_layout(neos_viewer_fig:go.Figure, neos:list) -> html.Div:
    side_panel_title = html.P(
        id="app_title", children=["Selected Neo Info"]
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
        children=[ #Name, Diameter, Mass, Energy, First Observation, Brightness
            html.Table(
                id="neo-infos-table",
                children=[
                    html.Tr(
                        children=[
                            html.Th(
                                id="neo-infos-name",
                                children=[
                                    "Name"
                                ]
                            ),
                            html.Th(id="neo-infos-name-value", children=["N/A"]),
                        ]
                    ),
                    html.Tr(
                        children=[
                            html.Td(
                                id="neo-infos-diameter",
                                children=[
                                    "Diameter",
                                ]
                            ),
                            html.Td(id="neo-infos-diameter-value", children=["N/A"]),
                        ]
                    ),
                    html.Tr(
                        children=[
                            html.Td(
                                id="neo-infos-mass",
                                children=[
                                    "Mass",
                                ]
                            ),
                            html.Td(id="neo-infos-mass-value", children=["N/A"]),
                        ]
                    ),
                    html.Tr(
                        children=[
                            html.Td(
                                id="neo-infos-energy",
                                children=[
                                    "Energy",
                                    html.Div(
                                        className="tooltip",
                                        children=[
                                            html.Img(
                                                src="/assets/question_mark.png",
                                                style={"width": "12px", "height": "12px", "margin-left": "6px"}
                                            ),
                                            html.Span(
                                                className="tooltiptext",
                                                children=[
                                                    "The kinetic Energy released at the impact.",
                                                    html.Br(),
                                                    "Measured in Megaton of TNT equivalent",
                                                ]
                                            )
                                        ],
                                        style={"display": "inline-flex"}
                                    )
                                ]
                            ),
                            html.Td(id="neo-infos-energy-value", children=["N/A"]),
                        ]
                    ),
                    html.Tr(
                        children=[
                            html.Td(
                                id="neo-infos-first-obs",
                                children=[
                                    "Discovery",
                                ]
                            ),
                            html.Td(id="neo-infos-first-observation-value", children=["N/A"]),
                        ]
                    )
                ]
            )
        ]
    )

    neos_filter = html.Div(
        id="panel-side-neos-filter",
        children=[
            html.P(
                id="neos-filter-title",
                children=["NEOs Filters"],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}
            ),
            # Two separate DatePickers for Start and End Dates
            html.Div(
                children=[
                    html.P("Start Date:", style={"color": "#fff", "fontSize": 16, "marginTop": "10px", "marginBottom": "5px"}),
                    dcc.DatePickerSingle(
                        id="neos-filter-start-date-picker",
                        date="2025-01-01", # Set an initial date
                        display_format="DD/MM/YYYY", # Changed format
                        style={"color": "#fff", "fontSize": 16, "textAlign": "center"}
                    ),
                    html.P("End Date:", style={"color": "#fff", "fontSize": 16, "marginTop": "15px", "marginBottom": "5px"}),
                    dcc.DatePickerSingle(
                        id="neos-filter-end-date-picker",
                        date="3025-01-01", # Set an initial date
                        display_format="DD/MM/YYYY", # Changed format
                        style={"color": "#fff", "fontSize": 16, "textAlign": "center"}
                    ),
                ],
                style={"margin-top": "20px", "textAlign": "center"} # Center the pickers
            ),
            # Impact Probability Filter
            html.Div(
                children=[
                    html.P("Impact Probability:", style={"color": "#fff", "marginTop": "10px"}),
                    dcc.Checklist(
                        id="neos-filter-impact-probability",
                        options=[
                            {"label": " Negligible", "value": "negligible"},
                            {"label": " Low", "value": "low"},
                            {"label": " Concerning", "value": "concerning"},
                        ],
                        value=["negligible", "low", "concerning"], # Default to all selected
                        inline=False,
                        style={"color": "#fff"}
                    )
                ],
                style={"margin-top": "20px", "margin-left": "0px", "margin-right": "0px"}
            ),
            # Diameter Filter
            html.Div(
                children=[
                    html.P("Diameter (km):", style={"color": "#fff", "marginTop": "10px"}),
                    dcc.RangeSlider(
                        id="neos-filter-diameter-slider",
                        min=0,
                        max=500, # You can adjust this max value based on your data
                        step=50,
                        value=[0, 5006],
                        marks={}, # Removed all marks for diameter
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ],
                style={"margin-top": "20px", "margin-left": "0px", "margin-right": "0px"}
            ),
            # Energy Slider
            html.Div(
                children=[
                    html.P("Energy (Megatons of TNT):", style={"color": "white", "marginTop": "10px"}),
                    dcc.RangeSlider(
                        id="neos-filter-energy-slider",
                        min=0,
                        max=1000, # Example max value, adjust based on your data's actual max energy
                        step=100, # Adjust step as needed
                        value=[0, 1000], # Default to full range
                        marks={},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ],
                style={"margin-top": "20px", "margin-left": "0px", "margin-right": "0px"}
            ),
        ],
        style={"margin-top": "20px", "width": "100%", "padding-left": "5px", "padding-right": "5px"}
    )

    side_panel_layout = html.Div(
        id="panel-side",
        children=[
            side_panel_title,
            neo_infos,
            neos_filter
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
                children=[
                    "Impact Probability",
                    html.Div(
                        className="tooltip",
                        children=[
                            html.Img(
                                src="/assets/question_mark.png",
                                style={"width": "12px", "height": "12px", "margin-left": "6px"},
                            ),
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
                    )
                ],
                style={"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center", "display": "block ruby"}
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
                size=150,
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
                theme="dark",
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
                children=[speed, time_left, impact_probability_indicator, ps_indicator],
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