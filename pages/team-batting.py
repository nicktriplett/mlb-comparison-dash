
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from pybaseball import team_pitching

# Creating Pitching Stats Dataframe
pitching_data_2022=team_pitching(2022)
pitching_data=pitching_data_2022[['Season','Team','Pitches','Strikes','W','L','SV','BS','G','CG','IP','TBF','H','R','ER','HR','BB','HBP','SO','WP','BK','K/9','BB/9','K/BB','GB/FB','LD%','GB%','FB%','LOB%','H/9','HR/9','AVG','ERA','WHIP','BABIP','FIP','WAR']].copy()
pitching_data['Team']=pitching_data['Team'].replace(
    {
        'NYY':'New York Yankees',
        'BOS':'Boston Red Sox',
        'BAL':'Baltimore Orioles',
        'TBR':'Tampa Bay Rays',
        'TOR':'Toronto Blue Jays',
        'CLE':'Cleveland Guardians',
        'DET':'Detroit Tigers',
        'KCR':'Kansas City Royals',
        'MIN':'Minnesota Twins',
        'CHW':'Chicago White Sox',
        'HOU':'Houston Astros',
        'OAK':'Oakland Athletics',
        'LAA':'Los Angeles Angels',
        'SEA':'Seattle Mariners',
        'TEX':'Texas Rangers',
        'NYM':'New York Mets',
        'ATL':'Atlanta Braves',
        'WSN':'Washington Nationals',
        'PHI':'Philadelphia Phillies',
        'MIA':'Miami Marlins',
        'STL':'St. Louis Cardinals',
        'CHC':'Chicago Cubs',
        'PIT':'Pittsburgh Pirates',
        'MIL':'Milwaukee Brewers',
        'CIN':'Cincinnati Reds',
        'SDP':'San Diego Padres',
        'LAD':'Los Angeles Dodgers',
        'SFG':'San Francisco Giants',
        'ARI':'Arizona Diamondbacks',
        'COL':'Colorado Rockies'
    }
)
pitching_data.rename(
    columns={
        'W':'Wins (W)',
        'L':'Losses (L)',
        'SV':'Saves (SV)',
        'BS':'Blown Saves (BS)',
        'G':'Games Played (G)',
        'CG':'Complete Games (CG)',
        'IP':'Innings Pitched (IP)',
        'TBF':'Total Batters Faced (TBF)',
        'H':'Hits (H)',
        'R':'Runs Scored Against (R)',
        'ER':'Earned Runs (ER)',
        'HR':'Home Runs Allowed (HR)',
        'BB':'Walks (BB)',
        'HBP':'Batters Hit By Pitches (HBP)',
        'SO':'Strikeouts (SO)',
        'WP':'Wild Pitches',
        'BK':'Balks',
        'K/9':'Number of Strikeouts Per 9 Innings (K/9)',
        'BB/9':'Number of Walks Per 9 Innings (BB/9)',
        'K/BB':'Strikeout to Walk Ratio (K/BB)',
        'GB/FB':'Ground Ball-to-Fly Ball Ratio (GB/FB)','LD%':'Line Drive Percentage (LD%)',
        'GB%':'Ground Ball Percentage (GB%)',
        'FB%':'Fly Ball Percentage (FB%)',
        'LOB%':'Runners Left On Base Percentage (LOB%)',
        'H/9':'Hits Given Up Per 9 Innings (H/9)',
        'HR/9':'Home Runs Given Up Per 9 Innings (HR/9)',
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
pitching_data.loc[:,('Team')]
pitching_data.set_index('Team',inplace=True)

# Removing Pitching Dataframe Column
pitching_data.drop(columns=['Season'],inplace=True)

# Sorting a List for Dashboard Components
pitching_stat_list=[x for x in pitching_data.columns]
pitching_team_list=[x for x in pitching_data.index]

# Registering the Pitching Page
dash.register_page(__name__)

# The Pitching Chart Page
layout=dbc.Container(
    children=[
    # Title and Dashboard Explanation
    html.H1('MLB Team Pitching Results (2022 Season)',className='text-center text-danger mt-3 mb-2 fs-1'),
    html.P("This is the best place to be for pitching data sorted by teams! Much like the Team Batting Data page, this page includes more than 30 different statistical measures and all 30 MLB teams' seasonal pitching data from the 2022 campaign. This graph works as you select different statistical measures and choose different MLB teams to review with those statistical measures.",className='text-center text-dark mb-3 mt-2 fs-6'),
    html.H3('Team Pitching Data Bar Chart', className='text-primary text-center fs-2 mt-3 mb-0'),
    # The Graph
    dbc.Row([
        dbc.Col(
            children=[
                dcc.Graph(
                    id='team_pitching_bar_chart',
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
                    id='team_pitching_stat_choice',
                    options=[
                        dict(label=x,value=x) for x in pitching_stat_list
                    ],
                    className='mt-1 mb-3',
                    value='Earned Run Average (ERA)',
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
                    id='pitching_team_dropdown',
                    options=[
                        dict(label=x,value=x) for x in pitching_team_list
                    ],
                    multi=True,
                    placeholder='Please select a team to review.',
                    optionHeight=25,
                    className='mt-1 mb-3',
                    value=['Houston Astros'],
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
    Output('team_pitching_bar_chart','figure'),
    Input('team_pitching_stat_choice','value'),
    Input('pitching_team_dropdown','value'),
)

def charts(stat_selection5,list_of_pitching_teams):
    if len(stat_selection5)==0:
        stat_selection5 = ['Earned Run Average (ERA)']

    if len(list_of_pitching_teams)==0:
        list_of_pitching_teams = ['Houston Astros']

    # Making Batting Data Subset
    team_pitching_data_subset=pitching_data.loc[list_of_pitching_teams,stat_selection5].copy().reset_index()

    # Batting Chart
    team_pitching_figure=px.bar(
        team_pitching_data_subset,
        x=stat_selection5,
        y='Team',
        orientation='h',
        text_auto=True,
        title=' ',
        color='Team',
        color_discrete_map={
            'Arizona Diamondbacks':'#A71930',
            'Atlanta Braves':'#13274F',
            'Baltimore Orioles':'#DF4601',
            'Boston Red Sox':'#BD3039',
            'Chicago White Sox':'#27251F',
            'Chicago Cubs':'#0E3386',
            'Cincinnati Reds':'#C6011F',
            'Cleveland Guardians':'#00385D',
            'Colorado Rockies':'#333366',
            'Detroit Tigers':'#0C2340',
            'Houston Astros':'#002D62',
            'Kansas City Royals':'#004687',
            'Los Angeles Angels':'#BA0021',
            'Los Angeles Dodgers':'#005A9C',
            'Miami Marlins':'#000000',
            'Milwaukee Brewers':'#12284B',
            'Minnesota Twins':'#002B5C',
            'New York Yankees':'#003087',
            'New York Mets':'#002D72',
            'Oakland Athletics':'#003831',
            'Philadelphia Phillies':'#E81828',
            'Pittsburgh Pirates':'#FDB827',
            'San Diego Padres':'#2F241D',
            'San Francisco Giants':'#FD5A1E',
            'Seattle Mariners':'#0C2C56',
            'St. Louis Cardinals':'#C41E3A',
            'Tampa Bay Rays':'#092C5C',
            'Texas Rangers':'#003278',
            'Toronto Blue Jays':'#134A8E',
            'Washington Nationals':'#AB0003',
        }
    )

    team_pitching_figure.update_xaxes(
        title_font={
        'size': 20,
        'color': 'black'
        },
        tickfont=dict(
            size=16,
            color='black'
        ),
        showgrid=True,
        gridwidth=1,
        gridcolor='black',
        showline=True,
        linewidth=1,
        linecolor='black'
    )

    team_pitching_figure.update_yaxes(
        title_text='Team(s)',
        title_font={
        'size': 20,
        'color': 'black'
        },
        tickfont=dict(
            size=16,
            color='black'
        ),
        showline=True,
        linewidth=1,
        linecolor='black',
        categoryorder='total ascending'
    )

    team_pitching_figure.update_layout(
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

    team_pitching_figure.update_traces(
        textfont_size=14
)
    return team_pitching_figure

