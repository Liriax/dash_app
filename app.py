# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import gunicorn
from dash.dependencies import Input, Output, State, ALL
# import the classes
import calculator
from layout import *
from util import *
# style the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = MainPanel

@app.callback(
    Output('table_absolute','children'),
    Output('table_relative','children'),
    Output('table_conditions','children'),
    Input('editing-rows-button','n_clicks'),
    State('table_absolute','children'),
    State('table_relative','children'),
    State('table_conditions','children')
)
def poduct_family_tables_output(n_clicks,table_absolute,table_relative,table_conditions):
    new_row_absolute=html.Tr([html.Td([n_clicks+1])]+[html.Td([dcc.Input(id={'type':comp_id,'index':n_clicks},type='text',value=10,step=0.1,style={'width':'70%'})]) for name,comp_id in absolute])
    new_row_relative=html.Tr([html.Td([n_clicks+1])]+[html.Td([dcc.Input(id={'type':comp_id,'index':n_clicks},type='text',value=10,step=0.1,style={'width':'70%'})]) for comp_id, name in relative])
    new_row_cond=html.Tr([html.Td([n_clicks+1])]+[html.Td([dcc.Input(id={'type':comp_id,'index':n_clicks},type='number',value=10,step=0.1,style={'width':'70%'})]) for  name, comp_id in cond if comp_id!='t_DLZ']+[
        html.Td([dcc.Input(id={'type':comp_id,'index':n_clicks},type='text',value=10,step=0.1,style={'width':'70%'})]) for  name, comp_id in cond if comp_id=='t_DLZ'
    ])
    table_absolute.append(new_row_absolute)
    table_relative.append(new_row_relative)
    table_conditions.append(new_row_cond)
    return table_absolute, table_relative, table_conditions

@app.callback(
    Output('table_invest_l3','children'),
    Input('new-invest-button-l3','n_clicks'),
    State('table_invest_l3','children'),
)
def table_invest_l3_output(n_clicks_l3,children_l3):
    new_row_l3 = html.Tr([html.Td(colSpan=2,children=[n_clicks_l3+1]),
        html.Td([dcc.Input(
            id={'type':'I_l3','index':n_clicks_l3},
            type='number',
            value=1000,
            step=0.01
        )]),
        html.Td([dcc.Input(
            id={'type':'c_main_l3','index':n_clicks_l3},
            type='number',
            value=20,
            step=0.01
        )])])
    children_l3.append(new_row_l3)
    return children_l3
@app.callback(
    Output('table_invest_l2','children'),
    Input('new-invest-button-l2','n_clicks'),
    State('table_invest_l2','children'),
)
def table_invest_output(n_clicks_l2,children_l2):
    new_row_l2 = html.Tr([
        html.Td(colSpan=2,children=[n_clicks_l2+1]),
        html.Td([dcc.Input(
            id={'type':'I_l2','index':n_clicks_l2},
            type='number',
            value=1000,
            step=0.01
        )]),
        html.Td([dcc.Input(
            id={'type':'c_main_l2','index':n_clicks_l2},
            type='number',
            value=20,
            step=0.01
        )])
    ])
    children_l2.append(new_row_l2)
   
    return children_l2

@app.callback(
    Output('table_same_prod','children'),
    Input('new-method-button-3','n_clicks'),
    State('table_same_prod','children')
)
def table_same_prod_output(n_clicks,children):
    new_row = html.Tr([
        html.Td(colSpan=2,children=[n_clicks+1]),
        html.Td([dcc.Input(
            id={'type':'I_x_3','index':n_clicks},
            type='number',
            value=1000,
            step=0.01
        )]),
        html.Td([dcc.Input(
            id={'type':'c_main_3','index':n_clicks},
            type='number',
            value=20,
            step=0.01
        )])
    ])
    children.append(new_row)
    return children
@app.callback(
    Output('table_similar_prod','children'),
    Input('new-method-button', 'n_clicks'),
    State('table_similar_prod','children')
)
def table_similar_prod_output (n_clicks, children):
    new_row = html.Tr([
        html.Td([n_clicks+1]),
        html.Td([dcc.Input(
            id={'type':'I_x','index':n_clicks},
            type='number',
            value=1000,
            step=0.01
        )]),
        html.Td([dcc.Input(
            id={'type':'n_KäA','index':n_clicks},
            type='number',
            value=10,
            step=1
        )]),
        html.Td([dcc.Input(
            id={'type':'c_main','index':n_clicks},
            type='number',
            value=20,
            step=0.01
        )])
    ])
    children.append(new_row)
    return children

# this switches the visibility of input fields for absolute and relative time
@app.callback(
    Output(component_id='div_datatable_relative', component_property='style'),
    Output(component_id='div_datatable_absolute', component_property='style'),
    [Input(component_id='dropdown-to-switch-between-absolute-and-relative-time', component_property='value')]
)
def switch_time_input_variant(visibility_state):
    if visibility_state == 'relative':
        return {'display': 'table-row'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'table-row'}

@app.callback(
    Output('figure_output', 'figure'),
    Output('results_output', 'children'),
    Output('R2_KW','children'),
    # Output('R3_KW','children'),
    Output('IiA_KäA_KW','children'),
    # Output('KäA_KW','children'),
    Output('I_pr', 'children'),
    Output('I_al','children'),
    Output('I_l2', 'children'),
    Output('I_l3','children'),
    Input("saveTable1Input", 'n_clicks'),
    Input('show-kw-button','n_clicks'),
    Input('resultSort', 'value'),
    Input("figure_output", "clickData"),
    Input({'type':'I_x','index':ALL},'value'),
    Input({'type':'n_KäA','index':ALL},'value'),
    Input({'type':'c_main','index':ALL},'value'),
    Input({'type':'I_x_3','index':ALL},'value'),
    Input({'type':'c_main_3','index':ALL},'value'),
    Input({'type':'I_l2','index':ALL},'value'),    
    Input({'type':'c_main_l2','index':ALL},'value'),
    Input({'type':'I_l3','index':ALL},'value'),
    Input({'type':'c_main_l3','index':ALL},'value'),
    State('matLevel', 'value'),
    State('supFunction', 'value'),
    [State({'type':comp_id,'index':ALL},'value') for name,comp_id in absolute],
    [State({'type':comp_id,'index':ALL},'value') for comp_id,name in relative],
    [State({'type':comp_id,'index':ALL},'value') for name,comp_id in cond],
    State('dropdown-to-switch-between-absolute-and-relative-time','value'),
    State('AS', 'value'),
    State('K_PGrund', 'value'),
    State('c_int', 'value'),
    State('t', 'value'),
)
# This function generates the output
def generateOutput(n_clicks1,n_clicks2, resultSort, clickData,
                    I_x_values, n_KäA_values, c_main_values,
                    I_x_values_3, c_main_values_3,
                    I_l2_values, c_main_l2_values,
                    I_l3_values, c_main_l3_values,
                   matLevel, supFunction, 
                   timeSameComponent,timeSimComponent,timeNewComponent,timeProcess,timeResource,
                   totalSearchTimeComponents,shareSameComponent,shareSimComponent,shareNewComponent,totalSearchTimeProcesses,totalSearchTimeResources,
                    mean_amount_of_elem_comp,t_DLZ,P_x,npvRevProProduct,l_Mx,
                   typeOfTimeMeasurement,
                   AS, K_PGrund, c_int, t,):

    

    n_prodFam=len(timeSameComponent)
    # fist save the user input parameters
    allgemeine_parameter = {
        "Arbeitsstunden pro Woche":AS,
        "Monatliches Grundgehalt in der Arbeitsvorbereitung":K_PGrund,
        "Zinssatz":c_int,
        "Betrachtungszeitraum":t
    }
    product_family_conditions = pd.DataFrame(list(zip(mean_amount_of_elem_comp,t_DLZ,P_x,npvRevProProduct,l_Mx)), columns=[name for comp_id,name in cond])
    product_family_absolute = pd.DataFrame(list(zip(timeSameComponent,timeSimComponent,timeNewComponent,timeProcess,timeResource)), columns=[name for comp_id,name in absolute])
    product_family_relative = pd.DataFrame(list(zip(totalSearchTimeComponents,shareSameComponent,shareSimComponent,shareNewComponent,totalSearchTimeProcesses,totalSearchTimeResources)), columns=[name for name,comp_id in relative])

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
    similar_prod_info_methods = pd.DataFrame(list(zip(I_x_values,n_KäA_values,c_main_values)), columns=["I_x","n_KäA","c_main"])
    same_prod_info_methods = pd.DataFrame(list(zip(I_x_values_3,c_main_values_3)), columns=["I_x","c_main"])
    l2_invest_methods = pd.DataFrame(list(zip(I_l2_values,c_main_l2_values)), columns=["I_l2","c_main"])
    l3_invest_methods = pd.DataFrame(list(zip(I_l3_values,c_main_l3_values)), columns=["I_l3","c_main"])
    IiA = 1 if "IiA" in supFunction else 0
    KäA = 1 if "KäA" in supFunction else 0
    ist_situation = {
        "matLevel":matLevel,
        "IiA":IiA,
        "KäA":KäA,
    }
    investition = {
        "I_l2":l2_invest_methods,
        "I_l3":l3_invest_methods,
        "I_identisch":same_prod_info_methods,
        "I_ähnlich":similar_prod_info_methods,
    }
    parameters = {
        "ist_situation":ist_situation,
        "investition":investition,
        "allgemeine_parameter":allgemeine_parameter,
        "product_family_parameter":product_family_conditions,
        "product_family_time":product_family_time
    }
    data = {'matLevel': matLevel, 'IiA': IiA, 'KäA': KäA,
            'typeOfTimeMeasurement': typeOfTimeMeasurement}
    ist_situation = pd.DataFrame([data])
    sit = Situation(parameters)
    # KW_l2=sit.KW_l2_tables
    KW_l3=sit.KW_l3_tables
    KW_IiA=sit.KW_IiA_tables
    KW_KäA=sit.KW_KäA_tables
    best_method_l2 = "bereits umgesetzt"
    best_method_l3 = "bereits umgesetzt"
    # if matLevel<2:
    #     best_method_l2 = KW_l2[0].name
    #     KW_l2 = [x.table for x in KW_l2]
        
    if matLevel<3:
        best_method_l3 = KW_l3[0].name
        KW_l3 = [x.table for x in KW_l3]

    if IiA ==0:
        I_al=KW_IiA[0].investition
        best_method_3 = KW_IiA[0].name
        KW_IiA=[x.table for x in KW_IiA]
    else:
        I_al = same_prod_info_methods.iloc[0]['I_x']
        best_method_3 = "bereits umgesetzt"
    if KäA ==0:
        I_pr = KW_KäA[0].investition
        best_method = KW_KäA[0].name
        best_method_num = [int(s) for s in best_method.split() if s.isdigit()][0]
        n_KäA = similar_prod_info_methods.iloc[best_method_num-1]['n_KäA']
        KW_KäA=[x.table for x in KW_KäA]
    else:
        I_pr = similar_prod_info_methods.iloc[0]['I_x']
        best_method = "bereits umgesetzt"
        n_KäA = similar_prod_info_methods.iloc[0]['n_KäA']

    KW_IiA_KäA = [sit.best_solution.table]+sit.recommend1 if (IiA==0 or KäA==0) else "bereits umgesetzt"
    best_level_return = [sit.best_level.table]+sit.recommend2 if matLevel<3 else "bereits umgesetzt"
    I_l2=sit.I_l2
    I_l3=sit.I_l3
    c_main_same=sit.c_main_same
    c_main_sim=sit.c_main_sim
    c_main_l2=sit.c_main_l2
    c_main_l3=sit.c_main_l3
    data2 = {'I_al': I_al, 'I_pr': I_pr, 'I_l2': I_l2, 'I_l3': I_l3,
                'AS': AS, 'K_PGrund': K_PGrund, 'c_main_l2': c_main_l2, 'c_main_l3':c_main_l3,"c_main_same":c_main_same, "c_main_sim":c_main_sim, 'c_int': c_int,
                't': t, 'n_KäA':n_KäA}
    invest_params = pd.DataFrame([data2])

    # now read the csv files and generate graphs and output tables
    res = pd.DataFrame(data=None,columns=["npv","comparison","investition","t_unsupported","improved_time","matLevel","prodFeat","treeMatchAlgo","alreadyImplemented","amount_of_product_features"])
    returns = [px.bar(res, x='comparison', y='npv', labels={'comparison': "", 'npv': ""}), 
            html.H6(
            style={"color": "red"},
            children=["Bitte Parameter eingeben und aktualisieren."]), 
            None,None,None,None,None,None]

    if n_clicks2>0:
        returns[2:]=[best_level_return,KW_IiA_KäA, f"Optimal: {best_method}", f"Optimal: {best_method_3}", f"Optimal: {best_method_l2}", f"Optimal: {best_method_l3}"]
    if n_clicks1 is not None :
        c = calculator.Calculator(ist_situation,invest_params,product_family_conditions,product_family_absolute,product_family_relative)
        res = c.calculate_results()
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
            g = px.bar(df, x='name', y='npv', labels={'name': "", 'npv': "Kapitalwert"}, color='npv')


        elif resultSort == "timeSaving":
            df = sorted_by_time
            name.insert(len(df), "Ist-Situation")

            g = px.bar(df, x='name', y='t_supported',
                       labels={'name': "", 't_supported': "Zeit nachher"}, color='t_supported')


        else:
            df = sorted_by_matLevel
            name.insert(0, "Ist-Situation")
            g = px.bar(df, x='name', y='matLevel', labels={'name': "", 'matLevel': "Reifegradstufe"},
                       color="matLevel")

        results_output = [html_table(df.iloc[x]["name"],df.iloc[x]["npv"], df.iloc[x]['investition'], df.iloc[x]['t_supported'], 
                                     df.iloc[x]['t_unsupported'], df.iloc[x]["IiA"], df.iloc[x]["KäA"], 
                                     df.iloc[x]["matLevel"],n_prodFam,df.iloc[x]["t_supported_x"],df.iloc[x]["t_unsupported_x"]).table for x in range(0, len(df))]
        try:
            n = clickData.get('points')[0].get('pointIndex')
            results_output.insert(0, results_output.pop(n))
        except:
            print("graph not rendered yet")

        results_output[0].style = {"width": "100%", "background-color": "#e6e6e6"}
        results_output.insert(0, html.P(style={"text-align": "center", "font-size": "small"}, children=[
            "Mit dem Clicken auf die Säule können Sie eine Option zum Anzeigen auswählen."]))

        returns[0]=g
        returns[1]=results_output

    return returns


# run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)
