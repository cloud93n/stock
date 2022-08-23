import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 



layout = html.Div(
    [html.H1('Stocks Analysis',style={'textAlign':'center'}),
     dbc.Row(
         [
             dbc.Col(
                 html.Div(
                     [
                        html.H2('Filters'),
                        dbc.Form([
                            dbc.FormGroup(
                                [
                                    dbc.Input(
                                        id="stock-input", value='TLKM',
                                        type="text",debounce =True, 
                                        style={'textTransform':'uppercase'}
                                    ),
                            
                                    dbc.Label("Graph"),
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Line", "value": 1},
                                            {"label": "Candlestick", "value": 2},
                                            {"label": "nbsa val", "value": 3},
                                        ],
                                        value=[2],
                                        id="switches-input",
                                        switch=True,
                                    ),
                                ]
                            )  
                        ])                              
                     ],
                     style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':15, 'marginRight':15}
                 ),
               
                 width=2),
             dbc.Col(
                 html.Div(
                     [
                         dcc.Tabs(id="tabs", value='tab-2',
                                  children=[
                                        dcc.Tab(label='Data Table', value='tab-1'),
                                        dcc.Tab(label='Graph', value='tab-2'),
                                        ]
                        ),
                        html.Div(id='tabs-content')
                    ]
                ), 
                width=10)
         ]
     ),
     dcc.Store(id='session', storage_type='session'),
     # Hidden div inside the app that stores the intermediate value
     html.Div(id='intermediate-value', style={'display': 'none'})
     ]
)