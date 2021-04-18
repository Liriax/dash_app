class ParamsForCalc:
    # T: depreciation period = use time

    # r: interest rate

    # c_main: maintenance cost rate

    # c_person: hourly personnel cost rate

    # t: work preparation time (hour)
    # t_S: time saving
    # t_t: throughput time
    # r_acc: revenue per product variant

    def __init__(I_l2, I_l3, I_al, I_pr, T, r_acc, t_t, c_person, t_S , c_main, r, t):
        self.I_total=I_l2+I_l3+I_al+I_pr 
        self.S_person = c_person * t_S # personnel cost savings
        self.r=r
        self.C_depr = I_total/T
        self.C_int = 0.5*(I_total)*r
        self.C_main = c_main * I_total
        self.C_person = c_person * t
        self.R_acc = r_acc*t_S/t_t # additional revenues

    def npv (self):
        npv= - I_total
        for t in range (1,T+1):
            npv+=(R_acc+S_person-C_main)/(1+r)**t
        return npv

    def comparison (self):
        return C_depr+C_int+C_main+C_person
        