import pandas as pd


class ParamsForCalc:
    # T: depreciation period = use time
    # r: interest rate
    # c_main: maintenance cost rate
    # c_person: hourly personnel cost rate
    # r_acc: revenue per product variant

    def __init__(self):  # t: work preparation time (hour); t_S: time saving; t_t: throughput time
        try:
            invest_params = pd.read_csv('parameter_Investitionsrechnung.csv')
            I_l2 = invest_params.iloc[0]["I_l2"]
            I_l3 = invest_params.iloc[0]["I_l3"]
            I_al = invest_params.iloc[0]["I_al"]
            I_pr = invest_params.iloc[0]["I_pr"]
            c_person = invest_params.iloc[0]["c_person"]
            c_main = invest_params.iloc[0]["c_main"]
            r = invest_params.iloc[0]["c_int"]
            T = invest_params.iloc[0]["t"]
            self.r = r
            self.c_main = c_main
            self.c_person = c_person
            self.T = T
            self.r_acc = invest_params.iloc[0]["npvRevProProduct"]
            self.I_total = I_l2 + I_l3 + I_al + I_pr
            self.C_depr = self.I_total / T
            self.C_int = 0.5 * self.I_total * r
            self.C_main = c_main * self.I_total
        except pd.errors.EmptyDataError:
            invest_params = 'could not read parameter_Investitionsrechnung.csv'

# p = ParamsForCalc()
# print(p.C_depr)
# print(p.C_int)
# print(p.C_main)