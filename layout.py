import dash_table
import dash_core_components as dcc
import dash_html_components as html
from util import *
import dash_bootstrap_components as dbc


left_side = html.Div(className='col1', style={'margin-left': '1vw', 'margin-top': '3vw'},

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
                                     ])
                                     
                                 ]
                             ),
                            html.P("Zeitangaben je Produktfamilie", style={"font-weight": "bold"}),

                             html.Tr(
                                 children=[
                                     html.Td([dcc.Dropdown(
                                         id='dropdown-to-switch-between-absolute-and-relative-time',
                                         options=[
                                             {'label': 'Absolute Zeitangaben (Min)', 'value': 'absolute'},
                                             {'label': 'Relative Zeitangaben (Min)', 'value': 'relative'}
                                         ],
                                         value='absolute',
                                     )],colSpan=2),
                                   html.Td(children=[ html.Button('Neue Produktfamilie', id='editing-rows-button', n_clicks=0)]),
                                 ]
                             ),
                             # Suchzeiten mit absoluten Werten
                                html.Tr(
                                    children=[
                                        html.Td(colSpan=3,children=[
                                         html.Table(id='table_absolute',children=[
                                             html.Tr([html.Td(["Produktfamilie"])]+[
                                                 html.Td([name]) for name, id in absolute
                                             ]),
                                         ])                                    
                                     ]),
                                    ],
                                id="div_datatable_absolute"

                                ),
                                # Suchzeiten mit Prozentualen Anteilen

                                html.Tr(
                                    children=[
                                        html.Td(colSpan=3,children=[
                                         html.Table(id='table_relative',children=[
                                             html.Tr([html.Td(["Produktfamilie"])]+[
                                                 html.Td([name]) for id, name in relative
                                             ]),
                                         ])                                    
                                     ]),
                                    ],
                                    id='div_datatable_relative'
                                ),
                                html.P("Nebenbedingungen je Produktfamilie", style={"font-weight": "bold"}),
                                html.Tr(
                                 html.Td(colSpan=3,
                                 children=[
                                    html.Td(colSpan=3,children=[
                                         html.Table(id='table_conditions',children=[
                                             html.Tr([html.Td(["Produktfamilie"])]+[
                                                 html.Td([name]) for name,comp_id in cond
                                             ]),
                                         ])                                    
                                     ]),
                                    ],id="div_datatable_conditions"

                                 ),
                                ),
                    

                         ],

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
                             # if maturity level = 1:
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition für Reifegradstufe 2"]),
                                     html.Td(colSpan=2, children=[
                                         html.Button('Neue Investition', id='new-invest-button-l2', n_clicks=0),
                                         ]
                                     )
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=4,children=[
                                         html.Table(id='table_invest_l2',children=[
                                             html.Tr([
                                                 html.Td(colSpan=2,children=["Investition"]),
                                                 html.Td(["Investitionssumme"]),
                                                 html.Td(["Instandhaltungskostensatz"])
                                             ]),
                                         ], style= {'width':'100%'})                                    
                                     ]),
                                    
                                 ]
                             ),
                             html.Tr([html.Td(colSpan=4,children=[html.P(id='I_l2')],style={'text-align':'right','color':'#cf7f0e'})]),
                            
                             # if maturity level = 2:
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition für Reifegradstufe 3"]),
                                     html.Td(colSpan=2, children=[
                                            html.Button('Neue Investition', id='new-invest-button-l3', n_clicks=0),
                                         ]
                                     )
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=4,children=[
                                         html.Table(id='table_invest_l3',children=[
                                             html.Tr([
                                                 html.Td(colSpan=2,children=["Investition"]),
                                                 html.Td(["Investitionssumme"]),
                                                 html.Td(["Instandhaltungskostensatz"])
                                             ]),
                                         ], style= {'width':'100%'})                                    
                                     ]),
                                    
                                 ]
                             ),
                             html.Tr([html.Td(colSpan=4,children=[html.P(id='I_l3')],style={'text-align':'right','color':'#cf7f0e'})]),
                            
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition für die Identifizierung identischer Produktinformationen"]),
                                     html.Td(
                                         children=[
                                             html.Button('Neue Methode', id='new-method-button-3', n_clicks=0),
                                         ]
                                     )
                                 ]
                             ),
                             html.Tr(
                                 children=[
                                     html.Td(colSpan=4,children=[
                                         html.Table(id='table_same_prod',children=[
                                             html.Tr([
                                                 html.Td(colSpan=2,children=["Methode"]),
                                                 html.Td(["Investitionssumme"]),
                                                 html.Td(["Instandhaltungskostensatz"])
                                             ]),
                                         ], style= {'width':'100%'})                                    
                                     ]),
                                    
                                 ]
                             ),
                             html.Tr([html.Td(colSpan=4,children=[html.P(id='I_al')],style={'text-align':'right','color':'#cf7f0e'})]),
                            
                            
                             html.Tr(
                                 children=[
                                     html.Th(colSpan=2, children=["Investition für die Klassifizierung ähnlicher Produktinformationen"]),
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
                                         html.Table(id='table_similar_prod',children=[
                                             html.Tr([
                                                 html.Td(["Methode zur Klassifizierung"]),
                                                 html.Td(["Investitionssumme"]),
                                                 html.Td(["Anzahl manueller Eingaben pro Bauteil (z.B. Produktmerkmale)"]),
                                                 html.Td(["Instandhaltungskostensatz"])
                                             ]),
                                         ])                                    
                                     ]),
                                    
                                 ]
                             ),
                             html.Tr([html.Td(colSpan=4,children=[html.P(id='I_pr')],style={'text-align':'right','color':'#cf7f0e'})]),
                            

                             # weitere Parameter hea
                             # der
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
                            
                         ]
                     ),
                     html.Br(),
                     html.Button("einzelne Kapitalwerte anzeigen", id='show-kw-button',n_clicks=0,style={'align': 'center', "font-weight": "bold"}),
                            html.P("--------Erhöhung auf Reifegrad 2--------",style={ "font-weight": "bold","text-align":"center"}),
                            html.Div(id='R2_KW'),
                            html.Br(),
                            html.P("--------Erhöhung auf Reifegrad 3--------",style={ "font-weight": "bold","text-align":"center"}),
                            html.Div(id='R3_KW'),
                            html.Br(),
                            html.P("--------Identifizierung identischer Produktinformationen--------",style={ "font-weight": "bold","text-align":"center"}),
                            html.Div(id='IiP_KW'),
                            html.Br(),
                            html.P("--------Klassifizierung ähnlicher Produktinformationen--------",style={ "font-weight": "bold","text-align":"center"}),
                            html.Div(id='KäP_KW'),
                            html.Br(),             

                 ])

right_side =    html.Div(className='col2',
                 style={'margin-left': '3vw', 'margin-top': '3vw'},
                 children=[
                     html.Button(id='saveTable1Input', n_clicks=None, children="Gesmatlösungen Aktualisieren"),
                    
                     html.Header("alle Lösungen", style={'text-align': 'center', "font-weight": "bold"}),
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
  

MainPanel=html.Div(
    style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-gap': '2vw'},
    children=[
        left_side,
        right_side
        # ------------------Output Division------------------------------------------------------
       ]
)