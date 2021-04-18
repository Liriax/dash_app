import pandas as pd
class CurrentSituation:
    def __init__(self):
        try:
            ist_situation = pd.read_csv('ist_situation.csv')
            self.matLevel = ist_situation.iloc[0]["matLevel"]
            self.supFunction = ist_situation.iloc[0]["supFunction"]
        except pd.errors.EmptyDataError:
            ist_situation = 'could not read ist_situation.csv!'
        try:
            invest_params = pd.read_csv('parameter_Investitionsrechnung.csv')
        except pd.errors.EmptyDataError:
            invest_params = 'could not read parameter_Investitionsrechnung.csv'
        
cs = CurrentSituation()
print(cs.matLevel)
print(cs.supFunction)
        