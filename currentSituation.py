import pandas as pd


class CurrentSituation:
    def __init__(self):
        try:
            ist_situation = pd.read_csv('ist_situation.csv')
            conditions = pd.read_csv('product_family_conditions.csv')

            self.matLevel = ist_situation.iloc[0]["matLevel"]
            self.treeMatchAlgo = ist_situation.iloc[0]["treeMatchAlgo"]
            self.prodFeat = ist_situation.iloc[0]["prodFeat"]
            self.typeOfTimeMeasurement = ist_situation.iloc[0]["typeOfTimeMeasurement"]
          
            
            self.n_prodFam = len(conditions)
            self.n_prodFeat=     list(conditions["n_prodFeat"])
            self.mean_amount_of_elem_comp = [list(conditions["mean_amount_of_elem_comp"])[x] if self.n_prodFeat[x] != 0 else 0 for x in range(0, len(conditions))]
            
            # calculate cumulative times by using either abs. time * freq or share of total time * total time
            if self.typeOfTimeMeasurement == 'absolute':
                product_families = pd.read_csv('product_family_absolute.csv')
                self.cumTimeNewComponent = list(product_families['timeNewComponent'])
                self.cumTimeSimComponent =  list(product_families['timeSimComponent'])
                self.cumTimeSameComponent = list(product_families['timeSameComponent'])
                self.cumtimeProcess =       list(product_families['timeProcess'])
                self.cumtimeResource =      list(product_families['timeResource'])

            if self.typeOfTimeMeasurement == 'relative':
                product_families = pd.read_csv('product_family_relative.csv')

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
                


            # if self.treeMatchAlgo == 1:
            #     sameComponent=0
            # else:
            #     sameComponent=self.cumTimeSameComponent
            
            # if self.prodFeat == 1:
            #     simComponent = 0.036*(35+15*self.n_prodFeat)*self.mean_amount_of_elem_comp
            # else:
            #     simComponent = self.cumTimeSimComponent
            
            # if self.treeMatchAlgo == 1 and self.prodFeat == 1:
            #     newComponent = 0
            # else: 
            #     newComponent = self.cumTimeNewComponent
            
            # Process = 0 if self.matLevel >= 2 else self.cumtimeProcess
            # Resource = 0 if self.matLevel == 3 else self.cumtimeResource
            # t_unsupported = \
            #     newComponent + \
            #     simComponent + \
            #     sameComponent + \
            #     Process + \
            #     Resource
            # self.t_unsupported = t_unsupported
        
            # print(self.timeNewComponent)


        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'

