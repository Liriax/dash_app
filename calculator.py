import currentSituation
import paramsForCalc
import alternative
import pandas as pd



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

    n_prodFeat = ist_situation.n_prodFeat
    all_zeros = [0 for x in range(0, ist_situation.n_prodFam)]
    sameComponent = all_zeros if alternative.treeMatchAlgo == 1 else ist_situation.cumTimeSameComponent
    simComponent = [(0.036*35+15*0.035)*n*m if alternative.prodFeat == 1 else t for n,m,t in zip(n_prodFeat,ist_situation.mean_amount_of_elem_comp,ist_situation.cumTimeSimComponent)]
    newComponent = all_zeros if alternative.treeMatchAlgo == 1 and alternative.prodFeat == 1 else ist_situation.cumTimeNewComponent
    
    
    Process = all_zeros if alternative.matLevel >= 2 else ist_situation.cumtimeProcess
    Resource = all_zeros if alternative.matLevel == 3 else ist_situation.cumtimeResource

    t_supported = [newComponent[x] + simComponent[x] + sameComponent[x] + Process[x] + Resource[x] for x in range(0, ist_situation.n_prodFam)]

    return t_supported


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
        
    # # no longer needed!
    # def calculate_comparison(self, alternative):
        
    #     t_supported = [x/60 for x in calculate_time(alternative, self.ist_situation)]
    #     I_total = calculate_investment(alternative, self.ist_situation, self.invest_params)         

    #     C_depr = I_total / self.invest_params.T
    #     C_int = 0.5 * I_total * self.invest_params.r
    #     C_main = self.invest_params.c_main * I_total
    #     C_person = [self.invest_params.k_personal * x for x in t_supported]
    #     return C_depr + C_int + C_main + C_person

    def calculate_npv(self, alternative):
        t_supported = [x/60 for x in calculate_time(alternative, self.ist_situation)]
        t_unsupported = [x/60 for x in calculate_time(self.ist_situation, self.ist_situation)]
         
        I_total = calculate_investment(alternative, self.ist_situation, self.invest_params) 
        C_main = self.invest_params.c_main * I_total # K_IHJ=k_IH*I_0

        r = self.invest_params.r
        S_person = [self.invest_params.k_personal * (x - y) for x, y in zip(t_unsupported, t_supported)]  # personnel cost savings
        C_person = [self.invest_params.k_personal * x for x in t_supported] # K_(P,x)=k_P*t_(Nachher,x)
        K_PJ=sum([c*x for c,x in zip(C_person, self.invest_params.P_x)]) # K_PJ=∑_(x=1)^X▒〖K_(P,x)*P_x 〗_
        K_J = K_PJ+C_main # K_J=K_PJ+K_IHJ
        # E_(Beschl,x) = e_(Var,x)*l_(M,x)*t_(s,x)/t_(DLZ,x) 
        R_acc = [e_Vx * (x - y) / t * z  for e_Vx, x, y, z, t in zip(self.invest_params.r_acc, t_unsupported, t_supported, self.invest_params.l_Mx, self.invest_params.t_DLZ)] # R_acc: additional revenues
        
        #E_J=∑(E_(P,x)+E_(Beschl,x))*P_x 〗
        E_J=sum([(x+y)*z for x,y,z in zip(S_person,R_acc,self.invest_params.P_x)])
        
        # KW_0=-I_0+∑(E_J-K_J)/(1+r)^t 
        npv = - I_total
        for t in range(1, self.invest_params.T + 1):
            npv += (E_J - K_J) / (1 + r) ** t
        return npv

    def calculate_results(self):
        res = []
     
        for alternative in self.alternatives:
            npv = round(self.calculate_npv(alternative),2)
            investition = round(calculate_investment(alternative, self.ist_situation, self.invest_params),2)
            t_supported_x =[round(x,2) for x in calculate_time(alternative, self.ist_situation)]
            t_unsupported_x = [round(x,2) for x in calculate_time(self.ist_situation, self.ist_situation)]
            print(t_supported_x)
            t_supported = sum(t_supported_x)
            t_unsupported = sum(t_unsupported_x)
             
            matLevel = alternative.matLevel
            # n_prodFeat = self.ist_situation.n_prodFeat
            prodFeat = alternative.prodFeat
            treeMatchAlgo = alternative.treeMatchAlgo
            alreadyImplemented = alternative.alreadyImplemented
            res.append([npv, investition, t_unsupported,  t_supported, matLevel, prodFeat, treeMatchAlgo, alreadyImplemented,t_supported_x,t_unsupported_x])
        res_df = pd.DataFrame(res, columns = ['npv', 'investition', 't_unsupported', 't_supported', 'matLevel', 'prodFeat', 'treeMatchAlgo', 'alreadyImplemented',"t_supported_x","t_unsupported_x"])
        
        name = ["RG {}{}{}".format(int(res_df.iloc[x]['matLevel']), ", SgB" if res_df.iloc[x]['treeMatchAlgo']==1 else "", ", SäB" if res_df.iloc[x]['prodFeat']==1 else "") if res_df.iloc[x]['investition'] >0 else "Ist-Situation" for x in range(0, len(res_df))]
        res_df['name']=name
        res_df.to_csv('result.csv', index=False)


# test: hat funktioniert 
# c = Calculator()
# for alt in c.alternatives:
#     print(calculate_time(alt, c.ist_situation))


# c = Calculator()
# for alt in c.alternatives:
#     print(alt.matLevel,alt.treeMatchAlgo, alt.prodFeat)
#     print(calculate_investment(alt, c.ist_situation, c.invest_params))
#     print(calculate_time(alt, c.ist_situation))
#     print("npv:" + str(c.calculate_npv(alt)))

# print(c.calculate_results())
