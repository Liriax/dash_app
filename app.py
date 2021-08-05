# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import gunicorn
from dash.dependencies import Input, Output, State
from ast import literal_eval

# import the classes
import calculator

# style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

params = [("Neuer Bauteile/Baugruppen", "timeNewComponent"),("Ähnlicher Bauteile/Baugruppen", "timeSimComponent"), ("Gleicher Bauteile/Baugruppen", "timeSameComponent"),("Prozessinformation","timeProcess"),("Ressource-Information", "timeResource")]
params_dict = [('totalSearchTimeComponents','Gesamte benötigte Zeit zum Suchen von Bauteilen (Minuten)'),
                                ('shareNewComponent', 'Prozentualer Anteil von Suchen neuer BT/BG'),
                                ('shareSimComponent',  'Prozentualer Anteil von Suchen ähnlicher BT/BG'),
                                ( 'shareSameComponent','Prozentualer Anteil von Suchen gleicher BT/BG'),
                                ('totalSearchTimeProcesses',  'Gesamte benötigte Zeit zum Suchen von Prozessen (Minuten)'),
                                ('totalSearchTimeResources',  'Gesamte benötigte Zeit zum Suchen von Resourcen (Minuten)')]
                                

cond = [("Anzahl manueller Eingaben pro Bauteil (z.B. Produktmerkmale)","n_SaB"),("Durschnittliche Anzahl an unbekannten Bauteilen","mean_amount_of_elem_comp"),
        ("Gesamte Durchlaufzeit des Produkts (Stunden)","t_DLZ"),
        ("Einnahmen pro Produktvariante","npvRevProProduct"),
        ("Anzahl an eingeführten Produktvarianten pro Jahr","P_x"),
        ("zeitgleich nutzbaren Montagelinien mit DAS", "l_Mx")]

headerStyle={
            'backgroundColor': 'white',
            'font-size': '15px'}

style_cell={
        'font-family':'Open Sans',
        'whiteSpace': 'normal',
        'height': 'auto',
        'font-size': '15px'
    }

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
                                                 {'label': 'Reifegrad 3', 'value': 3},
                                             ]
                                         )
                                     ])
                                 ]
                             ),
                             # row 2
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Bestehende Unterstützungen", html.Br(), "(Eine Analyse der Struktur ist nur notwendig, wenn die Erzeugnisstruktur mehr als 2 Ebenen enthält. Ansonsten ist eine Analyse der Mengenstückliste ausreichend)"]),
                                     html.Td(children=[
                                         dcc.Checklist(
                                             id='supFunction',
                                             options=[
                                                 {'label': 'Strukturanalyse unter Berücksichtigung gleicher Bauteile (SgB)', 'value': 'SgB'},
                                                 {'label': 'Strukturanalyse unter Berücksichtigung ähnlicher Bauteile (SäB)', 'value': 'SaB'}
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

                     html.Br(),
                     # Suchzeiten mit absoluten Werten
                     html.Div(
                         children=[
                            dash_table.DataTable(
                                id='datatable_absolute',
                                columns=(
                                    [{'id': 'prodFam', 'name': 'Produktfamilie'}] +
                                    [{'id': p[1], 'name': p[0]} for p in params]
                                ),
                                data=[
                                    dict(prodFam=i, **{param[1]: 10 for param in params})
                                    for i in range(1, 2)
                                ],
                                style_header=headerStyle,
                                style_cell = style_cell,
                                editable=True,
                                row_deletable=True
                            ),

                        ],
                     id="div_datatable_absolute"

                    ),
                     

                     # Suchzeiten mit Prozentualen Anteilen

                    html.Div(
                        children=[
                     dash_table.DataTable(
                        id='datatable_relative',
                        columns=([{'id': 'prodFam2', 'name': 'Produktfamilie'}] +
                                    [{'id': p[0], 'name': p[1]} for p in params_dict]
                        ),
                        data=[
                             dict(prodFam2=i, **{param[0]: 0 for param in params_dict})
                                    for i in range(1, 2)
                        ],
                        editable=True,
                        row_deletable=True,
                        style_header=headerStyle,
                        style_cell = style_cell,
                     ),
                     ],
                        id='div_datatable_relative'
                    ),
                    html.Button('Neue Produktfamilie', id='editing-rows-button', n_clicks=0),

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
                                     html.Td(children=["38,5 Stunden"])  # calculate standard cost
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
                                     html.Td(children=["0,5%, wird aber meist zur Berechnung höher angesetzt (~12%)"])  # standard interest
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Betrachtungszeitraum"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='t',
                                             type='number', min=1, value=3
                                         )
                                     ]),
                                     html.Td(children=["5"])  # standard duration
                                 ]
                             ),
                             html.Br()
                         ]
                     ),
                     html.Div(
                         
                                children=[
                                    html.P("Nebenbedingungen je Produkt/Produktfamilie", style={"font-weight": "bold"}),
                                    dash_table.DataTable(
                                        id='datatable_conditions',
                                        columns=(
                                            [{'id': 'prodFam3', 'name': 'Produktfamilie'}] +
                                            [{'id': p[1], 'name': p[0]} for p in cond]
                                        ),
                                        data=[
                                            dict(prodFam3=i, **{param[1]: 10 for param in cond})
                                            for i in range(1, 2)
                                        ],
                                        editable=True,
                                        row_deletable=True,
                                        style_header=headerStyle,
                                        style_cell = style_cell,
                                    ),

                                ],
                            id="div_datatable_conditions"

                    ),

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
                             {'label': 'Nach Kapitalwert sortieren', 'value': 'money'},
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
    ]
)

@app.callback(
    Output('datatable_absolute', 'data'),
    Output('datatable_relative', 'data'),
    Output('datatable_conditions', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('datatable_absolute', 'data'),
    State('datatable_absolute', 'columns'),
    State('datatable_relative', 'data'),
    State('datatable_relative', 'columns'),
    State('datatable_conditions', 'data'),
    State('datatable_conditions', 'columns'))
def add_row(n_clicks, rows1, columns1,rows2, columns2, rows3, columns3):
    if n_clicks > 0:
        rows1.append({c['id']: len(rows1)+1 if c['id']=='prodFam' else 10 for c in columns1})
        rows2.append({c['id']: len(rows2)+1 if c['id']=='prodFam2' else 0 for c in columns2})
        rows3.append({c['id']: len(rows3)+1 if c['id']=='prodFam3' else 10 for c in columns3})
    return rows1, rows2, rows3
    

# this switches the visibility of input fields for absolute and relative time
@app.callback(
    Output(component_id='div_datatable_relative', component_property='style'),
    Output(component_id='div_datatable_absolute', component_property='style'),
    [Input(component_id='dropdown-to-switch-between-absolute-and-relative-time', component_property='value')]
)
def switch_time_input_variant(visibility_state):
    if visibility_state == 'relative':
        return {'display': 'table', "width": "100%"}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'table'}

@app.callback(
    Output('figure_output', 'figure'),
    Output('results_output', 'children'),
    Input("saveTable1Input", 'n_clicks'),
    Input('resultSort', 'value'),
    Input("figure_output", "clickData"),
    State('matLevel', 'value'),
    State('supFunction', 'value'),
    State('datatable_absolute','data'),
    State('datatable_absolute','columns'),
    State('datatable_relative','data'),
    State('datatable_relative','columns'),
    State('datatable_conditions','data'),
    State('datatable_conditions','columns'),
   
    State('dropdown-to-switch-between-absolute-and-relative-time','value'),
  

    State('I_al', 'value'),
    State('I_pr', 'value'),
    State('I_l2', 'value'),
    State('I_l3', 'value'),
    State('AS', 'value'),
    State('K_PGrund', 'value'),
    State('c_main', 'value'),
    State('c_int', 'value'),
    State('t', 'value'),
)
# This function generates the output
def generateOutput(n_clicks1, resultSort, clickData,
                   matLevel, supFunction, 
                   rows, columns, rows2, columns2, rows3, columns3,
                   typeOfTimeMeasurement,
                   I_al, I_pr, I_l2, I_l3, AS, K_PGrund, c_main, c_int, t,
                    ):
    # fist save the user input parameters
    if n_clicks1 is not None :
        df = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        df.to_csv(r"assets/product_family_absolute.csv", index=False)
        df = pd.DataFrame(rows2, columns=[c['id'] for c in columns2])
        df.to_csv(r"assets/product_family_relative.csv", index=False)
        df = pd.DataFrame(rows3, columns=[c['id'] for c in columns3])
        df.to_csv(r"assets/product_family_conditions.csv", index=False)

        SgB = 1 if "SgB" in supFunction else 0
        SaB = 1 if "SaB" in supFunction else 0
        data = {'matLevel': matLevel, 'SgB': SgB, 'SaB': SaB,
                'typeOfTimeMeasurement': typeOfTimeMeasurement}
        df = pd.DataFrame([data])
        df.to_csv(r'assets/ist_situation.csv', index=False)
        data2 = {'I_al': I_al, 'I_pr': I_pr, 'I_l2': I_l2, 'I_l3': I_l3,
                 'AS': AS, 'K_PGrund': K_PGrund, 'c_main': c_main, 'c_int': c_int,
                 't': t}
        df2 = pd.DataFrame([data2])
        df2.to_csv(r'assets/parameter_Investitionsrechnung.csv', index=False)

    # now read the csv files and generate graphs and output tables
    res = pd.read_csv(r'assets/default_result.csv')
    if n_clicks1 is not None :
        c = calculator.Calculator()
        c.calculate_results()
        res = pd.read_csv(r'assets/result.csv')
        name = ["Option {}".format(x) for x in range(1, len(res))]

        # sort dataframes
        sorted_by_npv = res.sort_values(by=["npv"], ascending=False)
        sorted_by_time = res.sort_values(by=['t_supported'], ascending=True)
        sorted_by_matLevel = res.sort_values(by=['matLevel'], ascending=True)

        if resultSort == "money":
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

        results_output = [html_table(df.iloc[x]["name"],df.iloc[x]["npv"], df.iloc[x]['investition'], df.iloc[x]['t_supported'], 
                                     df.iloc[x]['t_unsupported'], df.iloc[x]["SgB"], df.iloc[x]["SaB"], 
                                     df.iloc[x]["matLevel"],len(rows),df.iloc[x]["t_supported_x"],df.iloc[x]["t_unsupported_x"]).table for x in range(0, len(df))]
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
    def __init__(self, name, money, investition, time, time_before, SgB, SaB, matLevel, n_prodFam, time_x, time_before_x):
        support_functions = []
        if SgB == 1:
            support_functions.append("SgB")
        if SaB == 1:
            support_functions.append("SäB")
        support_functions = str(support_functions).strip("[]'").replace("'", "")
        time_x = literal_eval(time_x)
        time_before_x = literal_eval(time_before_x)
        self.table = html.Table(style={"width": "100%"},
                                children=[
                                    html.Tr(
                                        children=[
                                            html.Th(colSpan=4, style={'text-align': 'left'},
                                                    children=[name])]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Kapitalwert: "]),
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
                                ]+[
                                    html.Tr(
                                        [
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[time_before_x[n]]),
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[time_x[n]])
                                        ]
                                    ) for n in range(0,n_prodFam)
                                ]+[
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
    app.run_server(debug=True, dev_tools_hot_reload=False)
