
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pybaseball import pitching_stats

# Creating Pitching Stats Dataframe
pitching_data_2022=pitching_stats(2022)
pitching_data=pitching_data_2022[['Season','Name','Team','W','L','G','IP','TBF','H','R','ER','HR','BB','HBP','SO','K/9','BB/9','K/BB','AVG','ERA','WHIP','BABIP','FIP','WAR']].copy()
pitching_data.rename(
    columns={
        'W':'Wins (W)',
        'L':'Losses (L)',
        'G':'Games Played (G)',
        'IP':'Innings Pitched (IP)',
        'TBF':'Total Batters Faced (TBF)',
        'H':'Hits (H)',
        'R':'Runs Scored Against (R)',
        'ER':'Earned Runs (ER)',
        'HR':'Home Runs Allowed (HR)',
        'BB':'Walks (BB)',
        'HBP':'Batters Hit By Pitches (HBP)',
        'SO':'Strikeouts (SO)',
        'K/9':'Number of Strikeouts Per 9 Innings (K/9)',
        'BB/9':'Number of Walks Per 9 Innings (BB/9)',
        'K/BB':'Strikeout to Walk Ratio (K/BB)',
        'AVG':"Opponents' Batting Average (AVG)",
        'ERA':'Earned Run Average (ERA)',
        'WHIP':'Walks And Hits Per Inning Pitched (WHIP)',
        'BABIP':'Batting Average on Balls in Play (BABIP)',
        'FIP':'Fielding Independent Pitching (FIP)',
        'WAR':'Wins Above Replacement (WAR)'
    },
    inplace=True
)
pitching_data.loc[:,('Season')]

# Creating and Setting an Index
pitching_data['Name (Team)'] = pitching_data['Name'] + ' (' + pitching_data['Team'] + ')'
pitching_data.loc[:,('Name (Team)')]
pitching_data.set_index('Name (Team)',inplace=True)

# Removing Batting Dataframe Columns
pitching_data.drop(columns=['Season','Name','Team'],inplace=True)

# Sorting a List for Dashboard Components
pitching_stat_list=[x for x in pitching_data.columns]

# Registering the Pitching Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('MLB Pitching Results (2022 Season)',className='text-center text-danger mt-3 mb-2 fs-1'),
    html.P("This page is the destination for reviewing MLB pitchers' results from the 2022 MLB Season! Included in the chart below is more than 20 statistical measures that determine how pitchers performed during play last season. Also included is 45 plotted points that represent the 45 MLB pitchers that qualified for 2022 MLB pitching awards. To qualify to be a pitcher on this graph, pitchers must have pitched at least 1 inning per game (or at least 162 innings during the entire season) last season. To make this scatter plot work, select two statistical measures (for both axes) that you'd like to use to compare pitchers with on this chart!",className='text-center text-dark mb-3 mt-2 fs-6'),
    html.H3('Pitching Data Scatter Plot', className='text-primary text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='pitcher_chart',
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
                html.P('Please select a statistical measure for the X-axis to compare players with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a statistical measure for the Y-axis to compare players with.",className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='pitcher_stat_dropdown1',
                    options=[
                        dict(label=x,value=x) for x in pitching_stat_list
                    ],
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value='Innings Pitched (IP)',
                    clearable=False
                )
            ],
            width=4,
            className='offset-md-1'
        ),
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='pitcher_stat_dropdown2',
                    options=[
                        dict(label=x,value=x) for x in pitching_stat_list
                    ],
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value='Earned Run Average (ERA)',
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
    Output('pitcher_chart','figure'),
    Input('pitcher_stat_dropdown1','value'),
    Input('pitcher_stat_dropdown2','value')
)

def charts(stat_selection2,stat_selection3):
        # Pitching Chart
    pitching_figure=px.scatter(
        pitching_data,
        x=stat_selection2,
        y=stat_selection3,
        title=' ',
        hover_name=pitching_data.index
    )

    pitching_figure.update_xaxes(
        title_font={
        'size': 18,
        'color': 'black'
        },
        tickfont=dict(
            size=14,
            color='black'
        ),
        showgrid=True,
        gridwidth=0.5,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    pitching_figure.update_yaxes(
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
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
    )

    pitching_figure.update_layout(
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

    pitching_figure.update_traces(
        marker_color='red',
        marker_size=11,
        marker_line_color='black',
        marker_line_width=1,
        textfont_size=14
)

    return pitching_figure
