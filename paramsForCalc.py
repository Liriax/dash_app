import pandas as pd


class ParamsForCalc:
    # T: depreciation period = use time
    # r: interest rate
    # c_main: maintenance cost rate
    # AS: hourly personnel cost rate
    # r_acc: revenue per product variant

    ("Durschnittliche Anzahl an unbekannten Bauteilen","mean_amount_of_elem_comp"),
    def __init__(self):  
        try:
            invest_params = pd.read_csv('parameter_Investitionsrechnung.csv')
            conditions = pd.read_csv('product_family_conditions.csv')
            self.I_l2 = invest_params.iloc[0]["I_l2"]
            self.I_l3 = invest_params.iloc[0]["I_l3"]
            self.I_al = invest_params.iloc[0]["I_al"]
            self.I_pr = invest_params.iloc[0]["I_pr"]
            self.AS = invest_params.iloc[0]["AS"]
            #K_PGrund is given in €/Month
            self.K_PGrund = invest_params.iloc[0]["K_PGrund"]
            self.c_main = invest_params.iloc[0]["c_main"] / 100
            self.r = invest_params.iloc[0]["c_int"] / 100
            self.T = invest_params.iloc[0]["t"]
            # 0.726 is german standard for "Personalnebenkosten", k_personal is given in €/h
            self.k_personal = (self.K_PGrund * 12 * 7 * (1 + 0.726)) / (365 * self.AS)
            self.r_acc = list(conditions["npvRevProProduct"])
            self.t_DLZ=  list(conditions['t_DLZ'])
            self.l_Mx =  list(conditions['l_Mx'])
            self.P_x =   list(conditions['P_x'])

        except pd.errors.EmptyDataError:
            invest_params = 'could not read parameter_Investitionsrechnung.csv'

# p = ParamsForCalc()
# print(p.C_depr)
# print(p.C_int)
# print(p.C_main)