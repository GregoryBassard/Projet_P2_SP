from dash import dcc, html

def create_layout(neos_viewer_fig):
    return html.Div([
        html.Div([
            html.H2("Filter", style={
                "textAlign": "center",
                "padding": "1rem 0",
                "borderBottom": "2px solid black"
            }),

            html.Label("Diameter Threshold", style={"padding": "1rem 0", "display": "block", "fontWeight": "bold"}),
            dcc.Slider(
                id="diameter-slider",
                min=0,
                max=1,
                step=0.1,
                value=0.5,
                marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),

            html.Br(),

            html.Label("Sentry Only", style={"paddingTop": "2rem", "display": "block", "fontWeight": "bold"}),
            dcc.Checklist(
                options=[
                    {"label": "Yes", "value": "yes"}
                ],
                value=[],
                id="sentry-toggle",
                inputStyle={"marginRight": "0.5rem", "marginLeft": "0.5rem"}
            ),

            html.Label("Include Observed", style={"paddingTop": "2rem", "display": "block", "fontWeight": "bold"}),
            dcc.RadioItems(
                options=[
                    {"label": "All", "value": "all"},
                    {"label": "Only Recent", "value": "recent"}
                ],
                value="all",
                id="observed-toggle",
                labelStyle={"display": "block", "marginTop": "0.5rem"}
            )
        ], style={
            "border": "2px solid black",
            "width": "20%",
            "height": "100vh",
            "fontSize": "1rem",
            "padding": "1rem",
            "overflowY": "auto",
            "boxSizing": "border-box"
        }),

        html.Div([
            dcc.Graph(
                id="solar-system",
                figure=neos_viewer_fig,
                style={"height": "100%", "width": "100%"},
                config={"responsive": True}
            )
        ], style={
            "border": "2px solid black",
            "width": "50%",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
        }),

        html.Div([
            html.Div(
                children=[
                    html.H1("Name: ", id="neo-name", style={"textAlign": "center"}),
                    html.H3("Palermo Scale: ", id="neo-ps", style={"paddingTop": "0.5rem"}),
                    html.H3("Torino Scale: ", id="neo-ts", style={"paddingTop": "0.5rem"}),
                    html.H3("Range: ", id="neo-range", style={"paddingTop": "0.5rem"}),
                    html.H3("Last Obs: ", id="last-obs", style={"paddingTop": "0.5rem"}),
                    html.H3("Diameter: ", id="neo-diameter", style={"paddingTop": "0.5rem"}),
                    html.H3("Impact probability: ", id="neo-ip", style={"paddingTop": "0.5rem"})
                ],
                style={
                    "border": "2px solid black",
                    "height": "35%",
                    "overflowY": "auto",
                    "padding": "0.5rem",
                    "boxSizing": "border-box"
                }
            ),
            html.Div("3D VI FOR CLICKED NEO", style={
                "border": "2px solid black",
                "height": "65%",
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
