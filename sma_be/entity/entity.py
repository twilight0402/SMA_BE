class SectorAnalysis:
    def __init__(self):
        self.sectorID = ""
        self.sectorName = ""
        self.recordTime = []
        self.lastTrade = []
        self.changeAmount = []
        self.changeRate = []
        self.totalCapit = []
        self.turnoverRate = []


class SectorInfo:
    def __init__(self):
        # 11个属性
        self.sectorID = ""
        self.sectorName = ""
        self.sectorType = ""
        self.recordTime = ""
        self.lastTrade = ""
        self.changeAmount = ""
        self.changeRate = ""
        self.totalCapit = ""
        self.turnoverRate = ""
        self.riseNumber = ""
        self.fallNumber = ""
