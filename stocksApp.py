import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import flask
import os

# We start a Flask server
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

# Dash then creates the app on the server
app = dash.Dash('app', server=server)

# This is a Python wrapper for generating HTML code.
app.layout = html.Div([
    html.H1('Soul-Selling Capitalism'),  # make a big header at the top
    # dash-core-components automatically generates code for graphs, dropdowns, and
    # other useful elements
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Teesle', 'value': 'TSLA'},
            {'label': 'Apely', 'value': 'AAPL'},
            {'label': 'Cheepotal', 'value': 'CMG'},
            {'label': 'Ten cents', 'value': 'TCEHY'},
            {'label': 'ALABAMA FUN', 'value': 'LDOS'}
        ],
        value='LDOS'  # the default value when you open the app, it gets updated when
                      # you select a new value from the dropdown
    ),
    
    # Graph() takes a dictionary, which we will create with update_graph()
    dcc.Graph(id='my-graph'),
    
    dcc.DatePickerRange(
    id='date-picker-range',
    start_date=dt(2017, 1, 1),
    end_date=dt.now()
    )
    
    ], className="container")

    

# this is a Python decorator. It feeds update_graph() into app.callback().
# It fetches the value from my-dropdown and feeds it into update_graph() as
# selected_dropdown_value.
@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value'), Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')])
def update_graph(selected_dropdown_value, start_date, end_date):
    df = web.DataReader(
        selected_dropdown_value, data_source='google',
        start=start_date, end=end_date)
    
    price_data = {
            'x': df.index,
            'y': df.Close,
            'line': {'width': 3},
            'name': 'price'
        }
    
    half_data = {
            'x': df.index,
            'y': df.Close / 2.0,
            'line': {'width': 3},
            'name': 'half_price'
        }

    # return a dictionary which is fed to my-graph
    return {
        'data': [price_data, half_data],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            },
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Stock Closing Price'},
        }
    }

# starts a webserver when running python app.py
if __name__ == '__main__':
    app.run_server()
