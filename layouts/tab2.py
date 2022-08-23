import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
from app import app
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json

@app.callback(Output('graph-content', 'children'),
 [
    Input('intermediate-value', 'children'),
    Input('switches-input', 'value')
 ])
def update_graph(jsonified_cleaned_data,switches_value):
    if jsonified_cleaned_data is None:
            raise PreventUpdate
    datasets = json.loads(jsonified_cleaned_data)
    #print(jsonified_cleaned_data)
    stock_df = pd.read_json(datasets['stock_df'], orient='split')
    stock_efek_df = pd.read_json(datasets['stock_efek_df'], orient='split')
    # print(stock_efek_df)
    nbsa_cumsum = pd.read_json(datasets['nbsa_cumsum'], orient='split',typ="series")
    nbsa_val_cumsum = pd.read_json(datasets['nbsa_val_cumsum'], orient='split',typ="series")
    # print(nbsa_cumsum)

    figure = create_figure(stock_df,nbsa_cumsum,nbsa_val_cumsum,stock_efek_df,switches_value)
    return figure

def create_figure(stock_df,nbsa_cumsum,nbsa_val_cumsum,stock_efek_df,switches_value):
    fig = make_subplots(rows=6, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.01,
                        row_heights=[0.5,0.1,0.1,0.1,0.1,0.1],
                        specs=[
                              [{"secondary_y": True}],
                              [{"secondary_y": True}],
                              [{"secondary_y": True}],
                              [{"secondary_y": True}],
                              [{"secondary_y": True}],
                              [{"secondary_y": True}]
                              ])
    if 2 in switches_value:
        fig.add_trace(go.Candlestick(x=stock_df.date,
                                    open=stock_df.prev,
                                    high=stock_df.high,
                                    low=stock_df.low,
                                    close=stock_df.close,
                                    increasing_line_color= 'green',
                                    decreasing_line_color= 'red',
                                    name = 'saham'),
                    row=1,
                    col=1)

    if 1 in switches_value:
        fig.add_trace(go.Scatter(x=stock_df.date,
                            y=stock_df.close,
                            marker_color="blue",
                            name = "close",
                            ),
                    row=1,
                    col=1)
    fig.add_trace(go.Scatter(x=stock_df.date,
                              y=nbsa_cumsum,
                              name = 'ff',
                              yaxis='y2',
                              ),
                  row=1,
                  col=1,
                  secondary_y=True
                  )
    if 3 in switches_value:
        fig.add_trace(go.Scatter(x=stock_df.date,
                                y=nbsa_val_cumsum,
                                name = 'ff_val',
                                yaxis='y3'
                                ),
                    row=1,
                    col=1,
                    secondary_y=True,
                    )
    fig.add_trace(go.Bar(x=stock_df.date,
                          y=stock_df.volume-stock_df.fn_vol,
                          marker_color="blue",
                          name = "volume"),
                  row=2,
                  col=1)
    fig.add_trace(go.Bar(x=stock_df.date,
                              y=stock_df.fn_vol,
                              marker_color="green",
                              name = 'fn_vol',
                              ),
                  row=2,
                  col=1,
                  )
    fig.add_trace(go.Scatter(x=stock_df.date,
                          y=abs(stock_df.nbsa)/(stock_df.fn_vol*2),
                          marker_color="purple",
                          name = "A/D strength"),
                  row=3,
                  col=1,
                  secondary_y=True,
                  )
    fig.add_trace(go.Bar(x=stock_df.date,
                          y=stock_df.nbsa,
                          marker_color="orange",
                          name = "fn_net"),
                  row=3,
                  col=1)
    fig.add_trace(go.Bar(x=stock_df.date,
                              y=stock_df.fn_vol/stock_df.volume,
                              name = 'fn_part',
                              marker_color="green",
                              ),
                  row=4,
                  col=1,
                  )
    fig.add_trace(go.Scatter(x=stock_df.date,
                              y=stock_df.freq,
                              name = 'freq',
                              marker_color="red",
                              ),
                  row=4,
                  col=1,
                  secondary_y=True
                  )
    fig.add_trace(go.Bar(x=stock_df.date,
                              y=np.log(stock_df.high)-np.log(stock_df.low),
                              name = 'price spread',
                              marker_color="orange",
                              ),
                  row=5,
                  col=1,
                  )
    fig.add_trace(go.Bar(x=stock_efek_df.index,
                            y=stock_efek_df['Total.1']-stock_efek_df['Foreign ID'],
                            name = "non ind asing"),
                    row=6,
                    col=1)
    fig.add_trace(go.Bar(x=stock_efek_df.index,
                            y=stock_efek_df['Foreign ID'],
                            name = "ind asing"),
                    row=6,
                    col=1)
    fig.add_trace(go.Bar(x=stock_efek_df.index,
                            y=stock_efek_df['Total']-stock_efek_df['Local ID'],
                            # marker_color="blue",
                            name = "non ind lokal"),
                    row=6,
                    col=1)  
    fig.add_trace(go.Bar(x=stock_efek_df.index,
                            y=stock_efek_df['Local ID'],
                            # marker_color="blue",
                            name = "ind lokal"),
                    row=6,
                    col=1)      
                           
    
    fig.update_layout(
        width=1300,
        height=1200,
        hovermode='x',
        dragmode='pan',
        barmode='stack',
        xaxis6=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.05)
        ),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                          label="1m",
                          step="month",
                          stepmode="backward"),
                    dict(count=3,
                          label="3m",
                          step="month",
                          stepmode="backward"),
                    dict(count=6,
                          label="6m",
                          step="month",
                          stepmode="backward"),
                    dict(count=1,
                          label="YTD",
                          step="year",
                          stepmode="todate"),
                    dict(count=1,
                          label="1y",
                          step="year",
                          stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        ),
      
    )
    
    fig.update_yaxes(autorange=True)
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    
    return html.Div([
                    dcc.Graph(
                        id='stocks-graph',
                        figure=fig,
                        config=
                        {'scrollZoom':True,
                        'showAxisDragHandles': True}
                    )
                ])


layout = html.Div(id='graph-content')