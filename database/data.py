# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 05:56:40 2020

@author: kriz_
"""

import psycopg2
from configparser import ConfigParser
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from app import app
import json
import pathlib
from pathlib import Path

def config(filename="D:\python\database.ini", section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def get_stocks_data(date):
    """ query tickers from the idxstocks table """
    conn = None
    stocks_df = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        sql="SELECT date,stock,prev,close,high,low,foreign_buy,foreign_sell,volume, freq FROM idxstocks WHERE date >= %s::Date"
        stocks_df = pd.read_sql(sql,conn, None, params=[date])
        print("The number of dates: ", len(stocks_df.index.unique()))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return stocks_df

def get_kepemilikan_efek():
    dir_path= 'D:/Gdrive/stockdata/kepemilikanefek/'
    files = [file.name for file in Path(dir_path).rglob('*.txt')]

    efek_df=[]
    for file in files:
        
        efek_df_tmp = pd.read_csv(dir_path+file, sep='|', index_col='Date',parse_dates=[0])
        efek_df_tmp = efek_df_tmp.drop(columns=['Sec. Num','Price'])
        efek_df_tmp =  efek_df_tmp[efek_df_tmp['Type'] == 'EQUITY']
        cols = efek_df_tmp.columns.drop(['Code','Type'])
        efek_df_tmp[cols] = efek_df_tmp[cols].astype('int64')
        efek_df.append(efek_df_tmp)

    return pd.concat(efek_df).sort_index()

@app.callback(Output('intermediate-value', 'children'), [Input('stock-input', 'value')])
def clean_data(value):
    date = "2020-01-01"
    all_stocks_df = get_stocks_data(date)
    efek_df = get_kepemilikan_efek()
    efek_df = efek_df.loc[date:]

    # print(efek_df)
    stock_df = all_stocks_df[all_stocks_df.stock.eq(value.upper())]
    stock_efek_df= efek_df[efek_df.Code.eq(value.upper())]

    stock_df['nbsa'] = stock_df.foreign_buy-stock_df.foreign_sell
    stock_df['fn_vol'] = (stock_df.foreign_buy+stock_df.foreign_sell)/2
    stock_df['nbsa_val'] =  -1*stock_df['nbsa']*(stock_df['close']+stock_df['high']+stock_df['low'])/3
    nbsa_cumsum=stock_df.nbsa.cumsum()
    nbsa_cumsum = nbsa_cumsum-min(nbsa_cumsum)
    nbsa_val_cumsum=stock_df.nbsa_val.cumsum()
    
    datasets={
        'stock_df' : stock_df.to_json(orient='split'),
        'nbsa_cumsum' : nbsa_cumsum.to_json(orient='split'),
        'nbsa_val_cumsum' : nbsa_val_cumsum.to_json(orient='split'),
        'stock_efek_df' : stock_efek_df.to_json(orient='split')
    }
    # print(datasets)
    return json.dumps(datasets)
     
