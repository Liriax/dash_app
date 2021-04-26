class Alternative:
    def __init__(self, treeMatchAlgo, prodFeat, matLevel, alreadyImplemented):
        self.prodFeat = prodFeat
        self.treeMatchAlgo = treeMatchAlgo
        self.matLevel = matLevel
        # 1, if this alternative is the same as "ist_situation"
        self.alreadyImplemented = alreadyImplemented
