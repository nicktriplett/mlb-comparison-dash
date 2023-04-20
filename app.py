
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from pybaseball import batting_stats, pitching_stats


# Instantiating the Dashboard
dashboard = Dash(__name__,external_stylesheets=[dbc.themes.SANDSTONE],use_pages=True)
server=dashboard.server
dashboard.title = 'Project 6 Dashboard'

# The Dashboard Layout
dashboard.layout = dbc.Container(
    children=[
        # Page Navigation
        dbc.NavbarSimple(
            brand='2022 MLB Season Dashboard',
            children=[
                dbc.NavItem(dbc.NavLink('Home',href='/')),
                dbc.NavItem(dbc.NavLink('Batting Data Chart',href='/batting')),
                dbc.NavItem(dbc.NavLink('Pitching Data Chart',href='/pitching')),
                dbc.NavItem(dbc.NavLink('Team Batting Data Chart',href='/team-batting')),
                dbc.NavItem(dbc.NavLink('Team Pitching Data Chart',href='/team-pitching')),
            ],
            color='primary',
            dark=True,
        ),

        # Page Content
        dash.page_container,
    ],
    fluid=True,
    class_name='px-0'
)


# run the app
if __name__ == '__main__':
    dashboard.run_server(debug=True)
