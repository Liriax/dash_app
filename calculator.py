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

    if alternative.treeMatchAlgo == 1:
        improved_time += 0
    else:
        improved_time += ist_situation.timeNewComponent

    if alternative.prodFeat == 1:
        improved_time += 0.036 * (35 + 15 * 9)  # Berechnung nach "TMU", 9 ist Anzahl der Produktmerkmale bei Opitz

    else:
        improved_time += ist_situation.timeSimComponent + ist_situation.timeNewComponent

    if alternative.matLevel == 1:
        improved_time += ist_situation.timeNewProcess + ist_situation.timeSimProcess + \
                         ist_situation.timeSameProcess
        improved_time += ist_situation.timeNewResource + ist_situation.timeSimResource + \
                         ist_situation.timeSameResource

    elif alternative.matLevel == 2:
        improved_time += ist_situation.timeNewProcess
        improved_time += ist_situation.timeNewResource + ist_situation.timeSimResource + \
                         ist_situation.timeSameResource

    elif alternative.matLevel == 3:
        improved_time += ist_situation.timeNewProcess
        improved_time += ist_situation.timeNewResource

    else:
        print('Ungültiger Reifegrad bei Berechnung von Zeitersparnissen!')

    return improved_time


def create_alternatives(ist_situation):
    alternatives = []
    # Here we make sure to only consider alternatives that are at least as good as the current situation
    # for i in range(1, 3): -> should be 4 because range(1,3) is only 1 and 2
    for i in range(1, 4):
        if ist_situation.matLevel <= i:
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(1, 1, i))
    return alternatives


class Calculator:
    def __init__(self):
        self.ist_situation = retrieve_ist_situation()
        self.invest_params = retrieve_invest_params()
        self.alternatives = create_alternatives(self.ist_situation)

    def calculate_npv(self, t_supported):
        # return self.invest_params.C_depr + self.invest_params.C_int + self.invest_params.C_main + self.invest_params.C_person
        # -> C_person needs to be calculated first, which requires the parameter t_supported!
        C_person = self.invest_params.c_person * t_supported
        return self.invest_params.C_depr + self.invest_params.C_int + self.invest_params.C_main + self.invest_params.c_person * t_supported

    # t_supported = t_not_supported - improved_time; t_t: throughput time (?); 
    def calculate_comparison(self, t_supported, improved_time, t_t):
        # MUSS NOCH ANGEPASST WERDEN!!!!
        r = self.invest_params.r
        C_main = self.invest_params.C_main
        S_person = self.invest_params.c_person * improved_time  # personnel cost savings
        C_person = self.invest_params.c_person * t_supported
        R_acc = self.invest_params.r_acc * improved_time / t_t  # R_acc: additional revenues
        npv = - self.I_total
        for t in range(1, self.T + 1):
            npv += (R_acc + S_person - C_main) / (1 + r) ** t
        return npv
    # def calculate_results(self):

# tests: 
# c = Calculator()
# for alt in c.alternatives:
#     print(calculate_time(alt, c.ist_situation))

# print(c.calculate_npv(t_supported=100))

