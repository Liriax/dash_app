import currentSituation
import paramsForCalc
import alternative
import result
import pandas as pd


def retrieve_ist_situation():  # the read, try and except are done by creating a CurrentSituation object
    return currentSituation.CurrentSituation()


def retrieve_invest_params():  # the read, try and except are done by creating a ParamsForCalc object
    return paramsForCalc.ParamsForCalc()


def calculate_time(alternative, ist_situation):
    improved_time = 0

    if alternative.treeMatAlgo == '1':
        improved_time += 0
    else:
        improved_time += ist_situation.timeNewComponent

    if alternative.prodFeat == '1':
        improved_time += 0.036 * (35 + 15 * 9)  # Berechnung nach "TMU", 9 ist Anzahl der Produktmerkmale bei Opitz

    else:
        improved_time += ist_situation.timeSimComponent + ist_situation.timeNewComponent

    if alternative.matLevel == '1':
        improved_time += ist_situation.timeNewProcess + ist_situation.timeSimProcess + \
                         ist_situation.timeSameProcess
        improved_time += ist_situation.timeNewResource + ist_situation.timeSimResource + \
                         ist_situation.timeSameResource

    elif alternative.matLevel == '2':
        improved_time += ist_situation.timeNewProcess
        improved_time += ist_situation.timeNewResource + ist_situation.timeSimResource + \
                         ist_situation.timeSameResource

    elif alternative.matLevel == '3':
        improved_time += ist_situation.timeNewProcess
        improved_time += ist_situation.timeNewResource

    else:
        print('Ungültiger Reifegrad bei Berechnung von Zeitersparnissen!')

    return improved_time


def create_alternatives(ist_situation):
    alternatives = []
    # Here we make sure to only consider alternatives that are at least as good as the current situation
    for i in range(1, 3):
        if ist_situation.matLevel <= i:
            if ist_situation.treeMatchAlgo == '0' and ist_situation.prodFeat == '0':
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == '0' and ist_situation.prodFeat == '1':
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == '1' and ist_situation.prodFeat == '0':
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == '1' and ist_situation.prodFeat == '1':
                alternatives.append(alternative.Alternative(1, 1, i))
    return alternatives


class Calculator:
    def __init__(self):
        self.ist_situation = retrieve_ist_situation()
        self.invest_params = retrieve_invest_params()
        self.alternatives = create_alternatives(self.ist_situation)

    def calculate_npv(self):
        return self.invest_params.C_depr + self.C_int + self.C_main + self.C_person


    def calculate_comparison(self):
        # MUSS NOCH ANGEPASST WERDEN!!!!
        S_person = self.c_person * t_S  # personnel cost savings
        C_person = self.c_person * t
        R_acc = self.r_acc * t_S / t_t  # additional revenues
        npv = - self.I_total
        for t in range(1, self.T + 1):
            npv += (R_acc + S_person - self.C_main) / (1 + self.r) ** t
        return npv
    def calculate_results(self):

