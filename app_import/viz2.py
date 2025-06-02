from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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
                plot_bgcolor="#1e1e1e",
                paper_bgcolor='#1e1e1e'
            )
        )

    bins = [-np.inf, -2, 0, np.inf]
    bin_labels = [
        "PS < -2 (Very Low to No Risk)",
        "-2 <= PS < 0 (Elevated Risk)",
        "PS >= 0 (Potentially Significant)"
    ]

    categorized_data = pd.cut(palermo_scale_values, bins=bins, labels=bin_labels, right=False)
    ps_counts = pd.Series(categorized_data).value_counts().reindex(bin_labels, fill_value=0)

    colors = ['#57fe36', '#feb836', '#fe3636']

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
        plot_bgcolor='#1e1e1e',  
        paper_bgcolor='#1e1e1e', 
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