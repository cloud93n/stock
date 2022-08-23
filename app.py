# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 05:56:40 2020

@author: kriz_
"""


import dash
import dash_bootstrap_components as dbc
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True