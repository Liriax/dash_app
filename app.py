# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import gunicorn
from dash.dependencies import Input, Output
# import the classes
from test_class import person

# style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H2('Dash: A web application framework for Python.'),
    html.P('Heroku: Diese Web-App wird auf Heroku deployed.'),
    html.Br(),
    html.Div(className='row',
             children=[
                 html.Div(className='four columns div-user-input1',
                          children=[        
                                        # input table
                                        html.Table(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Th(children=["header1"]),
                                                        html.Th(children=["header2"])
                                                    ]
                                                ),
                                                # row 1
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["name"]),
                                                        html.Td(children=[
                                                            dcc.Input(id='text-input1',
                                                            placeholder='input some text here',
                                                            type='text'
                                                            )
                                                        ])
                                                    ]
                                                ),
                                                # row 2
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["city"]),
                                                        html.Td(children=[
                                                            dcc.Input(id='text-input2',
                                                            placeholder='input some text here',
                                                            type='text'
                                                            )
                                                        ])
                                                    ]
                                                ),
                                                # row 3
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["age"]),
                                                        html.Td(children=[
                                                            dcc.Dropdown(
                                                                id='dropdown-input1',
                                                                options=[
                                                                    {'label': 'twenty', 'value': 20},
                                                                    {'label': 'thirty', 'value': 30}
                                                                    ],
                                                                value = 20
                                                                )
                                                        ])
                                                    ]
                                                )
                                            ]  
                                        ),
                                
                            ]
                    ),
                 html.Div(className='four columns div-user-input2',
                          children=[
                              html.Table(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Th(children=["header1"]),
                                                        html.Th(children=["header2"])
                                                    ]
                                                ),
                                                # row 1
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["table row 1"]),
                                                        html.Td(children=[
                                                            dcc.Input(id='text-input3',
                                                            placeholder='input some text here',
                                                            type='text'
                                                            )
                                                        ])
                                                    ]
                                                ),
                                                # row 2
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["table row 2"]),
                                                        html.Td(children=[
                                                            dcc.Input(id='text-input4',
                                                            placeholder='input some text here',
                                                            type='text'
                                                            )
                                                        ])
                                                    ]
                                                ),
                                                # row 3
                                                html.Tr(
                                                    children=[
                                         
                                                        html.Td(colSpan=2,
                                                        children=[
                                                             dcc.Graph(
                                                                    id='example-graph',
                                                                    figure=fig
                                                                )
                                                        ])
                                                    ]
                                                )
                                            ]  
                                        ),
                             
                          ]
                    ),
                html.Div(className='four columns div-user-input3',
                          children=[
                              html.Table(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Th(children=["Output type"]),
                                                        html.Th(children=["Output value"])
                                                    ]
                                                ),
                                                # row 1
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["name"]),
                                                        html.Td(children=[
                                                            html.Div(id='text-output1')
                                
                                                        ])
                                                    ]
                                                ),
                                                # row 2
                                                html.Tr(
                                                    children=[
                                                        html.Td(children=["city"]),
                                                        html.Td(children=[
                                                            html.Div(id='text-output2')
                                                            ])
                                                    ]
                                                ),
                                                # row 3
                                                html.Tr(
                                                    children=[
                                         
                                                        html.Td(children=["age"]),
                                                        html.Td(children=[
                                                            html.Div(id='dropdown-output1')
                                                            ])
                                                    ]
                                                )
                                            ]  
                                        )
                          ]
                    )
             ])
    
])

# Define all Outputs first! Otherwise error
# The order of the inputs is NOT the order of writing here, but the order of appearance in app.layout
@app.callback(
    Output(component_id='dropdown-output1', component_property='children'),
    Output(component_id='text-output1', component_property='children'),
    Output('text-output2','children'),
    Input(component_id='dropdown-input1', component_property='value'),
    Input('text-input2','value'),
    Input(component_id='text-input1', component_property='value'),

)
def update_output_div(age, name, city):
    p = person(age, name, city)
    return 'I will be {} years old in 10 years'.format(p.add_to_age(10)), 'I am {}'.format(p.name), 'I live in {}'.format(p.city)

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)