from dash import dcc, html
import plotly.graph_objects as go
from app_import.NEOs import NEOs
import dash_daq as daq

def create_layout(neos_viewer_fig:go.Figure, risk_distribution_fig:go.Figure, neos:list) -> html.Div:
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
                id="panel-side-neo-infos-title",
                children=["Selected NEO Information"],
                style={"color": "#fff", "fontSize": 22, "fontWeight": "bold", "textAlign": "center"}
            ),
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
                        max=500, 
                        step=50,
                        value=[0, 5006],
                        marks={}, 
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
                        max=1000, 
                        step=100, 
                        value=[0, 1000], 
                        marks={},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ],
                style={"margin-top": "20px", "margin-left": "0px", "margin-right": "0px"}
            ),
        ],
        style={"margin-top": "20px", "width": "100%", "padding-left": "5px", "padding-right": "5px"}
    )

    orbit_toggle = daq.ToggleSwitch(
        id="control-panel-toggle-orbit",
        value=True,
        label=["Hide orbit", "Show orbit"],
        color="#ffe102",
        style={"color": "#black"}
    )

    options = html.Div(
        html.Div(
            id="panel-side-options",
            children=[
                html.P(
                    id="panel-side-options-title",
                    children=["Viewer Options"],
                    style={"color": "#fff", "fontSize": 22, "fontWeight": "bold", "textAlign": "center"}
                ),
                dcc.Checklist(
                    id="panel-side-options-checklist",
                    options=[
                        {"label": "Show 3 axis", "value": "3axis"},
                        {"label": "Show neo name", "value": "neo_name"},
                        {"label": "Show only Earth", "value": "only_earth"}
                    ],
                    value=["3axis", "neo_name"],
                    labelStyle={"display": "block", "color": "#fff", "fontSize": 18, "textAlign": "left"}
                )
            ]
        )
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
                label={"label": "Hazardous (Palermo Scale)", "style": {"color": "#fff", "fontSize": 20, "fontWeight": "bold", "textAlign": "center"}},
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

    side_panel_layout = html.Div(
        id="panel-side",
        children=[
            options,
            neo_infos,
            neos_filter
        ],
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

    neos_viewer_layout = html.Div(
        id="neos_viewer_layout",
        children=[
            side_panel_layout,
            main_panel,
        ],
    )

    introduction_layout = html.Div(
        id="introduction_layout",
        children=[
            html.H1("NEOs Sentry", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            html.Strong("NEOs (Near-Earth Objects)"),
                            " are asteroids and comets whose orbits bring them within approximately 50 million kilometers of Earth's orbit. These celestial bodies are remnants from the formation of our solar system. While many NEOs exist, only a very small fraction pose any potential impact risk to Earth.",
                            html.Br(),
                            html.Br(),
                            " These objects are continuously observed and cataloged by astronomers worldwide to understand their trajectories and potential interactions with Earth."
                        ]
                    )
                ]
            ),
            html.H2("How Sentry Objects are Monitored", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            " The vast majority of potentially hazardous NEOs are meticulously tracked and monitored by systems like NASA's ",
                            "NEOs. Sentry is an automated collision monitoring system that continuously scans the catalog of NEOs for any future close approaches to Earth. When an object is identified as a \"Sentry object\", it means its orbit is being very carefully calculated and refined with every new observation. ",
                        ]
                    )
                ]
            )
        ]
    )

    neos_viewer_text_layout = html.Div(
        id="neos-viewer-text",
        children=[
            html.H2("Under Surveillance NEOs Viewer", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            "This application is an interactive dashboard for visualizing and exploring NEOs that are monitored for potential impact risks with Earth.",
                            html.Br(),
                            "It uses data from",
                            html.Strong(" NASA's Sentry system "),
                            "to display the orbits, physical characteristics, and risk assessments of asteroids and comets whose paths bring them close to our planet."
                        ]
                    )
                ]
            ),
            html.H3("How to Use it (a voir si on garde)", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.Ul([
                        html.Li([
                            html.Strong("3D Viewer : "),
                            "Use the 3D viewer to see the orbits of NEOs in the solar system. Select a specific NEO from the dropdown menu or by clicking on it in the viewer."
                        ]),
                        html.Li([
                            html.Strong("Filters : "),
                            "On the left panel, filter NEOs by date, impact probability, diameter, and energy. Adjust the sliders and checkboxes to refine the dropdown and the displayed NEOs."
                        ]),
                        html.Li([
                            html.Strong("NEO Information : "),
                            "When you select a NEO, detailed information about its size, mass, energy, discovery date, and impact probability will appear in the side panel."
                        ]),
                        html.Li([
                            html.Strong("Viewer Options : "),
                            "Toggle options to show or hide axes, NEO names, or display only Earth and its orbit."
                        ]),
                        html.Li([
                            html.Strong("Impact Dashboard : "),
                            "The control panel displays real-time data such as time left until the next possible impact, impact velocity, impact probability, and the Palermo Scale hazard rating."
                        ]),
                    ]),
                    html.P("Explore the dashboard to learn more about NEOs and their potential risks in an interactive and visual way!")
                ]
            ),
        ]
    )

    risk_distribution_text_layout = html.Div(
        id="risk-distribution-text",
        children=[
            html.H2("Risk Distribution of NEOs", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                        "This dashboard provides an interactive visualization of Near-Earth Objects (NEOs) that are monitored for potential impact risks with Earth. ",
                        "Using real data from ",
                        html.Strong("NASA's Sentry system"),
                        ", the application displays the orbits, physical characteristics, and risk assessments of asteroids and comets whose paths bring them close to our planet.",
                        ]
                    )
                ]
            ),
            html.H3("How to Use the Application", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.Ul(
                    [
                        html.Li("Select a NEO: Use the dropdown menu to choose a specific NEO and view its details, including diameter, impact velocity, Palermo Scale rating, and impact probability."),
                        html.Li("View Risk Distribution: The chart below the details section shows the overall distribution of impact risks (Palermo Scale) for all tracked NEOs."),
                        html.Li("Interpret the Data: Most NEOs fall into lower risk categories, but you can quickly identify objects with higher potential risk using the provided metrics and visualizations."),
                    ], style={"color": "white", "fontSize": "1.05em", "marginBottom": "20px"}),
                ]
            )          
        ]
    )

    risk_distribution_layout = dcc.Graph(
        id="risk-distribution-fig",
        figure=risk_distribution_fig,
        style={"height": "100%", "width": "100%"}
	)

    palermo_scale_text_layout = html.Div(
        id="palermo-scale-text",
        children=[
            html.H2("Understanding the Palermo Technical Impact Hazard Scale", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            "The Palermo Technical Impact Hazard Scale, often simply called the",
                            html.Strong("Palermo Scale"),
                            ", is a way for astronomers to assess the potential threat posed by Near-Earth Objects (NEOs) like asteroids and comets that might collide with Earth.",
                            html.Br(),
                            "Think of it like a sophisticated risk assessment for cosmic impacts. It's not just about how big an object is or how close it gets, it combines several factors to give us a more complete picture of the danger.",
                        ]
                    )
                ]
            ),
            html.H3("Here's a breakdown of what the Palermo Scale tells us :", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.Ul([
                        html.Li([
                            html.Strong("It's a Logarithmic Scale: "),
                            "This means that each increase of \"1\" on the scale represents a tenfold increase in risk. ",
                            "So, an object with a Palermo Scale value of +2 is 100 times more threatening than an object with a value of 0."
                        ]),
                        html.Li([
                            html.Strong("What the Numbers Mean :"),
                            html.Ul([
                                html.Li([
                                    html.B("Values less than -2 : "),
                                    "These mean the object poses basically no significant threat."
                                ]),
                                html.Li([
                                    html.B("Values between -2 and 0 : "),
                                    "These indicate a situation being monitored but not immediately alarming."
                                ]),
                                html.Li([
                                    html.B("A value of 0 : "),
                                    "The risk equals the background hazard."
                                ]),
                                html.Li([
                                    html.B("Values greater than 0 : "),
                                    "These indicate increasingly significant risk."
                                ]),
                            ])
                        ]),
                        html.Li([
                            html.Strong("What it Considers :"),
                            html.Ul([
                                html.Li([
                                    html.B("The probability of impact : "),
                                    "How likely is it to hit Earth?"
                                ]),
                                html.Li([
                                    html.B("The object's size and speed : "),
                                    "Bigger and faster objects carry more energy."
                                ]),
                                html.Li([
                                    html.B("The time until potential impact : "),
                                    "The sooner the impact, the less time to react."
                                ]),
                                html.Li([
                                    html.B("The background hazard : "),
                                    "The average long-term impact risk for objects of similar size."
                                ]),
                            ])
                        ])
                    ])
                ]
            ),
            html.H3("The Palermo Scale Formula :", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            "The Palermo Scale value",
                            html.I("P"),
                            " is calculated using the following formula :",
                            html.Div(
                                style={"textAlign": "center", "margin": "20px 0"},
                                children=[
                                    html.Img(
                                        src="https://latex.codecogs.com/png.image?%7B%5Ccolor%7BWhite%7D%20P%20=%20%5Clog_%7B10%7D%5Cleft(%5Cfrac%7Bp_i%7D%7Bf_B%20%5Ccdot%20T%7D%5Cright)%7D",
                                        style={"height": "48px"}
                                    )
                                ]
                            ),
                            html.Br(),
                            "Where:",
                            html.Ul([
                                html.Li(
                                    children=[
                                        "p",
                                        html.Sub("i"),
                                        " = The impact probability of the specific object."
                                    ]
                                ),
                                html.Li(
                                    children=[
                                        "f",
                                        html.Sub("B"),
                                        " = The background hazard, which is the average long-term impact risk for objects of similar size."
                                    ]
                                ),
                                html.Li("T = The time interval over which the risk is assessed."),
                            ])
                        ]
                    )
                ]
            )
        ]
    )

    conclusion_layout = html.Div(
        id="conclusion_layout",
        children=[
            html.H2("Conclusion", style={"textAlign": "center", "color": "#fff"}),
            html.Div(
                className="text",
                children=[
                    html.P(
                        [
                            "NEOs are a constant presence in our solar system, yet they pose virtually no threat to Earth. Thanks to advanced systems like NASA's Sentry system, these celestial bodies are continuously and meticulously tracked. This ongoing observation allows scientists to refine their orbital calculations with incredible precision. What might initially appear as a potential concern almost always diminishes to a negligible, or even zero, risk as more data is gathered. This rigorous and precise monitoring ensures that any genuine threat would be identified far in advance, giving us ample time to react.",
                            html.Br(),
                            "The vast majority of NEOs are nothing more than harmless cosmic neighbors, simply orbiting the Sun. As demonstrated by various visualizations and the use of a precise threat scale, we can confidently affirm that there are currently no known threats to Earth from any NEOs. The Palermo Scale, with its detailed and scientific approach, provides a clear framework for understanding and communicating the risks associated with these objects. It allows astronomers to prioritize their efforts effectively, ensuring vigilance while recognizing the low likelihood of significant impacts in the foreseeable future.",
                        ]
                    )
                ]
            )
        ],
    )

    root_layout = html.Div(
        id="root",
        children=[
            introduction_layout,
            html.Hr(),
            neos_viewer_text_layout,
            neos_viewer_layout,
            html.Hr(),
            risk_distribution_text_layout,
            risk_distribution_layout,
            palermo_scale_text_layout,
            html.Hr(),
            conclusion_layout,
        ],
    )

    return root_layout