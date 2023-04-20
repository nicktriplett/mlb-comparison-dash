
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pybaseball import batting_stats

# Creating Batting Stats Dataframe
batting_data_2022=batting_stats(2022)
batting_data=batting_data_2022[['Season','Name','Team','G','PA','H','2B','3B','HR','R','RBI','SO','BB','IBB','HBP','SB','AVG','OBP','SLG','OPS','wOBA','wRC','WAR']].copy()
batting_data.rename(
    columns={
        'G': 'Games Played (G)',
        'PA':'Plate Appearances (PA)',
        'H':'Hits (H)',
        '2B':'Doubles (2B)',
        '3B':'Triples (3B)',
        'HR':'Home Runs (HR)',
        'R':'Runs Scored (R)',
        'RBI':'Runs Batted In (RBI)',
        'SO':'Strikeouts (SO)',
        'BB':'Walks (BB)',
        'IBB':'Intentional Walks (IBB)',
        'HBP':'Hit By Pitches (HBP)',
        'SB':'Stolen Bases',
        'AVG':'Batting Average (AVG)',
        'OBP':'On-Base Percentage (OBP)',
        'SLG':'Slugging Percentage (SLG)',
        'OPS':'On-Base Plus Slugging (OPS)',
        'wOBA':'Weighted On-Base Average (wOBA)',
        'wRC':'Weighted Runs Created (wRC)',
        'WAR':'Wins Above Replacement (WAR)'
    },
    inplace=True
)
batting_data.loc[:,('Season')]

# Creating and Setting an Index
batting_data['Name (Team)'] = batting_data['Name'] + ' (' + batting_data['Team'] + ')'
batting_data.loc[:,('Name (Team)')]
batting_data.set_index('Name (Team)',inplace=True)

# Removing Batting Dataframe Columns
batting_data.drop(columns=['Season','Name','Team'],inplace=True)

# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in batting_data.columns]
batting_player_list = [x for x in batting_data.index]

# Registering the Player Batting Page
dash.register_page(__name__)

# The Batting Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('MLB Player Batting Results (2022 Season)',className='text-center text-danger mt-3 mb-2 fs-1'),
    html.P("This is the page to be at to review MLB batters' results from the 2022 MLB Season! 20 statistical measures and 130 MLB players combine on this page to create a comparison bar chart among players that qualified for the 2022 MLB batting title. To qualify for this achievement, players must have had at least 3.1 plate appearances per game (or at least 502 plate appearances during the entire season). To operate this bar chart, simply select the statistical measure that you'd like to compare players with and choose what players you'd like to review on the chart below!",className='text-center text-dark mb-3 mt-2 fs-6'),
    html.H3('Player Batting Data Bar Chart', className='text-primary text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='batter_chart',
                    className='m-4',
                    config=dict(displayModeBar=False),
                ),
            ],
            width=10,
            className='offset-md-1'
        )
    ]),
    # User Commands
    dbc.Row([
        dbc.Col(
            children=[
                html.P('Please select a statistical measure to compare players with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a player(s) you'd like to review above.",className='text-center text-dark fs-5 mt-3')
            ]
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='batter_stat_choice',
                    options=[
                        dict(label=x,value=x) for x in batting_stat_list
                    ],
                    className='mt-1 mb-3',
                    value='Home Runs (HR)',
                    multi=False,
                    optionHeight=25,
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='player_dropdown',
                    options=[
                        dict(label=x,value=x) for x in batting_player_list
                    ],
                    multi=True,
                    placeholder='Please select a player to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['Aaron Judge (NYY)'],
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-2'
        )
    ]),

    # Data Sources and Information
    html.Div(
        children=[
            'Data Source: ',
            html.A(
                'Pybaseball',
                href='https://github.com/jldbc/pybaseball',className='text-primary fs-5'
            ),
        ],
        className='text-dark text-center fs-5 mt-5'
    ),
    html.Div(
        children=[
            'Baseball Data Abbreviations and Definitions: ',
            html.A(
                'MLB Glossary',
                href='https://www.mlb.com/glossary',className='text-primary fs-5'
            )
        ],
        className='text-dark text-center fs-5 mb-2'
    )
    ],
    fluid=True
)

# Section for the Callback
@callback(
    Output('batter_chart','figure'),
    Input('batter_stat_choice','value'),
    Input('player_dropdown','value'),
)

def charts(stat_selection1,list_of_players):
    if len(stat_selection1)==0:
        stat_selection1 = ['Home Runs (HR)']

    if len(list_of_players)==0:
        list_of_players = ['Aaron Judge (NYY)']

    # Making Batting Data Subset
    batting_data_subset=batting_data.loc[list_of_players,stat_selection1].copy().reset_index()

    # Batting Chart
    batting_figure=px.bar(
        batting_data_subset,
        x=stat_selection1,
        y='Name (Team)',
        orientation='h',
        text_auto=True,
        title=' '
    )

    batting_figure.update_xaxes(
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    batting_figure.update_yaxes(
        title_text='Player(s) (Team Abbreviation)',
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        categoryorder='total ascending'
    )

    batting_figure.update_layout(
        title_font={
        'size': 24,
        'color': 'black'
        },
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,t=0,b=0),
        showlegend=False,
    )

    batting_figure.update_traces(
        marker_color='darkblue',
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14
)
    return batting_figure
