import currentSituation
import alternative
import pandas as pd

# Instandhaltungskosten für Gesamtlösung berechnen
def calculate_cost_with_diff_c_main(alternative, ist_situation,  c_main_l2,c_main_l3,c_main_same,c_main_sim):
    # find out if extra investment is to be made:
    invest_IiA = alternative.IiA - ist_situation.IiA
    invest_KäA = alternative.KäA - ist_situation.KäA
    mat_increase = 0
    if alternative.matLevel > ist_situation.matLevel:
        if alternative.matLevel == 3 and ist_situation.matLevel == 2:
            mat_increase += ist_situation.I_l3 * c_main_l2
        if alternative.matLevel == 2 and ist_situation.matLevel == 1:
            mat_increase += ist_situation.I_l2 * c_main_l3
        if alternative.matLevel == 3 and ist_situation.matLevel == 1:
            mat_increase += ist_situation.I_l2 * c_main_l2 + ist_situation.I_l3* c_main_l3
    
    I_total = invest_IiA * ist_situation.I_al * c_main_same + invest_KäA * ist_situation.I_pr * c_main_sim+mat_increase
    
    return I_total

# calculate total investment
def calculate_investment(alternative, ist_situation):
    # find out if extra investment is to be made:
    invest_IiA = alternative.IiA - ist_situation.IiA
    invest_KäA = alternative.KäA - ist_situation.KäA
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
    I_total = invest_IiA * ist_situation.I_al + invest_KäA * ist_situation.I_pr + mat_increase
    
    return I_total

def calculate_time(alternative, ist_situation): 

    n_KäA = ist_situation.n_KäA
    all_zeros = [0 for x in range(0, ist_situation.n_prodFam)]
    sameComponent = all_zeros if alternative.IiA == 1 else ist_situation.cumTimeSameComponent
    simComponent = [(0.0006*35+15*0.0006)*n*m if alternative.KäA == 1 else t for n,m,t in zip(n_KäA,ist_situation.mean_amount_of_elem_comp,ist_situation.cumTimeSimComponent)]
    newComponent = all_zeros if alternative.IiA == 1 and alternative.KäA == 1 else ist_situation.cumTimeNewComponent
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
            if ist_situation.IiA == 0 and ist_situation.KäA == 0:
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 0 and ist_situation.KäA == 1:
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 1 and ist_situation.KäA == 0:
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 1 and ist_situation.KäA == 1:
                alternatives.append(alternative.Alternative(1, 1, i))
        if ist_situation.matLevel == i:
            if ist_situation.IiA == 0 and ist_situation.KäA == 0:
                alternatives.append(alternative.Alternative(0, 0, i))
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 0 and ist_situation.KäA == 1:
                alternatives.append(alternative.Alternative(0, 1, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 1 and ist_situation.KäA == 0:
                alternatives.append(alternative.Alternative(1, 0, i))
                alternatives.append(alternative.Alternative(1, 1, i))
            if ist_situation.IiA == 1 and ist_situation.KäA == 1:
                alternatives.append(alternative.Alternative(1, 1, i))
    return alternatives


class Calculator:
    def __init__(self,ist_situation,invest_params,conditions,product_family_absolute,product_family_relative):
        self.ist_situation = currentSituation.CurrentSituation(ist_situation,invest_params,conditions,product_family_absolute,product_family_relative)
        self.alternatives = create_alternatives(self.ist_situation)
        
    # Kapitalwerte für Gesamtlösung berechnen
    def calculate_npv(self, alternative):
        t_supported = [x for x in calculate_time(alternative, self.ist_situation)]
        t_unsupported = [x for x in calculate_time(self.ist_situation, self.ist_situation)]
         
        c_main_l2 = self.ist_situation.c_main_l2 
        c_main_l3 = self.ist_situation.c_main_l3 
        c_main_same = self.ist_situation.c_main_same 
        c_main_sim = self.ist_situation.c_main_sim 
        C_main = calculate_cost_with_diff_c_main(alternative, self.ist_situation, c_main_l2,c_main_l3,c_main_same,c_main_sim) 
        I_total = calculate_investment(alternative,self.ist_situation)

        k_P=self.ist_situation.k_personal / 60 # convert to minutes
        r = self.ist_situation.r
        x_specific = sum([(k_P*(t_vorher-t_nachher)+e_Var*l_M*(t_vorher-t_nachher)/t_DLZ)*P-k_P*t_nachher*P for t_vorher, t_nachher, e_Var, l_M,t_DLZ,P in zip(t_unsupported,t_supported,self.ist_situation.r_acc,self.ist_situation.l_Mx, self.ist_situation.t_DLZ,self.ist_situation.P_x)]) 
        npv = - I_total
        assert isinstance(int(self.ist_situation.T), int), str(self.ist_situation.T)
        for t in range(1, int(self.ist_situation.T) + 1): 
            # npv += (E_J - K_J) / ((1 + r) ** t)
            npv += (x_specific - C_main)/ ((1 + r) ** t)
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
            KäA = alternative.KäA
            IiA = alternative.IiA
            res.append([npv, investition, t_unsupported,  t_supported, matLevel, KäA, IiA,t_supported_x,t_unsupported_x])

        res_df = pd.DataFrame(res, columns = ['npv', 'investition', 't_unsupported', 't_supported', 'matLevel', 'KäA', 'IiA',"t_supported_x","t_unsupported_x"])
        name = ["RG {}{}{}".format(int(res_df.iloc[x]['matLevel']), ", IiA" if res_df.iloc[x]['IiA']==1 else "", ", KäA" if res_df.iloc[x]['KäA']==1 else "") if res_df.iloc[x]['investition'] >0 else "Ist-Situation" for x in range(0, len(res_df))]
        res_df['name']=name
        return res_df

# # test: hat funktioniert 
# # c = Calculator()
# # for alt in c.alternatives:
# #     print(calculate_time(alt, c.ist_situation))


# # c = Calculator()
# # for alt in c.alternatives:
# #     print(alt.matLevel,alt.IiA, alt.KäA)
# #     print(calculate_investment(alt, c.ist_situation))
# #     print(calculate_time(alt, c.ist_situation))
# #     print("npv:" + str(c.calculate_npv(alt)))

# # print(c.calculate_results())

# I_total=3000
# c_main=0.2
# r=0.12
# T=5
# t_w=38.5
# K_PGrund=3200 # Monatsgehalt
# k_PGrund=K_PGrund*12*7/(365*t_w)
# k_PNeben=0.726
# k_P=k_PGrund+k_PGrund*k_PNeben # pro Stunde
# k_P/=60.0 # pro Minute
# t_unsupported=[40]
# t_supported=[3]
# r_acc=[10]
# l_Mx=[10] 
# t_DLZ=[10]
# P_x=[10]
# C_main = I_total*c_main
# x_specific = sum([(k_P*(t_vorher-2*t_nachher)+e_Var*l_M*(t_vorher-t_nachher)/t_DLZ)*P for t_vorher, t_nachher, e_Var, l_M,t_DLZ,P in zip(t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)])

# npv = - I_total
# for t in range(1, int(T) + 1): 
#     npv += (x_specific - C_main)/ ((1 + r) ** t)

# # print(npv)