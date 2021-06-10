import pandas as pd


class CurrentSituation:
    def __init__(self):
        try:
            ist_situation = pd.read_csv('ist_situation.csv')
            self.matLevel = ist_situation.iloc[0]["matLevel"]
            self.treeMatchAlgo = ist_situation.iloc[0]["treeMatchAlgo"]
            self.prodFeat = ist_situation.iloc[0]["prodFeat"]
            self.timeNewComponent = ist_situation.iloc[0]["timeNewComponent"]
            self.timeSimComponent = ist_situation.iloc[0]["timeSimComponent"]
            self.timeSameComponent = ist_situation.iloc[0]["timeSameComponent"]
            self.timeProcess = ist_situation.iloc[0]["timeProcess"]
            
            self.timeResource = ist_situation.iloc[0]["timeResource"]
            
            self.numNewVariant = ist_situation.iloc[0]["numNewVariant"]
            
            self.totalSearchTimeComponents = ist_situation.iloc[0]["totalSearchTimeComponents"]
            self.totalSearchTimeProcesses = ist_situation.iloc[0]["totalSearchTimeProcesses"]
            self.totalSearchTimeResources = ist_situation.iloc[0]["totalSearchTimeResources"]
            self.typeOfTimeMeasurement = ist_situation.iloc[0]["typeOfTimeMeasurement"]
            self.shareNewComponent = ist_situation.iloc[0]["shareNewComponent"]
            self.shareSimComponent = ist_situation.iloc[0]["shareSimComponent"]
            self.shareSameComponent = ist_situation.iloc[0]["shareSameComponent"]
           
            self.n_prodFeat= ist_situation.iloc[0]["n_prodFeat"]
            self.mean_amount_of_elem_comp = ist_situation.iloc[0]["mean_amount_of_elem_comp"] if self.n_prodFeat != 0 else 0

            # calculate cumulative times by using either abs. time * freq or share of total time * total time
            if self.typeOfTimeMeasurement == 'absolute':
                self.cumTimeNewComponent = self.timeNewComponent
                self.cumTimeSimComponent = self.timeSimComponent
                self.cumTimeSameComponent = self.timeSameComponent 
                self.cumtimeProcess = self.timeProcess
                self.cumtimeResource = self.timeResource 
            if self.typeOfTimeMeasurement == 'relative':
                self.cumTimeNewComponent = self.shareNewComponent * self.totalSearchTimeComponents
                self.cumTimeSimComponent = self.shareSimComponent * self.totalSearchTimeComponents
                self.cumTimeSameComponent = self.shareSameComponent * self.totalSearchTimeComponents
                self.cumtimeProcess = self.totalSearchTimeProcesses
                self.cumtimeResource = self.totalSearchTimeResources
                


            if self.treeMatchAlgo == 1:
                sameComponent=0
            else:
                sameComponent=self.cumTimeSameComponent
            
            if self.prodFeat == 1:
                simComponent = 0.036*(35+15*self.n_prodFeat)*self.mean_amount_of_elem_comp
            else:
                simComponent = self.cumTimeSimComponent
            
            if self.treeMatchAlgo == 1 and self.prodFeat == 1:
                newComponent = 0
            else: 
                newComponent = self.cumTimeNewComponent
            
            Process = 0 if self.matLevel >= 2 else self.cumtimeProcess
            Resource = 0 if self.matLevel == 3 else self.cumtimeResource
            t_unsupported = \
                newComponent + \
                simComponent + \
                sameComponent + \
                Process + \
                Resource
            self.t_unsupported = t_unsupported

        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'
