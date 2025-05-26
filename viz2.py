import dash
from dash import dcc, html
from dash.dependencies import Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from time import sleep

from app_import.NEOs import NEOs, load_neos


def create_palermo_scale_distribution_chart(neos: list) -> dcc.Graph:
    palermo_scale_values = []
    
    for neo in neos:
        if neo.data:
            ps_for_neo = []
            for event in neo.data:
                if 'ps' in event and event['ps'] is not None:
                    try:
                        ps_for_neo.append(float(event['ps']))
                    except ValueError:
                        continue
            
            if ps_for_neo:
                palermo_scale_values.append(max(ps_for_neo))

    if not palermo_scale_values:
        return dcc.Graph(
            figure=go.Figure().update_layout(
                title={
                    'text': "No NEO data available for Palermo Scale distribution.",
                    'y':0.5, 'x':0.5, 'xanchor': 'center', 'yanchor': 'middle',
                    'font': {'size': 18, 'color': 'white'}
                },
                template="plotly_dark",
                plot_bgcolor='#111111',
                paper_bgcolor='#111111'
            )
        )

    bins = [-np.inf, -2, 0, np.inf] # Modified bins
    bin_labels = [
        "PS < -2 (Very Low to Low Risk)", # Modified label
        "-2 <= PS < 0 (Elevated Risk)",
        "PS >= 0 (Potentially Significant)"
    ]

    categorized_data = pd.cut(palermo_scale_values, bins=bins, labels=bin_labels, right=False)
    ps_counts = pd.Series(categorized_data).value_counts().reindex(bin_labels, fill_value=0)

    colors = ['#57fe36', '#feb836', '#fe3636'] # Modified colors to match the number of bins

    fig = go.Figure(
        data=[
            go.Bar(
                x=ps_counts.index,
                y=ps_counts.values,
                marker_color=colors,
                text=ps_counts.values,
                textposition='auto',
                hovertemplate="<b>%{x}</b><br>Number of NEOs: %{y}<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title={
            'text': "Distribution of NEO Impact Risk (Palermo Scale)",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': 'white'}
        },
        xaxis_title="Palermo Scale Category",
        yaxis_title="Number of NEOs",
        template="plotly_dark",
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font_color='white',
        xaxis=dict(
            tickangle=-45,
            showgrid=False,
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title_font=dict(size=16),
            tickfont=dict(size=12)
        ),
        margin=dict(l=50, r=50, t=80, b=100),
        hovermode="closest"
    )

    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    load_dotenv()
    NASA_API_KEY = os.getenv('NASA_API_KEY')

    print("Loading NEOs data for visualization...")
    initial_neos_limit = 100
    neos_data = load_neos(ip_min=1e-6, ps_min=-4, limit=initial_neos_limit) 
    
    for i, neo in enumerate(neos_data):
        neo.get_data_and_summary()
        sleep(0.1)

    print("NEO data loading complete.")

    app = dash.Dash(__name__)

    neo_dropdown_options = [{'label': neo.name, 'value': neo.name} for neo in neos_data if neo.name]
    initial_selected_neo = neo_dropdown_options[0]['value'] if neo_dropdown_options else None

    app.layout = html.Div(
        style={
            'backgroundColor': '#111111',
            'color': 'white',
            'fontFamily': 'Inter, sans-serif',
            'padding': '20px',
            'minHeight': '100vh',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center'
        },
        children=[
            html.H1(
                "Combined NEO Dashboard",
                style={
                    'textAlign': 'center',
                    'marginBottom': '30px',
                    'fontSize': '2.8em',
                    'color': '#fec036'
                }
            ),
            
            html.Div(
                style={
                    'width': '90%',
                    'maxWidth': '1200px',
                    'marginBottom': '40px',
                    'padding': '20px',
                    'border': '1px solid #333333',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 8px rgba[0, 0, 0, 0.2]',
                    'backgroundColor': '#1e1e1e'
                },
                children=[
                    html.H2(
                        "Selected NEO Details",
                        style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#fec036'}
                    ),
                    dcc.Dropdown(
                        id='neo-selector-dropdown',
                        options=neo_dropdown_options,
                        value=initial_selected_neo,
                        clearable=False,
                        style={'width': '60%', 'margin': '0 auto 20px auto', 'color': 'black', 'fontFamily': 'Inter, sans-serif'}
                    ),
                    html.Div(
                        id='selected-neo-info',
                        style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'},
                        children=[
                            html.Div(className='info-box', children=[
                                html.H3("Diameter (km)", style={'textAlign': 'center'}),
                                html.P(id='diameter-value', style={'textAlign': 'center', 'fontSize': '1.5em'})
                            ]),
                            html.Div(className='info-box', children=[
                                html.H3("Impact Velocity (km/h)", style={'textAlign': 'center'}),
                                html.P(id='velocity-value', style={'textAlign': 'center', 'fontSize': '1.5em'})
                            ]),
                            html.Div(className='info-box', children=[
                                html.H3("Palermo Scale", style={'textAlign': 'center'}),
                                html.P(id='palermo-scale-value', style={'textAlign': 'center', 'fontSize': '1.5em'})
                            ]),
                            html.Div(className='info-box', children=[
                                html.H3("Impact Probability", style={'textAlign': 'center'}),
                                html.P(id='impact-probability-value', style={'textAlign': 'center', 'fontSize': '1.5em'})
                            ]),
                        ]
                    )
                ]
            ),

            html.Div(
                style={
                    'width': '90%',
                    'maxWidth': '1200px',
                    'padding': '20px',
                    'border': '1px solid #333333',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                    'backgroundColor': '#1e1e1e'
                },
                children=[
                    html.H2(
                        "Overall NEO Impact Risk Distribution",
                        style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#fec036'}
                    ),
                    html.P(
                        "This chart provides a broader view of the impact risk across all tracked NEOs. "
                        "Most objects fall into lower risk categories, indicating that while monitoring is extensive, "
                        "the number of truly threatening objects is small.",
                        style={
                            'textAlign': 'center',
                            'maxWidth': '800px',
                            'margin': '0 auto 20px auto',
                            'fontSize': '1.0em',
                            'lineHeight': '1.5'
                        }
                    ),
                    create_palermo_scale_distribution_chart(neos_data)
                ]
            ),
        ]
    )

    @app.callback(
        [Output('diameter-value', 'children'),
         Output('velocity-value', 'children'),
         Output('palermo-scale-value', 'children'),
         Output('impact-probability-value', 'children')],
        [dash.dependencies.Input('neo-selector-dropdown', 'value')]
    )
    def update_selected_neo_info(selected_neo_name):
        if not selected_neo_name:
            return "N/A", "N/A", "N/A", "N/A"

        selected_neo = next((neo for neo in neos_data if neo.name == selected_neo_name), None)

        if selected_neo and selected_neo.summary and selected_neo.data:
            diameter_km = float(selected_neo.summary['value'].get('diameter', 0)) if 'diameter' in selected_neo.summary['value'] else 0
            
            velocity_km_s = float(selected_neo.summary['value'].get('v_imp', 0)) if 'v_imp' in selected_neo.summary['value'] else 0
            velocity_km_h = velocity_km_s * 3600

            max_ps = -np.inf
            corresponding_ip = 0.0
            if selected_neo.data:
                for event in selected_neo.data:
                    if 'ps' in event and event['ps'] is not None:
                        try:
                            current_ps = float(event['ps'])
                            if current_ps > max_ps:
                                max_ps = current_ps
                                corresponding_ip = float(event.get('ip', 0.0))
                        except ValueError:
                            pass

            palermo_scale_str = f"{max_ps:.2f}" if max_ps != -np.inf else "N/A"
            impact_probability_str = f"{(corresponding_ip * 100):.7f}% (1 in ~{int(1/corresponding_ip)})" if corresponding_ip > 0 else "Negligible"

            return (
                f"{diameter_km:.3f} km",
                f"{velocity_km_h:.2f} km/h",
                palermo_scale_str,
                impact_probability_str
            )
        return "N/A", "N/A", "N/A", "N/A"

    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)