import pandas as pd

class CurrentSituation:
    def __init__(self):
        try:
            ist_situation = pd.read_csv(r'assets/ist_situation.csv')
            invest_params = pd.read_csv(r'assets/parameter_Investitionsrechnung.csv')
            conditions = pd.read_csv(r'assets/product_family_conditions.csv')
            methods = pd.read_csv(r'assets/similar_prod_info_methods.csv')

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

            self.matLevel = ist_situation.iloc[0]["matLevel"]
            self.SgB = ist_situation.iloc[0]["SgB"]
            self.SaB = ist_situation.iloc[0]["SaB"]
            self.typeOfTimeMeasurement = ist_situation.iloc[0]["typeOfTimeMeasurement"]
          
            
            self.n_prodFam = len(conditions)
            self.n_SaB = [invest_params.iloc[0]['n_SaB'] for x in range(0, self.n_prodFam)]
            self.mean_amount_of_elem_comp = [list(conditions["mean_amount_of_elem_comp"])[x] if self.n_SaB[x] != 0 else 0 for x in range(0, len(conditions))]

            # calculate cumulative times by using either abs. time * freq or share of total time * total time
            if self.typeOfTimeMeasurement == 'absolute':
                product_families = pd.read_csv(r'assets/product_family_absolute.csv')
                self.cumTimeNewComponent = list(product_families['timeNewComponent'])
                self.cumTimeSimComponent =  list(product_families['timeSimComponent'])
                self.cumTimeSameComponent = list(product_families['timeSameComponent'])
                self.cumtimeProcess =       list(product_families['timeProcess'])
                self.cumtimeResource =      list(product_families['timeResource'])

            if self.typeOfTimeMeasurement == 'relative':
                product_families = pd.read_csv(r'assets/product_family_relative.csv')

                self.totalSearchTimeComponents =list(product_families["totalSearchTimeComponents"])
                self.totalSearchTimeProcesses = list(product_families["totalSearchTimeProcesses"])
                self.totalSearchTimeResources = list(product_families["totalSearchTimeResources"])
                self.shareNewComponent =        list(product_families["shareNewComponent"])
                self.shareSimComponent =        list(product_families["shareSimComponent"])
                self.shareSameComponent =       list(product_families["shareSameComponent"])

                self.cumTimeNewComponent = [self.shareNewComponent[x] * self.totalSearchTimeComponents[x] for x in range(0, len(conditions))]
                self.cumTimeSimComponent = [self.shareSimComponent[x] * self.totalSearchTimeComponents[x]  for x in range(0, len(conditions))]
                self.cumTimeSameComponent = [self.shareSameComponent[x] * self.totalSearchTimeComponents[x] for x in range(0, len(conditions))]
                self.cumtimeProcess = self.totalSearchTimeProcesses
                self.cumtimeResource = self.totalSearchTimeResources
                


        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'

