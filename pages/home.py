
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')



layout = html.Div(
    children=[
        html.H1('MLB Comparison Dashboard (2022 Season)',className='text-center text-danger mt-3 mb-2 fs-1'),
        html.H2('A BSAN 406 Project Created by Nick Triplett',className='text-center text-dark mt-1 mb-2 fs-3'),
        html.P("Welcome to my Major League Baseball (MLB) Comparison Dashboard! This dashboard was created as part of many assigned projects through an analytics-oriented class at Southern Illinois University - Carbondale. Inside this dashboard, you'll discover multiple graphs and various statistical results coming from the 2022 MLB season. More information about each graph and results can be found on the other pages of this dashboard. Enjoy using this MLB dashboard!",className='text-center text-dark mb-0 mt-4 fs-6'),
        html.Img(src=dash.get_asset_url('mlb-logo-image.png'),style={'width':'46%'},className='mb-0 mx-5'),
        html.Img(src=dash.get_asset_url('mlb-word-image.png'),style={'width':'42%'},className='mb-0 ml-5'),
        html.Div(
            children=[
                'Image Source: ',
                html.A(
                    'LogoLook',
                    href='https://logolook.net/mlb-logo/',className='text-primary fs-4'
                ),
        ],
        className='text-dark text-center fs-4 mt-0'
        ),
        html.P('Note: This image was edited for the purpose of changing its appearance for this dashboard.',className='text-dark text-center fs-5')
    ]
)
