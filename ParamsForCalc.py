import pandas as pd

class ParamsForCalc:
    # T: depreciation period = use time
    # r: interest rate
    # c_main: maintenance cost rate
    # c_person: hourly personnel cost rate
    # r_acc: revenue per product variant

    def __init__(self):# t: work preparation time (hour); t_S: time saving; t_t: throughput time
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
            r_acc = invest_params.iloc[0]["npvRevProProduct"]
            self.I_total=I_l2+I_l3+I_al+I_pr 
            self.r=r
            self.C_depr = I_total/T
            self.C_int = 0.5*(I_total)*r
            self.C_main = c_main * I_total
        except pd.errors.EmptyDataError:
            invest_params = 'could not read parameter_Investitionsrechnung.csv'

        

    def npv (self, t_t, t_S, t):
        S_person = c_person * t_S # personnel cost savings
        C_person = c_person * t
        R_acc = r_acc*t_S/t_t # additional revenues
        npv= - I_total
        for t in range (1,T+1):
            npv+=(R_acc+S_person-C_main)/(1+r)**t
        return npv

    def comparison (self):
        return C_depr+C_int+C_main+C_person
        
