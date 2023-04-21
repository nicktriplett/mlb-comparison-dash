
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
        title=' ',
        color='Name (Team)',
        color_discrete_map={
            'Aaron Judge (NYY)':'#003087',
            'Manny Machado (SDP)':'#2F241D',
            'Nolan Arenado (STL)':'#C41E3A',
            'Paul Goldschmidt (STL)':'#C41E3A',
            'Freddie Freeman (LAD)':'#005A9C',
            'Francisco Lindor (NYM)':'#002D72',
            'Yordan Alvarez (HOU)':'#002D62',
            'Jose Altuve (HOU)':'#002D62',
            'Mookie Betts (LAD)':'#005A9C',
            'J.T. Realmuto (PHI)':'#E81828',
            'Dansby Swanson (ATL)':'#13274F',
            'Trea Turner (LAD)':'#005A9C',
            'Jose Ramirez (CLE)':'#00385D',
            'Andres Gimenez (CLE)':'#00385D',
            'Xander Bogaerts (BOS)':'#BD3039',
            'Jeff McNeil (NYM)':'#002D72',
            'Tommy Edman (STL)':'#C41E3A',
            'Austin Riley (ATL)':'#13274F',
            'Alex Bregman (HOU)':'#002D62',
            'Julio Rodriguez (SEA)':'#0C2C56',
            'Brandon Nimmo (NYM)':'#002D72',
            'Sean Murphy (OAK)':'#003831',
            'Rafael Devers (BOS)':'#BD3039',
            'Kyle Tucker (HOU)':'#002D62',
            'Willy Adames (MIL)':'#12284B',
            'Daulton Varsho (ARI)':'#A71930',
            'Bo Bichette (TOR)':'#134A8E',
            'Corey Seager (TEX)':'#003278',
            'Carlos Correa (MIN)':'#002B5C',
            'Steven Kwan (CLE)':'#00385D',
            'George Springer (TOR)':'#134A8E',
            'Marcus Semien (TEX)':'#003278',
            'Christian Walker (ARI)':'#A71930',
            'Eugenio Suarez (SEA)':'#0C2C56',
            'Matt Chapman (TOR)':'#134A8E',
            'Jake Cronenworth (SDP)':'#2F241D',
            'Pete Alonso (NYM)':'#002D72',
            'Nico Hoerner (CHC)':'#0E3386',
            'Taylor Ward (LAA)':'#BA0021',
            'Jose Abreu (CHW)':'#27251F',
            'Will Smith (LAD)':'#005A9C',
            'Shohei Ohtani (LAA)':'#BA0021',
            'Juan Soto (- - -)':'#ffffff',
            'Yandy Diaz (TBR)':'#092C5C',
            'Alejandro Kirk (TOR)':'#134A8E',
            'Adolis Garcia (TEX)':'#003278',
            'Ha-seong Kim (SDP)':'#2F241D',
            'Ian Happ (CHC)':'#0E3386',
            'Cedric Mullins II (BAL)':'#DF4601',
            'Elvis Andrus (- - -)':'#ffffff',
            'Jeremy Pena (HOU)':'#002D62',
            'Luis Arraez (MIN)':'#002B5C',
            'Matt Olson (ATL)':'#13274F',
            'Nathaniel Lowe (TEX)':'#003278',
            'Starling Marte (NYM)':'#002D72',
            'Brandon Drury (- - -)':'#ffffff',
            'Ryan McMahon (COL)':'#333366',
            'DJ LeMahieu (NYY)':'#003087',
            "Ke'Bryan Hayes (PIT)":'#FDB827',
            'Vladimir Guerrero Jr. (TOR)':'#134A8E',
            'Bryan Reynolds (PIT)':'#FDB827',
            'Randy Arozarena (TBR)':'#092C5C',
            'Andrew Benintendi (- - -)':'#ffffff',
            'Mark Canha (NYM)':'#002D72',
            'Gleyber Torres (NYY)':'#003087',
            'Jorge Mateo (BAL)':'#DF4601',
            'Josh Rojas (ARI)':'#A71930',
            'Thairo Estrada (SFG)':'#FD5A1E',
            'Kyle Schwarber (PHI)':'#E81828',
            'Teoscar Hernandez (TOR)':'#134A8E',
            'Hunter Renfroe (MIL)':'#12284B',
            'Anthony Santander (BAL)':'#DF4601',
            'Jurickson Profar (SDP)':'#2F241D',
            'Anthony Rizzo (NYY)':'#003087',
            'Justin Turner (LAD)':'#005A9C',
            'Ty France (SEA)':'#0C2C56',
            'Gio Urshela (MIN)':'#002B5C',
            'Amed Rosario (CLE)':'#00385D',
            'Max Muncy (LAD)':'#005A9C',
            'Eduardo Escobar (NYM)':'#002D72',
            'Bobby Witt Jr. (KCR)':'#004687',
            'Rhys Hoskins (PHI)':'#E81828',
            'Christian Yelich (MIL)':'#12284B',
            'Ronald Acuna Jr. (ATL)':'#13274F',
            'Mike Yastrzemski (SFG)':'#FD5A1E',
            'Trent Grisham (SDP)':'#2F241D',
            'J.P. Crawford (SEA)':'#0C2C56',
            'Javier Baez (DET)':'#0C2340',
            'Josh Bell (- - -)':'#ffffff',
            'Myles Straw (CLE)':'#00385D',
            'Seth Brown (OAK)':'#003831',
            'Cody Bellinger (LAD)':'#005A9C',
            'Brendan Rodgers (COL)':'#333366',
            'Ryan Mountcastle (BAL)':'#DF4601',
            'Luis Rengifo (LAA)':'#BA0021',
            'Josh Donaldson (NYY)':'#003087',
            'Austin Hays (BAL)':'#DF4601',
            'Alec Bohm (PHI)':'#E81828',
            'Whit Merrifield (- - -)':'#ffffff',
            'Tony Kemp (OAK)':'#003831',
            'Jonathan Schoop (DET)':'#0C2340',
            'Ketel Marte (ARI)':'#A71930',
            'Wilmer Flores (SFG)':'#FD5A1E',
            'Kyle Farmer (CIN)':'#C6011F',
            'Isiah Kiner-Falefa (NYY)':'#003087',
            'C.J. Cron (COL)':'#333366',
            'Alex Verdugo (BOS)':'#BD3039',
            'Miguel Rojas (MIA)':'#000000',
            'Lane Thomas (WSN)':'#AB0003',
            'Adam Frazier (SEA)':'#0C2C56',
            'J.D. Martinez (BOS)':'#BD3039',
            'Patrick Wisdom (CHC)':'#0E3386',
            'Carlos Santana (- - -)':'#ffffff',
            'Trey Mancini (- - -)':'#ffffff',
            'Rowdy Tellez (MIL)':'#12284B',
            'Tommy Pham (- - -)':'#ffffff',
            'Jesse Winker (SEA)':'#0C2C56',
            'A.J. Pollock (CHW)':'#27251F',
            'Cesar Hernandez (WSN)':'#AB0003',
            'Andrew McCutchen (MIL)':'#12284B',
            'Luke Voit (- - -)':'#ffffff',
            'Charlie Blackmon (COL)':'#333366',
            'Randal Grichuk (COL)':'#333366',
            'MJ Melendez (KCR)':'#004687',
            'Jesus Aguilar (- - -)':'#ffffff',
            'Andrew Vaughn (CHW)':'#27251F',
            'Marcell Ozuna (ATL)':'#13274F',
            'Nick Castellanos (PHI)':'#E81828',
            'Nelson Cruz (WSN)':'#AB0003',
            'Yuli Gurriel (HOU)':'#002D62'
        }
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
        marker_line_color='black',
        marker_line_width=0.5,
        textfont_size=14
)
    return batting_figure
