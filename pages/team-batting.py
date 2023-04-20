
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pybaseball import team_batting

# Creating Batting Stats Dataframe
batting_data_2022=team_batting(2022)
batting_data=batting_data_2022[['Season','Team','G','PA','H','1B','2B','3B','HR','R','RBI','SO','K%','BB','BB%','IBB','BB/K','HBP','SF','SH','SB','CS','AVG','OBP','SLG','OPS','BABIP','LD%','GB%','FB%','wOBA','wRC','WAR']].copy()
batting_data.rename(
    columns={
        'G': 'Games Played (G)',
        'PA':'Plate Appearances (PA)',
        'H':'Hits (H)',
        '1B':'Singles (1B)',
        '2B':'Doubles (2B)',
        '3B':'Triples (3B)',
        'HR':'Home Runs (HR)',
        'R':'Runs Scored (R)',
        'RBI':'Runs Batted In (RBI)',
        'SO':'Strikeouts (SO)',
        'K%':'Strikeout Percentage (K%)',
        'BB':'Walks (BB)',
        'BB%':'Walk Percentage (BB%)',
        'IBB':'Intentional Walks (IBB)',
        'BB/K':'Walk-to-Strikeout Ratio (BB/K)',
        'HBP':'Hit By Pitches (HBP)',
        'SF':'Sacrifice Flies (SF)',
        'SH':'Sacrifice Hits (Bunts)',
        'SB':'Stolen Bases',
        'CS':'Caught Stealing (CS)',
        'AVG':'Batting Average (AVG)',
        'OBP':'On-Base Percentage (OBP)',
        'SLG':'Slugging Percentage (SLG)',
        'OPS':'On-Base Plus Slugging (OPS)',
        'BABIP':'Batting Average on Balls in Play (BABIP)',
        'LD%':'Line Drive Percentage (LD%)',
        'GB%':'Ground Ball Percentage (GD%)',
        'FB%':'Fly Ball Percentage (FB%)',
        'wOBA':'Weighted On-Base Average (wOBA)',
        'wRC':'Weighted Runs Created (wRC)',
        'WAR':'Wins Above Replacement (WAR)'
    },
    inplace=True
)
batting_data.loc[:,('Season')]

# Creating and Setting an Index
batting_data.loc[:,('Team')]
batting_data.set_index('Team',inplace=True)

# Removing Batting Dataframe Column
batting_data.drop(columns=['Season'],inplace=True)

# Sorting Lists for Dashboard Components
batting_stat_list=[x for x in batting_data.columns]
batting_team_list=[x for x in batting_data.index]

# Registering the Team Batting Page
dash.register_page(__name__)

# The Batting Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('MLB Batting Results (2022 Season)',className='text-center text-danger mt-3 mb-2 fs-1'),
    html.P("This is the page to be at to review MLB batters' results from the 2022 MLB Season! 20 statistical measures and 130 MLB players combine on this page to create a comparison bar chart among players that qualified for the 2022 MLB batting title. To qualify for this achievement, players must have had at least 3.1 plate appearances per game (or at least 502 plate appearances during the entire season). To operate this bar chart, simply select the statistical measure that you'd like to compare players with and choose what players you'd like to review on the chart below!",className='text-center text-dark mb-3 mt-2 fs-6'),
    html.H3('Batting Data Bar Chart', className='text-primary text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='team_batting_chart',
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
                html.P('Please select a statistical measure to compare teams with.',className='text-center text-dark fs-5 mt-3')
            ],
            width=6
        ),
        dbc.Col(
            children=[
                html.P("Please select a team(s) you'd like to review above.",className='text-center text-dark fs-5 mt-3')
            ]
        )
    ]),
    # Dropdown Boxes
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Dropdown(
                    id='team_batting_stat_choice',
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
                    id='team_dropdown',
                    options=[
                        dict(label=x,value=x) for x in batting_team_list
                    ],
                    multi=True,
                    placeholder='Please select a team to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['HOU'],
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
    Output('team_batting_chart','figure'),
    Input('team_batting_stat_choice','value'),
    Input('team_dropdown','value'),
)

def charts(stat_selection4,list_of_teams):
    if len(stat_selection4)==0:
        stat_selection4 = ['Home Runs (HR)']

    if len(list_of_teams)==0:
        list_of_teams = ['HOU']

    # Making Batting Data Subset
    team_batting_data_subset=batting_data.loc[list_of_teams,stat_selection4].copy().reset_index()

    # Batting Chart
    team_batting_figure=px.bar(
        team_batting_data_subset,
        x=stat_selection4,
        y='Team',
        orientation='h',
        text_auto=True,
        title=' '
    )

    team_batting_figure.update_xaxes(
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

    team_batting_figure.update_yaxes(
        title_text='Team Abbreviation',
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
        linecolor='black'
    )

    team_batting_figure.update_layout(
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

    team_batting_figure.update_traces(
        marker_color='darkblue',
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14
)
    return team_batting_figure
