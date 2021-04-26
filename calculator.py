import currentSituation
import paramsForCalc
import alternative
import pandas as pd
# amount of opitz product features is 9
amount_of_product_features = 9

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
            mat_increase += params.I_l3
        if alternative.matLevel == 2 and ist_situation.matLevel == 1:
            mat_increase += params.I_l2
        if alternative.matLevel == 3 and ist_situation.matLevel == 1:
            mat_increase += params.I_l2 + params.I_l3
    
    # calculate amount of investment needed:
    I_total = invest_tree_matching * params.I_al + invest_prod_feature * params.I_pr + mat_increase
    
    return I_total

def calculate_time(alternative, ist_situation): 

    sameComponent = 0 if alternative.treeMatchAlgo == 1 else ist_situation.timeSameComponent * ist_situation.freqSameComponent
    simComponent = 0.036 * (35 + 15 * amount_of_product_features) if alternative.prodFeat == 1 else ist_situation.timeSimComponent * ist_situation.freqSimComponent
    newComponent = 0.036 * (35 + 15 * amount_of_product_features) if alternative.prodFeat == 1 and alternative.treeMatchAlgo == 1 else ist_situation.timeNewComponent*ist_situation.freqNewComponent
    sameProcess = 0 if alternative.matLevel >= 2 else ist_situation.timeSameProcess * ist_situation.freqSameProcess
    simProcess = 0 if alternative.matLevel >= 2 else ist_situation.timeSimProcess * ist_situation.freqSimProcess
    sameResource = 0 if alternative.matLevel == 3 else ist_situation.timeSameResource * ist_situation.freqSameResource
    simResource = 0 if alternative.matLevel == 3 else ist_situation.timeSimResource * ist_situation.freqSimResource

    improved_time = newComponent + \
                simComponent + \
                sameComponent + \
                ist_situation.timeNewProcess*ist_situation.freqNewProcess + \
                simProcess + \
                sameProcess + \
                ist_situation.timeNewResource*ist_situation.freqNewResource + \
                simResource + \
                sameResource
    return improved_time


def create_alternatives(ist_situation):
    alternatives = []
    # Here we make sure to only consider alternatives that are at least as good as the current situation
    # for i in range(1, 3): -> should be 4 because range(1,3) is only 1 and 2
    for i in range(1, 4):
        if ist_situation.matLevel < i:
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(0, 0, i, 0))
                alternatives.append(alternative.Alternative(0, 1, i, 0))
                alternatives.append(alternative.Alternative(1, 0, i, 0))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(0, 1, i, 0))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(1, 0, i, 0))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(1, 1, i, 0))
        if ist_situation.matLevel == i:
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(0, 0, i, 1))
                alternatives.append(alternative.Alternative(0, 1, i, 0))
                alternatives.append(alternative.Alternative(1, 0, i, 0))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 0 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(0, 1, i, 1))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 0:
                alternatives.append(alternative.Alternative(1, 0, i, 1))
                alternatives.append(alternative.Alternative(1, 1, i, 0))
            if ist_situation.treeMatchAlgo == 1 and ist_situation.prodFeat == 1:
                alternatives.append(alternative.Alternative(1, 1, i, 1))
    return alternatives


class Calculator:
    def __init__(self):
        self.ist_situation = retrieve_ist_situation()
        self.invest_params = retrieve_invest_params()
        self.alternatives = create_alternatives(self.ist_situation)
        

    def calculate_comparison(self, alternative):
        # return self.invest_params.C_depr + self.invest_params.C_int + self.invest_params.C_main + self.invest_params.C_person
        # -> C_person needs to be calculated first, which requires the parameter  improved_time!
        improved_time = calculate_time(alternative, self.ist_situation)
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params)

        t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
         

        C_depr = I_total / self.invest_params.T
        C_int = 0.5 * I_total * self.invest_params.r
        C_main = self.invest_params.c_main * I_total
        C_person = self.invest_params.c_person * improved_time
        return C_depr + C_int + C_main + C_person

    # improved_time = calculate_time(alternative, self.ist_situation)
    def calculate_npv(self, alternative):
        improved_time = calculate_time(alternative, self.ist_situation)
        t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
         
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params) 
        C_main = self.invest_params.c_main * I_total

        r = self.invest_params.r
        S_person = self.invest_params.c_person * (t_unsupported - improved_time)  # personnel cost savings
        C_person = self.invest_params.c_person * improved_time
        R_acc = self.invest_params.r_acc * (t_unsupported - improved_time) / t_unsupported * self.ist_situation.numNewVariant  # R_acc: additional revenues
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
            t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
             
            matLevel = alternative.matLevel
            prodFeat = alternative.prodFeat
            treeMatchAlgo = alternative.treeMatchAlgo
            alreadyImplemented = alternative.alreadyImplemented
            res.append([npv, comparison, investition, t_unsupported,  improved_time, matLevel, prodFeat, treeMatchAlgo, alreadyImplemented, amount_of_product_features])
        res_df = pd.DataFrame(res, columns = ['npv', 'comparison', 'investition', 't_unsupported', 'improved_time', 'matLevel', 'prodFeat', 'treeMatchAlgo', 'alreadyImplemented', 'amount_of_product_features'])
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
