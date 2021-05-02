# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import gunicorn
from dash.dependencies import Input, Output, State

# import the classes
import calculator

# style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

opt = 1

app.layout = html.Div(
    style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '2vw'},
    children=[
        html.Div(className='col1', style={'margin-left': '1vw', 'margin-top': '3vw'},

                 children=[
                     # table 1
                     html.Table(
                         children=[
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=3, style={'text-align': 'center'}, children=["Ist-Situation"])
                                 ]
                             ),

                             # row 1
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Aktueller Reifegrad"]),
                                     html.Td(children=[
                                         dcc.Dropdown(
                                             id='matLevel',
                                             options=[
                                                 {'label': 'Reifegrad 1', 'value': 1},
                                                 {'label': 'Reifegrad 2', 'value': 2},
                                                 {'label': 'Reifegrad 3', 'value': 3}
                                             ]
                                         )
                                     ])
                                 ]
                             ),
                             # row 2
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Bestehende Unterstützungen"]),
                                     html.Td(children=[
                                         dcc.Checklist(
                                             id='supFunction',
                                             options=[
                                                 {'label': 'Tree-Matching', 'value': 'treeMatching'},
                                                 {'label': 'Produktmerkmale', 'value': 'prodFeature'}
                                             ],
                                             value=[]

                                         )
                                     ])
                                 ]
                             ),
                             html.Br(),

                             # Number of new variants
                             html.Tr(
                                 children=[
                                     html.Td(children=["Anzahl neue Varianten pro Jahr"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="numNewVariant",
                                             type="number", min=0, value=5
                                         )
                                     ]),
                                     html.Td(children=[
                                         html.Button(id='saveTable1Input', n_clicks=None, children="Speichern")
                                     ])

                                 ]
                             ),

                             html.Tr(
                                 children=[
                                     dcc.Dropdown(
                                         id='dropdown-to-switch-between-absolute-and-relative-time',
                                         options=[
                                             {'label': 'Absolute Zeitangaben', 'value': 'absolute'},
                                             {'label': 'Relative Zeitangaben', 'value': 'relative'}
                                         ],
                                         value='absolute'
                                     ),

                                 ]
                             ),

                             html.Tr(id="dummyOutput1")
                         ],

                     ),
                     # Suchzeiten mit absoluten Werten
                     html.Table(
                         children=[
                             # headers Suchzeiten
                             html.Tr(
                                 children=[
                                     html.Th(children=["Suchzeiten zum Identifizieren"]),
                                     html.Th(children=["Dauer"]),
                                     html.Th(children=["Häufigkeit je Variante"])
                                 ]
                             ),

                             # Bauteile 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neuer Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeNewComponent",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqNewComponent",
                                             type="number", min=1, value=5
                                         )
                                     ])
                                 ]

                             ),
                             # Bauteile 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnlicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSimComponent",
                                             type="number", min=0, value=5
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSimComponent",
                                             type="number", min=1, value=20
                                         )
                                     ])
                                 ]
                             ),
                             # Bauteile 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSameComponent",
                                             type="number", min=0, value=15
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSameComponent",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]

                             ),

                             html.Br(),

                             # Prozess 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neue Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeNewProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqNewProcess",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),
                             # Prozess 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnliche Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSimProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSimProcess",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),
                             # Prozess 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleiche Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSameProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSameProcess",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),

                             html.Br(),

                             # ressource 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neue Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeNewResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqNewResource",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),
                             # ressource 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnliche Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSimResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSimResource",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),
                             # ressource 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleiche Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSameResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="freqSameResource",
                                             type="number", min=1, value=10
                                         )
                                     ])
                                 ]
                             ),
                         ], style={'display': 'block'}, id='tableAbsoluteTimes',
                     ),

                     html.Br(),
                     # Suchzeiten mit Prozentualen Anteilen
                     html.Table(
                         children=[
                             html.Td(children=["Gesamte benötigte Zeit zum Suchen von Bauteilen, Prozessen und Resourcen"]),
                             html.Td(children=[
                                 dcc.Input(
                                     id="totalSearchTime",
                                     type="number", min=0, value=5
                                 )
                             ]),
                             # headers Suchzeiten
                             html.Tr(
                                 children=[
                                     html.Th(children=["Beschreibung der Suchzeit"]),
                                     html.Th(children=["Prozentualer Anteil des gesamten Suchprozesses"]),
                                 ]
                             ),

                             # Bauteile 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neuer Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareNewComponent",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]

                             ),
                             # Bauteile 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnlicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSimComponent",
                                             type="number", min=0, value=5
                                         )
                                     ]),
                                 ]
                             ),
                             # Bauteile 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSameComponent",
                                             type="number", min=0, value=15
                                         )
                                     ]),
                                 ]

                             ),

                             html.Br(),

                             # Prozess 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neue Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareNewProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),
                             # Prozess 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnliche Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSimProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),
                             # Prozess 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleiche Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSameProcess",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),

                             html.Br(),

                             # ressource 1
                             html.Tr(
                                 children=[
                                     html.Td(children=["Neue Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareNewResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),
                             # ressource 2
                             html.Tr(
                                 children=[
                                     html.Td(children=["Ähnliche Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSimResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),
                             # ressource 3
                             html.Tr(
                                 children=[
                                     html.Td(children=["Gleiche Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="shareSameResource",
                                             type="number", min=0, value=10
                                         )
                                     ]),
                                 ]
                             ),
                         ], style={'display': 'block'}, id='tableRelativeTimes',
                     ),
                     html.Br(),
                     # ------table 2-----------------------------------
                     html.Table(
                         children=[
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=3, style={'text-align': 'center'},
                                             children=["Parameter für Investitionsrechnung"])
                                 ]
                             ),
                             # Rechnungsmethode Dropdown
                             html.Tr(
                                 children=[
                                     html.Td(children=["Rechnungsmethode"]),
                                     html.Td(colSpan=2,
                                             children=[
                                                 dcc.Dropdown(
                                                     id='calMethod',
                                                     options=[
                                                         {'label': 'Statische Kostenvergleichsrechnung',
                                                          'value': 'comparison'},
                                                         {
                                                             'label': 'Dynamische Investitionsrechnung mit Kapitalwertmethode',
                                                             'value': 'npv'}
                                                     ],
                                                     value='comparison'
                                                 )
                                             ])
                                 ]
                             ),
                             # Investition Dropdown
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition"]),
                                     html.Th(children=["Summe"])
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für Algorithmus"]),
                                     html.Td(
                                         children=[
                                             dcc.Input(
                                                 id='I_al',
                                                 type='number', min=0, value=1000
                                             )
                                         ]
                                     )
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für Produktmerkmale"]),
                                     html.Td(
                                         children=[
                                             dcc.Input(
                                                 id='I_pr',
                                                 type='number', min=0, value=1000
                                             )
                                         ]
                                     )
                                 ]
                             ),
                             # if maturity level = 1:
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für Reifegrad 2"]),
                                     html.Td(colSpan=2, children=[
                                         dcc.Input(
                                             id='I_l2',
                                             type='number', min=0, value=1000
                                         )
                                     ])
                                 ]
                             ),
                             # if maturity level = 2:
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für Reifegrad 3"]),
                                     html.Td(colSpan=2, children=[
                                         dcc.Input(
                                             id='I_l3',
                                             type='number', min=0, value=1000
                                         )
                                     ])
                                 ]
                             ),
                             # weitere Parameter header
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Weitere Parameter"]),
                                     html.Th(children=["Standard DE"])

                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Personalkostensatz, %"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_person',
                                             type='number', min=0, value=20
                                         )
                                     ]),
                                     html.Td(children=[""])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Instandhaltungskostensatz, %"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_main',
                                             type='number', min=0, value=20
                                         )
                                     ]),
                                     html.Td(children=[""])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Zinssatz, %"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_int',
                                             type='number', min=0, value=7
                                         )
                                     ]),
                                     html.Td(children=[""])  # standard interest
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Nutzungsdauer, Jahren"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='t',
                                             type='number', min=1, value=3
                                         )
                                     ]),
                                     html.Td(children=["3"])  # standard duration
                                 ]
                             ),
                             html.Br(),
                             html.Tr(id="npvChainOutput",
                                     children=[
                                         html.Td(children=["Einnahmen pro Produktvariante"]),
                                         html.Td(children=[
                                             dcc.Input(id='npvRevProProduct', type='number', min=0, value=500)]),
                                         html.Td(html.Button(id="saveTable2Input", n_clicks=None, children="Submit"))
                                     ]
                                     ),

                             html.Tr(id="dummyOutput2")

                         ]
                     )

                 ]),

        #  html.Div(className='col2', style = {'margin-left': '3vw', 'margin-top': '3vw'},
        #     children=[

        #     ]
        #  ),

        # ------------------Output Division------------------------------------------------------
        html.Div(className='col2',
                 style={'margin-left': '3vw', 'margin-top': '3vw'},
                 children=[
                     html.Header("Ergebnis", style={'text-align': 'center', "font-weight": "bold"}),
                     html.Br(),
                     dcc.Dropdown(
                         id='resultSort',
                         options=[
                             {'label': 'Nach Kosten/Kapitalwert sortieren', 'value': 'money'},
                             {'label': 'Nach Reifegrad sortieren', 'value': 'matLevel'},
                             {'label': 'Nach Zeit sortieren', 'value': 'timeSaving'}
                         ],
                         value='money'
                     ),
                     dcc.Graph(id="figure_output"),
                     html.Div(id="dummy_output"),
                     html.Div(id="results_output")

                 ]

                 )

    ])


# this switches the visibility of input fields for absolute and relative time
@app.callback(
    Output(component_id='tableRelativeTimes', component_property='style'),
    Output(component_id='tableAbsoluteTimes', component_property='style'),
    [Input(component_id='dropdown-to-switch-between-absolute-and-relative-time', component_property='value')]
)
def switch_time_input_variant(visibility_state):
    if visibility_state == 'relative':
        return [{'display': 'block'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'block'}]


# Define all Outputs first! Otherwise error
# Be careful with the order!


@app.callback(
    Output('dummyOutput1', 'children'),
    # Output('CostCapOutput','children'),
    # Output('InvSumOutput','children'),
    # Output('timeBeforeOutput','children'),
    # Output('timeAfterOutput','children'),
    Input("saveTable1Input", 'n_clicks'),
    State('matLevel', 'value'),
    State('supFunction', 'value'),
    State('timeNewComponent', 'value'),
    State('freqNewComponent', 'value'),
    State('timeSimComponent', 'value'),
    State('freqSimComponent', 'value'),
    State('timeSameComponent', 'value'),
    State('freqSameComponent', 'value'),
    State('timeNewProcess', 'value'),
    State('freqNewProcess', 'value'),
    State('timeSimProcess', 'value'),
    State('freqSimProcess', 'value'),
    State('timeSameProcess', 'value'),
    State('freqSameProcess', 'value'),
    State('timeNewResource', 'value'),
    State('freqNewResource', 'value'),
    State('timeSimResource', 'value'),
    State('freqSimResource', 'value'),
    State('timeSameResource', 'value'),
    State('freqSameResource', 'value'),
    State('numNewVariant', 'value'),
    State('totalSearchTime', 'value'),
    State('dropdown-to-switch-between-absolute-and-relative-time', 'value'),
    State('shareNewComponent', 'value'),
    State('shareSimComponent', 'value'),
    State('shareSameComponent', 'value'),
    State('shareNewProcess', 'value'),
    State('shareSimProcess', 'value'),
    State('shareSameProcess', 'value'),
    State('shareNewResource', 'value'),
    State('shareSimResource', 'value'),
    State('shareSameResource', 'value'),
)
# This function calculates the total search time and writes the input from Ist-Situation to a csv file
def save_ist_situation(n_clicks, matLevel, supFunction,
                       timeNewComponent, timeSimComponent, timeSameComponent,
                       timeNewProcess, timeSimProcess, timeSameProcess,
                       timeNewResource, timeSimResource, timeSameResource,
                       freqNewComponent, freqSimComponent, freqSameComponent,
                       freqNewProcess, freqSimProcess, freqSameProcess,
                       freqNewResource, freqSimResource, freqSameResource,
                       numNewVariant, totalSearchTime, typeOfTimeMeasurement,
                       shareNewComponent, shareSimComponent, shareSameComponent,
                       shareNewProcess, shareSimProcess, shareSameProcess,
                       shareNewResource, shareSimResource, shareSameResource):
    if n_clicks is not None:
        treeMatchAlgo = 1 if "treeMatching" in supFunction else 0
        prodFeat = 1 if "prodFeature" in supFunction else 0
        data = {'matLevel': matLevel, 'treeMatchAlgo': treeMatchAlgo, 'prodFeat': prodFeat,
                'timeNewComponent': timeNewComponent, 'timeSimComponent': timeSimComponent,
                'timeSameComponent': timeSameComponent,
                'timeNewProcess': timeNewProcess, 'timeSimProcess': timeSimProcess, 'timeSameProcess': timeSameProcess,
                'timeNewResource': timeNewResource, 'timeSimResource': timeSimResource,
                'timeSameResource': timeSameResource,
                'freqNewComponent': freqNewComponent, 'freqSimComponent': freqSimComponent,
                'freqSameComponent': freqSameComponent,
                'freqNewProcess': freqNewProcess, 'freqSimProcess': freqSimProcess, 'freqSameProcess': freqSameProcess,
                'freqNewResource': freqNewResource, 'freqSimResource': freqSimResource,
                'freqSameResource': freqSameResource,
                'numNewVariant': numNewVariant, 'totalSearchTime': totalSearchTime, 'typeOfTimeMeasurement': typeOfTimeMeasurement,
                'shareNewComponent': shareNewComponent, 'shareSimComponent': shareSimComponent, 'shareSameComponent': shareSameComponent,
                'shareNewProcess': shareNewProcess, 'shareSimProcess': shareSimProcess, 'shareSameProcess': shareSameProcess,
                'shareNewResource': shareNewResource, 'shareSimResource': shareSimResource, 'shareSameResource': shareSameResource}
        df = pd.DataFrame([data])
        df.to_csv('ist_situation.csv', index=False)
    return None


@app.callback(
    Output('dummyOutput2', 'children'),
    Input("saveTable2Input", 'n_clicks'),
    State('I_al', 'value'),
    State('I_pr', 'value'),
    State('I_l2', 'value'),
    State('I_l3', 'value'),
    State('c_person', 'value'),
    State('c_main', 'value'),
    State('c_int', 'value'),
    State('t', 'value'),
    State('npvRevProProduct', 'value')
)
# This function writes the input from Parameter für Investitionsrechnung to a csv file
def save_parameter_Investitionsrechnung(n_clicks, I_al, I_pr, I_l2, I_l3, c_person, c_main, c_int, t, npvRevProProduct):
    data = {'I_al': I_al, 'I_pr': I_pr, 'I_l2': I_l2, 'I_l3': I_l3,
            'c_person': c_person, 'c_main': c_main, 'c_int': c_int,
            't': t,
            'npvRevProProduct': npvRevProProduct}
    df = pd.DataFrame([data])
    df.to_csv('parameter_Investitionsrechnung.csv', index=False)
    return None


class html_table:
    def __init__(self, opt, money, investition, time, time_before, treeMatchAlgo, prodFeat, matLevel, ifCost):
        support_functions = []
        if treeMatchAlgo == 1:
            support_functions.append("Tree-Matching")
        if prodFeat == 1:
            support_functions.append("Produktmerkmale*")
        support_functions = str(support_functions).strip("[]'").replace("'", "")

        self.table = html.Table(style={"width": "100%"},
                                children=[
                                    html.Tr(
                                        children=[
                                            html.Th(colSpan=4, style={'text-align': 'left'},
                                                    children=["Option {}".format(opt) if opt > 0 else "Ist-Situation"])]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Kosten: " if ifCost else "Kapitalwert: "]),
                                            html.Td(children=[str(money)]),
                                            html.Td(children=["Investitionssumme: "]),
                                            html.Td(children=[str(investition)])
                                        ]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Durchsatzzeit vorher: "]),
                                            html.Td(children=[str(time_before)]),
                                            html.Td(children=["Durchsatzzeit nachher: "]),
                                            html.Td(children=[str(time)])
                                        ]
                                    ),

                                    # header support function outputs
                                    html.Tr(
                                        children=[
                                            html.Td(children=["Unterstützungen: "]),
                                            html.Td(support_functions),
                                            html.Td(children=["Reifegrad: "]),
                                            html.Td(matLevel)
                                        ]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=[""]),
                                            html.Td(colSpan=3,
                                                    children=["*Bei Produktmermale wird der Standardwert 9 benutzt"],
                                                    style={"font-size": "small"})
                                        ] if prodFeat == 1 else None
                                    ),

                                    html.Br()
                                ])


@app.callback(
    Output('figure_output', 'figure'),
    Output('results_output', 'children'),
    Input("saveTable2Input", 'n_clicks'),
    Input('resultSort', 'value'),
    Input('calMethod', 'value'),
    Input("figure_output", "clickData")
)
def generate_graphs(n_clicks, resultSort, calMethod, clickData):
    res = pd.read_csv('default_result.csv')
    if n_clicks is not None:
        c = calculator.Calculator()
        c.calculate_results()
        res = pd.read_csv('result.csv')
        name = ["Option {}".format(x) for x in range(1, len(res))]
        name.insert(0, "Ist-Situation")

        # sort dataframes
        sorted_by_npv = res.sort_values(by=["npv"], ascending=False)
        sorted_by_cost = res.sort_values(by=["comparison"], ascending=True)
        sorted_by_time = res.sort_values(by=['improved_time'], ascending=True)
        sorted_by_matLevel = res.sort_values(by=['matLevel'], ascending=True)

        best_time = sorted_by_time.iloc[0]['improved_time']

        sorted_by_npv['name'] = name
        sorted_by_time['name'] = name
        sorted_by_cost['name'] = name
        sorted_by_matLevel['name'] = name
        npv_fig = px.bar(sorted_by_npv, x='name', y='npv', labels={'name': "", 'npv': "Kapitalwert"}, color='npv')
        time_fig = px.bar(sorted_by_time, x='name', y='improved_time',
                          labels={'name': "", 'improved_time': "Zeit nachher"}, color='improved_time')
        cost_fig = px.bar(sorted_by_cost, x='name', y='comparison', labels={'name': "", 'comparison': "Kosten"},
                          color="comparison")
        mat_fig = px.bar(sorted_by_matLevel, x='name', y='matLevel', labels={'name': "", 'matLevel': "Reifegrad"},
                         color="matLevel")

        ifCost = True

        if resultSort == "money":
            if calMethod == "comparison":
                ifCost = True
                df = sorted_by_cost
                g = cost_fig
            else:
                ifCost = False
                df = sorted_by_npv
                g = npv_fig

        elif resultSort == "timeSaving":
            df = sorted_by_time
            g = time_fig

        else:
            df = sorted_by_matLevel
            g = mat_fig

        results_output = [html_table(x, df.iloc[x][calMethod], \
                                     df.iloc[x]['investition'], df.iloc[x]['improved_time'], \
                                     df.iloc[x]['t_unsupported'], df.iloc[x]["treeMatchAlgo"], df.iloc[x]["prodFeat"],
                                     df.iloc[x]["matLevel"], ifCost).table for x in range(0, len(df))]
        try:
            n = clickData.get('points')[0].get('pointIndex')
            results_output.insert(0, results_output.pop(n))
        except:
            print("not rendered yet")

        results_output[0].style = {"width": "100%", "background-color": "#baefff"}

        return g, results_output

    else:
        return px.bar(res, x='comparison', y='npv', labels={'comparison': "", 'npv': ""}), html.H6(
            children=["Bitte Parameter eingeben."])


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
