import currentSituation
import paramsForCalc
import alternative
import pandas as pd
# amount of opitz product features is 9
n_prodFeat = 9

# def retrieve_ist_situation():  # the read, try and except are done by creating a CurrentSituation object
#     return currentSituation.CurrentSituation()


# def retrieve_invest_params():  # the read, try and except are done by creating a ParamsForCalc object
#     return paramsForCalc.ParamsForCalc()


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

#"calculate_time" takes in time durations in minutes but returns the total time in hours!
def calculate_time(alternative, ist_situation): 
    n_prodFeat = ist_situation.n_prodFeat
    sameComponent = 0 if alternative.treeMatchAlgo == 1 else ist_situation.cumTimeSameComponent
    simComponent = 0.036 * (35 + 15 * n_prodFeat) if alternative.prodFeat == 1 else ist_situation.cumTimeSimComponent
    newComponent = 0.036 * (35 + 15 * n_prodFeat) if alternative.prodFeat == 1 and alternative.treeMatchAlgo == 1 \
                                                else ist_situation.cumTimeNewComponent
    sameProcess = 0 if alternative.matLevel >= 2 else ist_situation.cumTimeSameProcess
    simProcess = 0 if alternative.matLevel >= 2 else ist_situation.cumTimeSimProcess
    sameResource = 0 if alternative.matLevel == 3 else ist_situation.cumTimeSameResource
    simResource = 0 if alternative.matLevel == 3 else ist_situation.cumTimeSimResource

    t_supported = newComponent + \
                simComponent + \
                sameComponent + \
                ist_situation.cumTimeNewProcess + \
                simProcess + \
                sameProcess + \
                ist_situation.cumTimeNewResource + \
                simResource + \
                sameResource
    return round(t_supported/60, 1)


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
        self.ist_situation = currentSituation.CurrentSituation()
        self.invest_params = paramsForCalc.ParamsForCalc()
        self.alternatives = create_alternatives(self.ist_situation)
        

    def calculate_comparison(self, alternative):
        
        t_supported = calculate_time(alternative, self.ist_situation)
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params)

        t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
         

        C_depr = I_total / self.invest_params.T
        C_int = 0.5 * I_total * self.invest_params.r
        C_main = self.invest_params.c_main * I_total
        C_person = self.invest_params.k_personal * t_supported
        return C_depr + C_int + C_main + C_person

    def calculate_npv(self, alternative):
        t_supported = calculate_time(alternative, self.ist_situation)
        t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
         
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params) 
        C_main = self.invest_params.c_main * I_total

        r = self.invest_params.r
        S_person = self.invest_params.k_personal * (t_unsupported - t_supported)  # personnel cost savings

        C_person = self.invest_params.k_personal * t_supported
        R_acc = self.invest_params.r_acc * (t_unsupported - t_supported) / t_unsupported * self.ist_situation.numNewVariant  # R_acc: additional revenues
        npv = - I_total
        for t in range(1, self.invest_params.T + 1):
            npv += (R_acc - C_main - C_person) / (1 + r) ** t
        return npv

    def calculate_results(self):
        res = []
        for alternative in self.alternatives:
            npv = int(self.calculate_npv(alternative))
            comparison = int(self.calculate_comparison(alternative))
            investition = int(calculate_investment(alternative, self.ist_situation, self.invest_params))
            t_supported = calculate_time(alternative, self.ist_situation)
            t_unsupported = calculate_time(self.ist_situation, self.ist_situation)
             
            matLevel = alternative.matLevel
            prodFeat = alternative.prodFeat
            treeMatchAlgo = alternative.treeMatchAlgo
            alreadyImplemented = alternative.alreadyImplemented
            res.append([npv, comparison, investition, t_unsupported,  t_supported, matLevel, prodFeat, treeMatchAlgo, alreadyImplemented, n_prodFeat])
        res_df = pd.DataFrame(res, columns = ['npv', 'comparison', 'investition', 't_unsupported', 't_supported', 'matLevel', 'prodFeat', 'treeMatchAlgo', 'alreadyImplemented', 'n_prodFeat'])
        
        name = ["RG {}{}{}".format(int(res_df.iloc[x]['matLevel']), ", SA" if res_df.iloc[x]['treeMatchAlgo']==1 else "", ", BA" if res_df.iloc[x]['prodFeat']==1 else "") if res_df.iloc[x]['investition'] >0 else "Ist-Situation" for x in range(0, len(res_df))]
        res_df['name']=name
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
