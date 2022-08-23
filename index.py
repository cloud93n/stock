# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 05:56:40 2020

@author: kriz_
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

import psycopg2
from configparser import ConfigParser
from app import app
from layouts import tab1, tab2, sidepanel
from database import data

app.layout = sidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout
   





if __name__ == '__main__':
    app.run_server(debug=True)