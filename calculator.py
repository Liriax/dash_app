import currentSituation
import paramsForCalc
import alternative
import result
import pandas as pd


def retrieve_ist_situation():  # the read, try and except are done by creating a CurrentSituation object
    return currentSituation.CurrentSituation()


def retrieve_invest_params():  # the read, try and except are done by creating a ParamsForCalc object
    return paramsForCalc.ParamsForCalc()

def calculate_investment(alternative, ist_situation, params):
    # find out if extra investment is to be made:
    invest_tree_matching = alternative.treeMatchAlgo - ist_situation.treeMatchAlgo
    invest_prod_feature = alternative.prodFeat - ist_situation.prodFeat
    # find out investment needed for the increase of maturity level:
    mat_increase = 0
    if alternative.matLevel > ist_situation.matLevel:
        if alternative.matLevel == 3 and ist_situation.matLevel == 2:
            mat_increase+=params.I_l3
        if alternative.matLevel == 2 and ist_situation.matLevel == 1:
            mat_increase+=params.I_l2
        if alternative.matLevel == 3 and ist_situation.matLevel == 1:
            mat_increase+=params.I_l2+params.I_l3
    
    # calculate amount of investment needed:
    I_total = invest_tree_matching * params.I_al + invest_prod_feature * params.I_pr + mat_increase
    
    return I_total

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
        

    def calculate_comparison(self, alternative):
        # return self.invest_params.C_depr + self.invest_params.C_int + self.invest_params.C_main + self.invest_params.C_person
        # -> C_person needs to be calculated first, which requires the parameter t_supported!
        improved_time = calculate_time(alternative, self.ist_situation)
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params)

        t_unsupported = self.ist_situation.t_unsupported
        t_supported = t_unsupported - improved_time

        C_depr = I_total / self.invest_params.T
        C_int = 0.5 * I_total * self.invest_params.r
        C_main = self.invest_params.c_main * I_total
        C_person = self.invest_params.c_person * t_supported
        return C_depr + C_int + C_main + C_person

    # improved_time = calculate_time(alternative, self.ist_situation)
    def calculate_npv(self, alternative):
        improved_time = calculate_time(alternative, self.ist_situation)
        t_unsupported = self.ist_situation.t_unsupported
        t_supported = t_unsupported - improved_time
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params) 
        C_main = self.invest_params.c_main * I_total

        r = self.invest_params.r
        S_person = self.invest_params.c_person * improved_time  # personnel cost savings
        C_person = self.invest_params.c_person * t_supported
        R_acc = self.invest_params.r_acc * improved_time / t_unsupported * self.ist_situation.numNewVariant  # R_acc: additional revenues
        npv = - I_total
        for t in range(1, self.invest_params.T + 1):
            npv += (R_acc + S_person - C_main) / (1 + r) ** t
        return npv

    def calculate_results(self):
        res = []
        for alternative in self.alternatives:
            npv = self.calculate_npv(alternative)
            comparison = self.calculate_comparison(alternative)
            investition = calculate_investment(alternative, self.ist_situation, self.invest_params) 
            improved_time = calculate_time(alternative, self.ist_situation)
            t_unsupported = self.ist_situation.t_unsupported
            t_supported = t_unsupported - improved_time
            matLevel = alternative.matLevel
            prodFeat = alternative.prodFeat
            treeMatchAlgo = alternative.treeMatchAlgo
            res.append([npv,comparison,investition, t_unsupported, t_supported, matLevel, prodFeat, treeMatchAlgo])
        res_df = pd.DataFrame(res, columns = ['npv','comparison','investition', 't_unsupported', 't_supported', 'matLevel', 'prodFeat', 'treeMatchAlgo'])
        res_df.to_csv('result.csv', index=False)


# test: hat funktioniert 
# c = Calculator()
# for alt in c.alternatives:
#     print(calculate_time(alt, c.ist_situation))

# print(c.calculate_npv(calculate_time(c.alternatives[0], c.ist_situation)))

# c = Calculator()
# for alt in c.alternatives:
#     print(alt.matLevel,alt.treeMatchAlgo, alt.prodFeat)
#     print(calculate_investment(alt, c.ist_situation, c.invest_params))
#     print(calculate_time(alt, c.ist_situation))
#     print("npv:" + str(c.calculate_npv(alt)))
#     print("costs:" + str(c.calculate_comparison(alt)))

# print(c.calculate_results())
