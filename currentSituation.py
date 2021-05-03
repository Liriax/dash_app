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
            self.totalSearchTime = ist_situation.iloc[0]["totalSearchTime"]
            self.typeOfTimeMeasurement = ist_situation.iloc[0]["typeOfTimeMeasurement"]
            self.shareNewComponent = ist_situation.iloc[0]["shareNewComponent"]
            self.shareSimComponent = ist_situation.iloc[0]["shareSimComponent"]
            self.shareSameComponent = ist_situation.iloc[0]["shareSameComponent"]
            self.shareNewProcess = ist_situation.iloc[0]["shareNewProcess"]
            self.shareSimProcess = ist_situation.iloc[0]["shareSimProcess"]
            self.shareSameProcess = ist_situation.iloc[0]["shareSameProcess"]
            self.shareNewResource = ist_situation.iloc[0]["shareNewResource"]
            self.shareSimResource = ist_situation.iloc[0]["shareSimResource"]
            self.shareSameResource = ist_situation.iloc[0]["shareSameResource"]
            self.n_prodFeat= ist_situation.iloc[0]["n_prodFeat"]   

            # calculate cumulative times by using either abs. time * freq or share of total time * total time
            if self.typeOfTimeMeasurement == 'absolute':
                self.cumTimeNewComponent = self.timeNewComponent * self.freqNewComponent
                self.cumTimeSimComponent = self.timeSimComponent * self.freqSimComponent
                self.cumTimeSameComponent = self.timeSameComponent * self.freqSameComponent
                self.cumTimeNewProcess = self.timeNewProcess * self.freqNewProcess
                self.cumTimeSimProcess = self.timeSimProcess * self.freqSimProcess
                self.cumTimeSameProcess = self.timeSameProcess * self.freqNewProcess
                self.cumTimeNewResource = self.timeNewResource * self.freqNewResource
                self.cumTimeSimResource = self.timeSimResource * self.freqSimResource
                self.cumTimeSameResource = self.timeSameResource * self.freqSameResource
            if self.typeOfTimeMeasurement == 'relative':
                self.cumTimeNewComponent = self.shareNewComponent * self.totalSearchTime
                self.cumTimeSimComponent = self.shareSimComponent * self.totalSearchTime
                self.cumTimeSameComponent = self.shareSameComponent * self.totalSearchTime
                self.cumTimeNewProcess = self.shareNewProcess * self.totalSearchTime
                self.cumTimeSimProcess = self.shareSimProcess * self.totalSearchTime
                self.cumTimeSameProcess = self.shareSameProcess * self.totalSearchTime
                self.cumTimeNewResource = self.shareNewResource * self.totalSearchTime
                self.cumTimeSimResource = self.shareSimResource * self.totalSearchTime
                self.cumTimeSameResource = self.shareSameResource * self.totalSearchTime



            sameComponent = 0 if self.treeMatchAlgo == 1 else self.cumTimeSameComponent
            simComponent = 0.036 * (35 + 15 * 9) if self.prodFeat == 1 else self.cumTimeSimComponent
            newComponent = 0.036 * (35 + 15 * 9) if self.prodFeat == 1 and self.treeMatchAlgo == 1 else self.cumTimeNewComponent
            sameProcess = 0 if self.matLevel >= 2 else self.cumTimeSameProcess
            simProcess = 0 if self.matLevel >= 2 else self.cumTimeSimProcess
            sameResource = 0 if self.matLevel == 3 else self.cumTimeSameResource
            simResource = 0 if self.matLevel == 3 else self.cumTimeSimResource
            self.t_unsupported = \
                newComponent + \
                simComponent + \
                sameComponent + \
                self.cumTimeNewProcess + \
                simProcess + \
                sameProcess + \
                self.cumTimeNewResource + \
                simResource + \
                sameResource

        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'
