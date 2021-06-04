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
                                     html.Td(colSpan=2, children=["Aktueller Reifegrad (RF)"]),
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
                                                 {'label': 'Strukturanalyse unter Berücksichtigung gleicher Bauteile (SgB)', 'value': 'treeMatching'},
                                                 {'label': 'Strukturanalyse unter Berücksichtigung ähnlicher Bauteile (SäB)', 'value': 'prodFeature'}
                                             ],
                                             value=[]

                                         )
                                     ]),
                                     html.Td(children=[
                                         html.Button(id='saveTable1Input', n_clicks=None, children="Aktualisieren")
                                     ])
                                 ]
                             ),
                             html.Br(),

                             html.Br(),
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
                                     html.Th(colSpan=2, children=["Suchzeiten zum Identifizieren"]),
                                     html.Th(colSpan=2, children=["Dauer (Minuten)"])
                                 ]
                             ),

                             # Bauteile 1
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2,children=["Neuer Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeNewComponent",
                                             type="number", min=0, value=10
                                         )
                                     ])
                                 ]

                             ),
                             # Bauteile 2
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2,children=["Ähnlicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSimComponent",
                                             type="number", min=0, value=5
                                         )
                                     ])
                                 ]
                             ),
                             # Bauteile 3
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2,children=["Gleicher Bauteile/Baugruppen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeSameComponent",
                                             type="number", min=0, value=15
                                         )
                                     ])
                                 ]

                             ),

                             html.Br(),

                             # Prozess 1
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2,children=["Prozessinformation"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeProcess",
                                             type="number", min=0, value=10
                                         )
                                     ])
                                 ]
                             ),

                             html.Br(),

                             # ressource 1
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2,children=["Ressource-Information"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="timeResource",
                                             type="number", min=0, value=10
                                         )
                                     ])
                                 ]
                             )

                         ], style={'display': 'table'}, id='tableAbsoluteTimes',
                     ),

                     # Suchzeiten mit Prozentualen Anteilen
                     html.Table(
                         children=[
                             html.Br(),
                             html.Tr(children=[
                                 html.Th(children=["Gesamte benötigte Zeit zum Suchen von Bauteilen (Minuten)"]),
                                 html.Td(children=[
                                     dcc.Input(
                                         id="totalSearchTimeComponents",
                                         type="number", min=0, value=5
                                     )
                                 ])]
                             ),

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

                             html.Tr(children=[
                                 html.Th(children=[
                                     "Gesamte benötigte Zeit zum Suchen von Prozessen (Minuten)"]),
                                 html.Td(children=[
                                     dcc.Input(
                                         id="totalSearchTimeProcesses",
                                         type="number", min=0, value=5
                                     )
                                 ])]
                             ),


                             html.Br(),

                             html.Tr(children=[
                                 html.Th(children=[
                                     "Gesamte benötigte Zeit zum Suchen von Resourcen (Minuten)"]),
                                 html.Td(children=[
                                     dcc.Input(
                                         id="totalSearchTimeResources",
                                         type="number", min=0, value=5
                                     )
                                 ])]
                             ),

                         ], id='tableRelativeTimes'
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
                                     html.Td(colSpan=2, children=["Investition für Strukturanalyse unter Berücksichtigung gleicher Bauteile"]),
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
                                     html.Td(colSpan=2, children=["Investition für Strukturanalyse unter Berücksichtigung ähnlicher Bauteile"]),
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
                            html.Br(),

                             # weitere Parameter header
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Weitere Parameter"]),
                                     html.Th(children=["Standard DE"])

                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Arbeitsstunden pro Woche"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='AS',
                                             type='number', min=0, value=30
                                         )
                                     ]),
                                     html.Td(children=["35-40 Stunden"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Monatliches Grundgehalt in der Arbeitsvorbereitung"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='K_PGrund',
                                             type='number', min=0, value=1000
                                         )
                                     ]),
                                     html.Td(children=["3200€"])  # calculate standard cost
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
                                     html.Td(children=["20-30%"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Zinssatz, %"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_int',
                                             type='number', min=0, value=6
                                         )
                                     ]),
                                     html.Td(children=["maximal 6%"])  # standard interest
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
                                     html.Td(children=["3 bzw. 5 für ERP-System"])  # standard duration
                                 ]
                             ),
                             html.Tr(
                                 children=[

                                     html.Td(children=["Anzahl manueller Eingaben pro Bauteil (z.B. Produktmerkmale)"]),

                                     html.Td(children=[
                                         dcc.Input(
                                             id='n_prodFeat',
                                             type='number', min=0, value=9
                                         )
                                     ]),
                                     html.Td(children=["9"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Durschnittliche Anzahl an elementaren Bauteilen"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='mean_amount_of_elem_comp',
                                             type='number', min=0, value=9
                                         )
                                     ]),
                                     html.Td(children=["9"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Produktsdurchlaufzeit in der Montage (Stunden)"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='t_DLZ',
                                             type='number', min=0, value=5
                                         )
                                     ]),
                                     html.Td(children=["5"]) 
                                 ]
                             ),
                             # Number of new variants
                             html.Tr(
                                 children=[
                                     html.Td(children=["Anzahl neue Varianten pro Jahr"], id='numNewVariantLabel',
                                             style={'display': 'none'}),
                                     html.Td(children=[
                                         dcc.Input(
                                             id="numNewVariant",
                                             type="number", min=0, value=5, style={'display': 'none'}
                                         )
                                     ]),

                                 ]
                             ),
                             html.Br(),
                             html.Tr(id="npvChainOutput",
                                     children=[
                                         html.Td(children=["Einnahmen pro Produktvariante"], id='npvRevProProductLabel',
                                                 style={'display': 'none'}),
                                         html.Td(children=[
                                             dcc.Input(id='npvRevProProduct', type='number', min=0, value=500,
                                                       style={'display': 'none'})]),
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
        return {'display': 'table', "width": "100%"}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'table'}


@app.callback(
    Output(component_id='npvRevProProduct', component_property='style'),
    Output(component_id='npvRevProProductLabel', component_property='style'),
    Output(component_id='numNewVariant', component_property='style'),
    Output(component_id='numNewVariantLabel', component_property='style'),
    [Input(component_id='calMethod', component_property='value')]
)
def switch_npv_rev_pro_product_visibility(calc_method):
    if calc_method == 'npv':
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}
    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


@app.callback(
    Output('figure_output', 'figure'),
    Output('results_output', 'children'),
    Input("saveTable1Input", 'n_clicks'),
    Input("saveTable2Input", 'n_clicks'),
    Input('resultSort', 'value'),
    Input('calMethod', 'value'),
    Input("figure_output", "clickData"),
    State('matLevel', 'value'),
    State('supFunction', 'value'),
    State('timeNewComponent', 'value'),
    State('timeSimComponent', 'value'),
    State('timeSameComponent', 'value'),
    State('timeProcess', 'value'), 
    State('timeResource', 'value'),
    State('numNewVariant', 'value'),
    State('totalSearchTimeComponents', 'value'),
    State('totalSearchTimeProcesses', 'value'),
    State('totalSearchTimeResources', 'value'),
    State('dropdown-to-switch-between-absolute-and-relative-time', 'value'),
    State('shareNewComponent', 'value'),
    State('shareSimComponent', 'value'),
    State('shareSameComponent', 'value'),
    
    State('n_prodFeat', 'value'),
    State('mean_amount_of_elem_comp', 'value'),
    State('I_al', 'value'),
    State('I_pr', 'value'),
    State('I_l2', 'value'),
    State('I_l3', 'value'),
    State('AS', 'value'),
    State('K_PGrund', 'value'),
    State('c_main', 'value'),
    State('c_int', 'value'),
    State('t', 'value'),
    State('npvRevProProduct', 'value'),
    State('t_DLZ', 'value')
)
# This function generates the output
def generateOutput(n_clicks1, n_clicks2, resultSort, calMethod, clickData,
                   matLevel, supFunction,
                   timeNewComponent, timeSimComponent, timeSameComponent,
                   timeProcess,
                   timeResource,
                   numNewVariant,
                   totalSearchTimeComponents, totalSearchTimeProcesses, totalSearchTimeResources,
                   typeOfTimeMeasurement,
                   shareNewComponent, shareSimComponent, shareSameComponent,
                   n_prodFeat, mean_amount_of_elem_comp, I_al,
                   I_pr, I_l2, I_l3, AS, K_PGrund, c_main, c_int, t, npvRevProProduct, t_DLZ):
    # fist save the user input parameters
    if n_clicks1 is not None or n_clicks2 is not None:
        treeMatchAlgo = 1 if "treeMatching" in supFunction else 0
        prodFeat = 1 if "prodFeature" in supFunction else 0
        data = {'matLevel': matLevel, 'treeMatchAlgo': treeMatchAlgo, 'prodFeat': prodFeat,
                'timeNewComponent': timeNewComponent, 'timeSimComponent': timeSimComponent,
                'timeSameComponent': timeSameComponent,
                'timeProcess': timeProcess, 
                'timeResource': timeResource,
                'numNewVariant': numNewVariant,
                'totalSearchTimeComponents': totalSearchTimeComponents,
                'totalSearchTimeProcesses': totalSearchTimeProcesses,
                'totalSearchTimeResources': totalSearchTimeResources,
                'typeOfTimeMeasurement': typeOfTimeMeasurement,
                'shareNewComponent': shareNewComponent / 100, 'shareSimComponent': shareSimComponent / 100,
                'shareSameComponent': shareSameComponent / 100,
                'n_prodFeat': n_prodFeat, 'mean_amount_of_elem_comp': mean_amount_of_elem_comp}
        df = pd.DataFrame([data])
        df.to_csv('ist_situation.csv', index=False)
        data2 = {'I_al': I_al, 'I_pr': I_pr, 'I_l2': I_l2, 'I_l3': I_l3,
                 'AS': AS, 'K_PGrund': K_PGrund, 'c_main': c_main, 'c_int': c_int,
                 't': t,
                 'npvRevProProduct': npvRevProProduct, 't_DLZ':t_DLZ}
        df2 = pd.DataFrame([data2])
        df2.to_csv('parameter_Investitionsrechnung.csv', index=False)

    # now read the csv files and generate graphs and output tables
    res = pd.read_csv('default_result.csv')
    if n_clicks1 is not None or n_clicks2 is not None:
        c = calculator.Calculator()
        c.calculate_results()
        res = pd.read_csv('result.csv')
        name = ["Option {}".format(x) for x in range(1, len(res))]

        # sort dataframes
        sorted_by_npv = res.sort_values(by=["npv"], ascending=False)
        sorted_by_cost = res.sort_values(by=["comparison"], ascending=True)
        sorted_by_time = res.sort_values(by=['t_supported'], ascending=True)
        sorted_by_matLevel = res.sort_values(by=['matLevel'], ascending=True)

        ifCost = True

        if resultSort == "money":
            if calMethod == "comparison":
                ifCost = True
                df = sorted_by_cost
                name.insert(0, "Ist-Situation")
                # df['name'] = name
                g = px.bar(df, x='name', y='comparison', labels={'name': "", 'comparison': "Kosten"},
                           color="comparison")
            else:
                ifCost = False
                df = sorted_by_npv
                if df.iloc[1]['npv'] <= 0:
                    name.insert(0, "Ist-Situation")
                else:
                    name.insert(len(df), "Ist-Situation")
                # df['name'] = name
                g = px.bar(df, x='name', y='npv', labels={'name': "", 'npv': "Kapitalwert"}, color='npv')


        elif resultSort == "timeSaving":
            df = sorted_by_time
            name.insert(len(df), "Ist-Situation")
            # df['name'] = name

            g = px.bar(df, x='name', y='t_supported',
                       labels={'name': "", 't_supported': "Zeit nachher"}, color='t_supported')


        else:
            df = sorted_by_matLevel
            name.insert(0, "Ist-Situation")
            # df['name'] = name
            g = px.bar(df, x='name', y='matLevel', labels={'name': "", 'matLevel': "Reifegrad"},
                       color="matLevel")

        results_output = [html_table(df.iloc[x]["name"], df.iloc[x][calMethod], \
                                     df.iloc[x]['investition'], df.iloc[x]['t_supported'], \
                                     df.iloc[x]['t_unsupported'], df.iloc[x]["treeMatchAlgo"], df.iloc[x]["prodFeat"],
                                     df.iloc[x]["matLevel"], ifCost).table for x in range(0, len(df))]
        try:
            n = clickData.get('points')[0].get('pointIndex')
            results_output.insert(0, results_output.pop(n))
        except:
            print("graph not rendered yet")

        results_output[0].style = {"width": "100%", "background-color": "#e6e6e6"}
        results_output.insert(0, html.P(style={"text-align": "center", "font-size": "small"}, children=[
            "Mit dem Clicken auf die Säule können Sie eine Option zum Anzeigen auswählen."]))

        return g, results_output

    else:
        return px.bar(res, x='comparison', y='npv', labels={'comparison': "", 'npv': ""}), html.H6(
            style={"color": "red"},
            children=["Bitte Parameter eingeben."])


# this class is for the output tables: each option is a html_table object
class html_table:
    def __init__(self, name, money, investition, time, time_before, treeMatchAlgo, prodFeat, matLevel, ifCost):
        support_functions = []
        if treeMatchAlgo == 1:
            support_functions.append("SgB")
        if prodFeat == 1:
            support_functions.append("SäB")
        support_functions = str(support_functions).strip("[]'").replace("'", "")

        self.table = html.Table(style={"width": "100%"},
                                children=[
                                    html.Tr(
                                        children=[
                                            html.Th(colSpan=4, style={'text-align': 'left'},
                                                    children=[name])]
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
                                            html.Td(children=["Suchzeit vorher: "]),
                                            html.Td(children=[str(time_before)]),
                                            html.Td(children=["Suchzeit nachher: "]),
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

                                    html.Br()
                                ])


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)
