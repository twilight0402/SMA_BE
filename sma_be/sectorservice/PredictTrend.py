from django.http import HttpResponse
from sma_be.sectorservice import AIModel
from sma_be.sectorDao import SectorAnalysisDao
from sma_be.sectorservice.AIModel import Net
import datetime
import json


def getPriceTrend(sectorID: str):
    priceChange_list = AIModel.getPredictData(sectorID)
    return priceChange_list


def getFutureTime(lastTime: str, days_num: int):
    predictTime = []
    for i in range(days_num):
        while True:
            newTime = datetime.datetime.strptime(lastTime, '%Y-%m-%d')
            newTime = newTime + datetime.timedelta(days=1)
            lastTime = newTime.strftime('%Y-%m-%d')
            if newTime.weekday() not in [5, 6]:
                break

        predictTime.append(lastTime)
    return predictTime


def sendPredictData(request):
    sectorID = str(request.GET.get("sectorID"))
    old_data_len = 14
    if sectorID is not None:
        priceChange_list = getPriceTrend(sectorID)
        sectorAnalysis = SectorAnalysisDao.getSectorDayAnalysisList([sectorID])[0]
        oldTime = sectorAnalysis.recordTime[-old_data_len:]
        newTime = getFutureTime(oldTime[-1], 7)
        oldPrice = sectorAnalysis.lastTrade[-old_data_len:]

        base_info = {"status": 200,"dataName": "priceTrend",
                     "recordTime": oldTime + newTime,
                     "oldData": oldPrice + [None, ] * 7,
                     "predictData": [None, ] * (old_data_len-1) + [oldPrice[-1]] + priceChange_list}
        return HttpResponse(json.dumps(base_info))
    else:
        return HttpResponse(" ")

