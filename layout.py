import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from util import *

MainPanel=html.Div(
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
                                     html.Td(colSpan=2, children=["Aktuelle Reifegradstufe (RF)"]),
                                     html.Td(children=[
                                         dcc.Dropdown(
                                             id='matLevel',
                                             options=[
                                                 {'label': 'Reifegradstufe 1', 'value': 1},
                                                 {'label': 'Reifegradstufe 2', 'value': 2},
                                                 {'label': 'Reifegradstufe 3', 'value': 3},
                                             ],
                                             value = 1
                                         )
                                     ])
                                 ]
                             ),
                             # row 2
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Bestehende Unterstützungen", html.Br(), "(Wenn die Erzeugnisstruktur mehr als 2 Ebenen enthält, muss die Unterstützung die Erzeugnisstruktur berücksichtigen)"]),
                                     html.Td(children=[
                                         dcc.Checklist(
                                             id='supFunction',
                                             options=[
                                                 {'label': 'Identifizierung identischer Produktinformationen (IiP)', 'value': 'SgB'},
                                                 {'label': 'Klassifizierung ähnlicher Produktinformationen (KäP)', 'value': 'SaB'}
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
                                             {'label': 'Absolute Zeitangaben (Min)', 'value': 'absolute'},
                                             {'label': 'Relative Zeitangaben (Min)', 'value': 'relative'}
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
                             html.Tr(
                                 html.Td(colSpan=4,
                                 children=[
                                    html.P("Nebenbedingungen je Produktfamilie", style={"font-weight": "bold"}),
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

                                    ],id="div_datatable_conditions"

                                 ),
                                
                                    

                            ),
                             # Investition Dropdown
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition"]),
                                     html.Th(children=["Summe"])
                                 ]
                             ),
                             # if maturity level = 1:
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für Reifegradstufe 2"]),
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
                                     html.Td(colSpan=2, children=["Investition für Reifegradstufe 3"]),
                                     html.Td(colSpan=2, children=[
                                         dcc.Input(
                                             id='I_l3',
                                             type='number', min=0, value=1000
                                         )
                                     ])
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=2, children=["Investition für die Identifizierung identischer Produktinformationen"]),
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
                                     html.Td(colSpan=2, children=["Investition für die Klassifizierung ähnlicher Produktinformationen"]),
                                     html.Td(colSpan=2,
                                         children=[
                                             html.Button('Neue Methode', id='new-method-button', n_clicks=0),
                                         ]
                                     )
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=4,children=[
                                         dash_table.DataTable(
                                        id='datatable_similar_prod',
                                        columns=(
                                            [{'id': 'simProd', 'name': 'Methode zur Klassifizierung'}] +
                                            [{'id': p[1], 'name': p[0], 'type': 'numeric'} for p in simProd]
                                        ),
                                        data=[
                                            {'simProd':1,"I_x":1000,"n_SaB":10}
                                        ],
                                        editable=True,
                                        row_deletable=True,
                                        style_header=headerStyle,
                                        style_cell = style_cell,
                                    ),
                                    
                                     ]),
                                    
                                 ]
                             ),
                             html.Tr([html.Td(colSpan=4,children=[html.P(id='I_pr')],style={'text-align':'right','color':'#cf7f0e'})]),
                            html.Br(),

                             # weitere Parameter header
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Allgemeine Parameter"]),
                                     html.Th(children=["Standards in DE"])

                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Arbeitsstunden pro Woche"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='AS',
                                             type='number', min=0, value=38.5, step = 0.1
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
                                             type='number', min=0, value=3200, step = 0.01
                                         )
                                     ]),
                                     html.Td(children=["3200€"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Instandhaltungskostensatz"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_main',
                                             type='number', min=0, value=20, step = 0.1
                                         )
                                     ]),
                                     html.Td(children=["20-30%"])  # calculate standard cost
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Zinssatz"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='c_int',
                                             type='number', min=0, value=12, step=0.1
                                         )
                                     ]),
                                     html.Td(children=["0,5%, wird aber meist zur Berechnung höher angesetzt"])  # standard interest
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(children=["Betrachtungszeitraum"]),
                                     html.Td(children=[
                                         dcc.Input(
                                             id='t',
                                             type='number', min=1, value=5
                                         )
                                     ]),
                                     html.Td(children=["5 Jahre"])  # standard duration
                                 ]
                             ),
                             html.Br()
                         ]
                     ),
                     

                 ]),


        # ------------------Output Division------------------------------------------------------
        html.Div(className='col2',
                 style={'margin-left': '3vw', 'margin-top': '3vw'},
                 children=[
                     html.Header("Ergebnis", style={'text-align': 'center', "font-weight": "bold"}),
                     html.Br(),
                     html.P("--------Erhöhung auf Reifegrad 2--------",style={ "font-weight": "bold","text-align":"center"}),
                     dbc.Row(
                         [
                         dbc.Col([html.Div(id='R2_KW')])]
                     ),
                     html.Br(),
                     html.P("--------Erhöhung auf Reifegrad 3--------",style={ "font-weight": "bold","text-align":"center"}),
                     dbc.Row(
                         [
                         dbc.Col([html.Div(id='R3_KW')])]
                     ),
                     html.Br(),
                     html.P("--------Identifizierung identischer Produktinformationen--------",style={ "font-weight": "bold","text-align":"center"}),
                     dbc.Row(
                         [
                         dbc.Col([html.Div(id='IiP_KW')])]
                     ),
                     html.Br(),
                     html.P("--------Klassifizierung ähnlicher Produktinformationen--------",style={ "font-weight": "bold","text-align":"center"}),
                     dbc.Row(
                         [
                         dbc.Col([html.Div(id='KäP_KW')])]
                     ),
                     html.Br(),
                     html.P("--------Identifizierung neuer Produktinformationen--------",style={ "font-weight": "bold","text-align":"center"}),
                     html.Div(id="checklist-new-prod-info"),
                     html.Br(),
                     html.P("alle Lösungen",style={ "font-weight": "bold"}),
                     dcc.Dropdown(
                         id='resultSort',
                         options=[
                             {'label': 'Nach Kapitalwert sortieren', 'value': 'money'},
                             {'label': 'Nach Reifegradstufe sortieren', 'value': 'matLevel'},
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