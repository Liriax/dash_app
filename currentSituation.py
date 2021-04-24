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
            self.timeNewProcess = ist_situation.iloc[0]["timeNewProcess"]
            self.timeSimProcess = ist_situation.iloc[0]["timeSimProcess"]
            self.timeSameProcess = ist_situation.iloc[0]["timeSameProcess"]
            self.timeNewResource = ist_situation.iloc[0]["timeNewResource"]
            self.timeSimResource = ist_situation.iloc[0]["timeSimResource"]
            self.timeSameResource = ist_situation.iloc[0]["timeSameResource"]
            self.numNewVariant = ist_situation.iloc[0]["numNewVariant"]
            self.freqNewComponent = ist_situation.iloc[0]["freqNewComponent"]
            self.freqSimComponent = ist_situation.iloc[0]["freqSimComponent"]
            self.freqSameComponent = ist_situation.iloc[0]["freqSameComponent"]
            self.freqNewProcess = ist_situation.iloc[0]["freqNewProcess"]
            self.freqSimProcess = ist_situation.iloc[0]["freqSimProcess"]
            self.freqSameProcess = ist_situation.iloc[0]["freqSameProcess"]
            self.freqNewResource = ist_situation.iloc[0]["freqNewResource"]
            self.freqSimResource = ist_situation.iloc[0]["freqSimResource"]
            self.freqSameResource = ist_situation.iloc[0]["freqSameResource"]
            # calculate t_suchzeiten: 
            sameComponent = 0 if self.treeMatchAlgo == 1 else self.timeSameComponent * self.freqSameComponent
            simComponent = 0.036 * (35 + 15 * 9) if self.prodFeat == 1 else self.timeSimComponent * self.freqSimComponent
            newComponent = 0.036 * (35 + 15 * 9) if self.prodFeat == 1 and self.treeMatchAlgo == 1 else self.timeNewComponent*self.freqNewComponent
            sameProcess = 0 if self.matLevel >= 2 else self.timeSameProcess * self.freqSameProcess
            simProcess = 0 if self.matLevel >= 2 else self.timeSimProcess * self.freqSimProcess
            sameResource = 0 if self.matLevel == 3 else self.timeSameResource * self.freqSameResource
            simResource = 0 if self.matLevel == 3 else self.timeSimResource * self.freqSimResource
            self.t_unsupported = \
                newComponent + \
                simComponent + \
                sameComponent + \
                self.timeNewProcess*self.freqNewProcess + \
                simProcess + \
                sameProcess + \
                self.timeNewResource*self.freqNewResource + \
                simResource + \
                sameResource

        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'
