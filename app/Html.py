from dash import dcc, html

def create_layout(neos_viewer_fig):
    return  html.Div([
        html.Div([
            html.Div("Filter", style={
                "border": "2px solid black",
                "width": "20%",
                "height": "100vh",
                "fontSize": "2rem",
                "textAlign": "center",
                "paddingTop": "1rem",
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
                "flexDirection": "column"
            }),
            html.Div([
                html.Div(
                    children=[
                        html.H1("Name: ", id="neo-name", style={"textAlign":"center"}),
                        html.H3("Palermo Scale: ", id="neo-ps", style={"paddingTop" : "0.5rem"}),
                        html.H3("Torino Scale: ", id="neo-ts", style={"paddingTop" : "0.5rem"}),
                        html.H3("Range: ", id="neo-range", style={"paddingTop" : "0.5rem"}),
                        html.H3("Last Obs: ", id="last-obs", style={"paddingTop" : "0.5rem"}),
                        html.H3("Diameter: ", id="neo-diameter", style={"paddingTop" : "0.5rem"}),
                        html.H3("Impact probability: ", id="neo-ip", style={"paddingTop" : "0.5rem"})
                    ],
                    style={
                        "border": "2px solid black",
                        "height": "35%",
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
    ])