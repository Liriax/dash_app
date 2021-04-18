import CurrentSituation
import ParamsForCalc
import pandas as pd


def retrieve_ist_situation(): # the read, try and except are done by creating a CurrentSituation object
    # try:
    #     ist_situation = pd.read_csv('ist_situation.csv')
    # except pd.errors.EmptyDataError:
    #     ist_situation = 'could not read ist_situation.csv!'
    # return ist_situation
    return CurrentSituation()


def retrieve_invest_params(): # the read, try and except are done by creating a ParamsForCalc object
    # try:
    #     invest_params = pd.read_csv('parameter_Investitionsrechnung.csv')
    # except pd.errors.EmptyDataError:
    #     invest_params = 'could not read parameter_Investitionsrechnung.csv'
    # return invest_params
    return ParamsForCalc()


def calculate_total_time(alternative, ist_situation):
    new_time = 0
    if(ist_situation.treeMatAlgo == 0): #treeMatAlgo is 0 when it's not used, otherwise it would be 1
        new_time = ist_situation.timeNewComponent
    else:
        new_time += 0



class Calculator:
    alternative1 = {"treeMatchAlgo": 0, "prodFeat": 0, "matLevel": "1"}
    alternative2 = {"treeMatchAlgo": 0, "prodFeat": 1, "matLevel": "1"}
    alternative3 = {"treeMatchAlgo": 1, "prodFeat": 0, "matLevel": "1"}
    alternative4 = {"treeMatchAlgo": 1, "prodFeat": 1, "matLevel": "1"}
    alternative5 = {"treeMatchAlgo": 0, "prodFeat": 0, "matLevel": "2"}
    alternative6 = {"treeMatchAlgo": 0, "prodFeat": 1, "matLevel": "2"}
    alternative7 = {"treeMatchAlgo": 1, "prodFeat": 0, "matLevel": "2"}
    alternative8 = {"treeMatchAlgo": 1, "prodFeat": 1, "matLevel": "2"}
    alternative9 = {"treeMatchAlgo": 0, "prodFeat": 0, "matLevel": "3"}
    alternative10 = {"treeMatchAlgo": 0, "prodFeat": 1, "matLevel": "3"}
    alternative11 = {"treeMatchAlgo": 1, "prodFeat": 0, "matLevel": "3"}
    alternative12 = {"treeMatchAlgo": 1, "prodFeat": 1, "matLevel": "3"}
    alternativen = [alternative1, alternative2, alternative3, alternative4, alternative5, alternative6, alternative7,
                    alternative8, alternative9, alternative10, alternative11, alternative12]

    ist_situation = retrieve_ist_situation()
    invest_params = retrieve_invest_params()

    for a in alternativen:
        improved_time = calculate_total_time(a, ist_situation)
