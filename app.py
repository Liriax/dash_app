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
# import the classes
import calculator
from layout import *

# style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = MainPanel

@app.callback(
    Output('datatable_similar_prod','data'),
    Input('new-method-button', 'n_clicks'),
    Input('datatable_similar_prod','data'),
)
def add_new_method(n_clicks,methods):
    if n_clicks>0:
        methods.append({'simProd':len(methods)+1, 'I_x':1000,'n_SaB':10})
    return methods

@app.callback(
    Output('datatable_absolute', 'data'),
    Output('datatable_relative', 'data'),
    Output('datatable_conditions', 'data'),
    
    Input('editing-rows-button','n_clicks'),
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
    Output('R2_KW','children'),
    Output('R3_KW','children'),
    Output('IiP_KW','children'),
    Output('KäP_KW','children'),
    Output('I_pr', 'children'),
    Output("checklist-new-prod-info",'children'),
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
    State('datatable_similar_prod','data'),
    State('datatable_similar_prod','columns'),
    State('dropdown-to-switch-between-absolute-and-relative-time','value'),
    State('I_al', 'value'),
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
                   rows, columns, rows2, columns2, rows3, columns3, rows4, columns4,
                   typeOfTimeMeasurement,
                   I_al, I_l2, I_l3, 
                   AS, K_PGrund, c_main, c_int, t,
                    ):
    # fist save the user input parameters
    if n_clicks1 is not None :
        allgemeine_parameter = {
            "Arbeitsstunden pro Woche":AS,
            "Monatliches Grundgehalt in der Arbeitsvorbereitung":K_PGrund,
            "Instandhaltungskostensatz": c_main,
            "Zinssatz":c_int,
            "Betrachtungszeitraum":t
        }
        product_family_conditions = pd.DataFrame(rows3, columns=[c['id'] for c in columns3])
        product_family_conditions.to_csv(r"assets/product_family_conditions.csv", index=False)

        product_family_absolute = pd.DataFrame(rows, columns=[c['id'] for c in columns])
        product_family_absolute.to_csv(r"assets/product_family_absolute.csv", index=False)
        product_family_relative = pd.DataFrame(rows2, columns=[c['id'] for c in columns2])
        product_family_relative.to_csv(r"assets/product_family_relative.csv", index=False)

        if typeOfTimeMeasurement == 'absolute':
            product_families = product_family_absolute
            cumTimeNewComponent = list(product_families['timeNewComponent'])
            cumTimeSimComponent =  list(product_families['timeSimComponent'])
            cumTimeSameComponent = list(product_families['timeSameComponent'])
            cumtimeProcess =       list(product_families['timeProcess'])
            cumtimeResource =      list(product_families['timeResource'])

        elif typeOfTimeMeasurement == 'relative':
            product_families = product_family_relative
            totalSearchTimeComponents =list(product_families["totalSearchTimeComponents"])
            totalSearchTimeProcesses = list(product_families["totalSearchTimeProcesses"])
            totalSearchTimeResources = list(product_families["totalSearchTimeResources"])
            shareNewComponent =        list(product_families["shareNewComponent"])
            shareSimComponent =        list(product_families["shareSimComponent"])
            shareSameComponent =       list(product_families["shareSameComponent"])

            cumTimeNewComponent = [shareNewComponent[x] * totalSearchTimeComponents[x] for x in range(0, len(product_family_conditions))]
            cumTimeSimComponent = [shareSimComponent[x] * totalSearchTimeComponents[x]  for x in range(0, len(product_family_conditions))]
            cumTimeSameComponent = [shareSameComponent[x] * totalSearchTimeComponents[x] for x in range(0, len(product_family_conditions))]
            cumtimeProcess = totalSearchTimeProcesses
            cumtimeResource = totalSearchTimeResources

        product_family_time = {
            "cumTimeNewComponent":cumTimeNewComponent ,
            "cumTimeSimComponent":cumTimeSimComponent,
            "cumTimeSameComponent":cumTimeSameComponent,
            "cumtimeProcess" :cumtimeProcess,
            "cumtimeResource":cumtimeResource
        }
        
        similar_prod_info_methods = pd.DataFrame(rows4, columns=[c['id'] for c in columns4])
        similar_prod_info_methods.to_csv(r"assets/similar_prod_info_methods.csv", index=False)

        SgB = 1 if "SgB" in supFunction else 0
        SaB = 1 if "SaB" in supFunction else 0
        checklist=[]
        if SgB == 1:
            checklist.append(1)
        if SaB == 1:
            checklist.append(2)
        nicht = "nicht " if checklist!=[1,2] else ""
        ist_situation = {
            "matLevel":matLevel,
            "IiP":SgB,
            "KäP":SaB,
        }
        investition = {
            "I_l2":I_l2,
            "I_l3":I_l3,
            "I_identisch":I_al,
            "I_ähnlich":similar_prod_info_methods
        }
        parameters = {
            "ist_situation":ist_situation,
            "investition":investition,
            "allgemeine_parameter":allgemeine_parameter,
            "product_family_parameter":product_family_conditions,
            "product_family_time":product_family_time
        }
        data = {'matLevel': matLevel, 'SgB': SgB, 'SaB': SaB,
                'typeOfTimeMeasurement': typeOfTimeMeasurement}
        df = pd.DataFrame([data])
        df.to_csv(r'assets/ist_situation.csv', index=False)
        KW_l2,KW_l3,KW_IiP,KW_KäP = calculate_separate_npvs(parameters)
        if SaB ==0:
            I_pr = KW_KäP[0].investition
            best_method = KW_KäP[0].name
            best_method_num = [int(s) for s in best_method.split() if s.isdigit()][0]
            n_SaB = similar_prod_info_methods.iloc[best_method_num-1]['n_SaB']
            KW_KäP=[x.table for x in KW_KäP]
        else:
            I_pr = similar_prod_info_methods.iloc[0]['I_x']
            best_method = "bereits umgesetzt"
            n_SaB = similar_prod_info_methods.iloc[0]['n_SaB']


        data2 = {'I_al': I_al, 'I_pr': I_pr, 'I_l2': I_l2, 'I_l3': I_l3,
                 'AS': AS, 'K_PGrund': K_PGrund, 'c_main': c_main, 'c_int': c_int,
                 't': t, 'n_SaB':n_SaB}
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
            g = px.bar(df, x='name', y='matLevel', labels={'name': "", 'matLevel': "Reifegradstufe"},
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

        
        return g, results_output, \
            KW_l2, KW_l3,KW_IiP,KW_KäP, f"Optimal: {best_method}",[dcc.Checklist(
                            options=[
                                {"label": "Identifizierung identischer Produktinformationen (IiP)", "value": 1},
                                {"label": "Klassifizierung ähnlicher Produktinformationen (KäP)", "value": 2},
                            ],
                            value=checklist,
                            id="checklist-new-prod-info",
                        ),html.P(f"Bedingung {nicht}erfüllt")]

    else:
        return px.bar(res, x='comparison', y='npv', labels={'comparison': "", 'npv': ""}), html.H6(
            style={"color": "red"},
            children=["Bitte Parameter eingeben."]), \
            None, None,None,None, None,None



# run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
