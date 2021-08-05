import currentSituation
import alternative
import pandas as pd



def calculate_investment(alternative, ist_situation):
    # find out if extra investment is to be made:
    invest_SgB = alternative.SgB - ist_situation.SgB
    invest_SaB = alternative.SaB - ist_situation.SaB
    # find out investment needed for the increase of maturity level:
    mat_increase = 0
    if alternative.matLevel > ist_situation.matLevel:
        if alternative.matLevel == 3 and ist_situation.matLevel == 2:
            mat_increase += ist_situation.I_l3
        if alternative.matLevel == 2 and ist_situation.matLevel == 1:
            mat_increase += ist_situation.I_l2
        if alternative.matLevel == 3 and ist_situation.matLevel == 1:
            mat_increase += ist_situation.I_l2 + ist_situation.I_l3
    
    # calculate amount of investment needed:
    I_total = invest_SgB * ist_situation.I_al + invest_SaB * ist_situation.I_pr + mat_increase
    
    return I_total

def calculate_time(alternative, ist_situation): 

    n_SaB = ist_situation.n_SaB
    all_zeros = [0 for x in range(0, ist_situation.n_prodFam)]
    sameComponent = all_zeros if alternative.SgB == 1 else ist_situation.cumTimeSameComponent
    simComponent = [(0.036*35+15*0.035)*n*m if alternative.SaB == 1 else t for n,m,t in zip(n_SaB,ist_situation.mean_amount_of_elem_comp,ist_situation.cumTimeSimComponent)]
    newComponent = all_zeros if alternative.SgB == 1 and alternative.SaB == 1 else ist_situation.cumTimeNewComponent
    
    
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
            if ist_situation.SgB == 0 and ist_situation.SaB == 0:
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 0 and ist_situation.SaB == 1:
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 1 and ist_situation.SaB == 0:
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 1 and ist_situation.SaB == 1:
                alternatives.append(alternative.Alternative(1, 1, i))
        if ist_situation.matLevel == i:
            if ist_situation.SgB == 0 and ist_situation.SaB == 0:
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 0 and ist_situation.SaB == 1:
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 1 and ist_situation.SaB == 0:
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.SgB == 1 and ist_situation.SaB == 1:
                alternatives.append(alternative.Alternative(1, 1, i))
    return alternatives


class Calculator:
    def __init__(self):
        self.ist_situation = currentSituation.CurrentSituation()
        self.alternatives = create_alternatives(self.ist_situation)
        

    def calculate_npv(self, alternative):
        t_supported = [x/60 for x in calculate_time(alternative, self.ist_situation)]
        t_unsupported = [x/60 for x in calculate_time(self.ist_situation, self.ist_situation)]
         
        I_total = calculate_investment(alternative, self.ist_situation) 
        C_main = self.ist_situation.c_main * I_total # K_IHJ=k_IH*I_0

        r = self.ist_situation.r
        S_person = [self.ist_situation.k_personal * (x - y) for x, y in zip(t_unsupported, t_supported)]  # personnel cost savings
        C_person = [self.ist_situation.k_personal * x for x in t_supported] # K_(P,x)=k_P*t_(Nachher,x)
        K_PJ=sum([c*x for c,x in zip(C_person, self.ist_situation.P_x)]) # K_PJ=∑_(x=1)^X〖K_(P,x)*P_x 〗
        K_J = K_PJ+C_main # K_J=K_PJ+K_IHJ

        # E_(Beschl,x) = e_(Var,x)*l_(M,x)*t_(s,x)/t_(DLZ,x) 
        R_acc = [e_Vx * (x - y) / t * z  for e_Vx, x, y, z, t in zip(self.ist_situation.r_acc, t_unsupported, t_supported, self.ist_situation.l_Mx, self.ist_situation.t_DLZ)] # R_acc: additional revenues
        
        #E_J=∑(E_(P,x)+E_(Beschl,x))*P_x 〗
        E_J=sum([(x+y)*z for x,y,z in zip(S_person,R_acc,self.ist_situation.P_x)])
        
        # KW_0=-I_0+∑(E_J-K_J)/(1+r)^t 
        npv = - I_total
        for t in range(1, self.ist_situation.T + 1):
            npv += (E_J - K_J) / (1 + r) ** t
        return npv

    def calculate_results(self):
        res = []
     
        for alternative in self.alternatives:
            npv = round(self.calculate_npv(alternative),2)
            investition = round(calculate_investment(alternative, self.ist_situation),2)
            t_supported_x =[round(x,2) for x in calculate_time(alternative, self.ist_situation)]
            t_unsupported_x = [round(x,2) for x in calculate_time(self.ist_situation, self.ist_situation)]
            t_supported = sum(t_supported_x)
            t_unsupported = sum(t_unsupported_x)
             
            matLevel = alternative.matLevel
            # n_SaB = self.ist_situation.n_SaB
            SaB = alternative.SaB
            SgB = alternative.SgB
            res.append([npv, investition, t_unsupported,  t_supported, matLevel, SaB, SgB,t_supported_x,t_unsupported_x])
        res_df = pd.DataFrame(res, columns = ['npv', 'investition', 't_unsupported', 't_supported', 'matLevel', 'SaB', 'SgB',"t_supported_x","t_unsupported_x"])
        
        name = ["RG {}{}{}".format(int(res_df.iloc[x]['matLevel']), ", SgB" if res_df.iloc[x]['SgB']==1 else "", ", SäB" if res_df.iloc[x]['SaB']==1 else "") if res_df.iloc[x]['investition'] >0 else "Ist-Situation" for x in range(0, len(res_df))]
        res_df['name']=name
        res_df.to_csv(r'assets/result.csv', index=False)


# test: hat funktioniert 
# c = Calculator()
# for alt in c.alternatives:
#     print(calculate_time(alt, c.ist_situation))


# c = Calculator()
# for alt in c.alternatives:
#     print(alt.matLevel,alt.SgB, alt.SaB)
#     print(calculate_investment(alt, c.ist_situation))
#     print(calculate_time(alt, c.ist_situation))
#     print("npv:" + str(c.calculate_npv(alt)))

# print(c.calculate_results())
