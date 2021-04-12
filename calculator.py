import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State


def retrieve_ist_situation():
    try:
        ist_situation = pd.read_csv('ist_situation.csv')
    except pd.errors.EmptyDataError:
        ist_situation = 'could not read ist_situation.csv!'
    return ist_situation


def retrieve_invest_params():
    try:
        invest_params = pd.read_csv('parameter_Investitionsrechnung.csv')
    except pd.errors.EmptyDataError:
        invest_params = 'could not read parameter_Investitionsrechnung.csv'
    return invest_params


def calculate_total_time(alternative, ist_situation):
    new_time = 0
    if(ist_situation.treeMatAlgo == #f):
        new_time = ist_situation.timeNewComponent
    else:
        new_time += 0



class Calculator:
    alternative1 = {"treeMatchAlgo": "false", "prodFeat": "false", "matLevel": "1"}
    alternative2 = {"treeMatchAlgo": "false", "prodFeat": "true", "matLevel": "1"}
    alternative3 = {"treeMatchAlgo": "true", "prodFeat": "false", "matLevel": "1"}
    alternative4 = {"treeMatchAlgo": "true", "prodFeat": "true", "matLevel": "1"}
    alternative5 = {"treeMatchAlgo": "false", "prodFeat": "false", "matLevel": "2"}
    alternative6 = {"treeMatchAlgo": "false", "prodFeat": "true", "matLevel": "2"}
    alternative7 = {"treeMatchAlgo": "true", "prodFeat": "false", "matLevel": "2"}
    alternative8 = {"treeMatchAlgo": "true", "prodFeat": "true", "matLevel": "2"}
    alternative9 = {"treeMatchAlgo": "false", "prodFeat": "false", "matLevel": "3"}
    alternative10 = {"treeMatchAlgo": "false", "prodFeat": "true", "matLevel": "3"}
    alternative11 = {"treeMatchAlgo": "true", "prodFeat": "false", "matLevel": "3"}
    alternative12 = {"treeMatchAlgo": "true", "prodFeat": "true", "matLevel": "3"}
    alternativen = [alternative1, alternative2, alternative3, alternative4, alternative5, alternative6, alternative7,
                    alternative8, alternative9, alternative10, alternative11, alternative12]

    ist_situation = retrieve_ist_situation()
    invest_params = retrieve_invest_params()

    for a in alternativen:
        improved_time = calculate_total_time(a, ist_situation)
