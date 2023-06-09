
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
        html.P("Welcome to my Major League Baseball (MLB) Comparison Dashboard! This dashboard was created as part of many assigned projects through an analytics-oriented class at Southern Illinois University - Carbondale. Inside this dashboard, you'll discover multiple graphs and various statistical results coming from the 2022 MLB season. More information about each graph and results can be found on the other pages of this dashboard. Special thanks are due to Dr. Tyson Van Alfen for all of his help in getting this dashboard running and uploaded online! Enjoy using this MLB dashboard!",className='text-center text-dark mb-4 mt-4 fs-6'),
        dbc.Row([
            dbc.Col(
                html.Img(
                    src=dash.get_asset_url('mlb-logo-image.png'),
                    style={
                        'width':'100%',
                        'vertical-align':'top',
                        'object-fit':'contain'}
                ),
                width={'size': 5}
            ),
            dbc.Col(
                html.Div(
                    children=[
                        html.Img(
                            src=dash.get_asset_url('mlb-word-image.png'),
                            style={
                                'width': '100%',
                                'vertical-align':'top',
                                'object-fit':'contain'}
                        )
                    ],
                style={'margin-top': '45px'}
                ),
                width={'size': 5}
            )
            ],
            justify='center'
        ),
        html.Div(
            children=[
                'Image Source: ',
                html.A(
                    'LogoLook',
                    href='https://logolook.net/mlb-logo/',className='text-primary fs-4'
                ),
        ],
        className='text-dark text-center fs-4 mt-3'
        ),
        html.P('Note: This image was edited for the purpose of changing its appearance for this dashboard.',className='text-dark text-center fs-5')
    ]
)
