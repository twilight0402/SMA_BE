from django.http import HttpResponse
# from django.http.response import JsonResponse
from sma_be.sectorDao import SectorAnalysisDao
from sma_be.sectorservice import HotSector
# from backend.sectorservice import PredictTrend
# from backend.sectorservice.AIModel import Net

import json


def dataAlign(sectorList):
    '''
    数据对齐
    :param sectorList:
    :return:
    '''
    # 找到最大长度
    max_len = 0
    for item in sectorList:
        max_len = max(max_len, len(item.recordTime))

    for item in sectorList:
        item.recordTime = ["", ] * (max_len - len(item.recordTime)) + item.recordTime
        item.lastTrade = [None, ] * (max_len - len(item.lastTrade)) + item.lastTrade
        item.changeAmount = [0, ] * (max_len - len(item.changeAmount)) + item.changeAmount
        item.changeRate = [0, ] * (max_len - len(item.changeRate)) + item.changeRate
        item.totalCapit = [0, ] * (max_len - len(item.totalCapit)) + item.totalCapit
        item.turnoverRate = [0, ] * (max_len - len(item.turnoverRate)) + item.turnoverRate
    return sectorList


def getHotSectorFullAnalysisInfo(data_type=""):
    '''
    根据top10的id，返回top10的sector对象
    :return:  list(sector)
    '''
    top_10_id = HotSector.getHotSectorID()
    # top_10_sectorInfoList = []
    if data_type == "day":
        top_10_sectorInfoList = SectorAnalysisDao.getSectorDayAnalysisList(top_10_id)
    elif data_type == "month":
        top_10_sectorInfoList = SectorAnalysisDao.getSectorMonthAnalysisList(top_10_id)
    elif data_type == "week":
        top_10_sectorInfoList = SectorAnalysisDao.getSectorWeekAnalysisList(top_10_id)
    else:
        top_10_sectorInfoList = SectorAnalysisDao.getSectorDayAnalysisList(top_10_id)
    return top_10_sectorInfoList


# 下面的函数用来处理请求
def getHotSectorAnalysisInfor(request):
    '''
    返回当前最热门版块信息 ： 转换了getHotSectorFullInfo() 返回的数据
    '''

    # 环境问题，真的没办法，浪费了几天时间，只能在这里用参数在这里转发到predict
    # predict_tag = str(request.GET.get("predict"))
    # if predict_tag == "True":
    #     # PredictTrend.sendPredictData(request)
    #     pass
    # else:

    data_type = request.GET.get("type")
    print("data_type:", data_type)
    top_10_sectorAnalysisInfoList = getHotSectorFullAnalysisInfo(data_type)
    top_10_sectorAnalysisInfoList = dataAlign(top_10_sectorAnalysisInfoList)
    data = {"status": 200, "dataName": "sectoranalysis", "recordTime": [], "sectorList": []}
    json_obj = data
    json_obj["recordTime"] = top_10_sectorAnalysisInfoList[0].recordTime
    for sector in top_10_sectorAnalysisInfoList:
        json_obj["sectorList"].append(json.loads(json.dumps(sector.__dict__)))

    return HttpResponse(json.dumps(json_obj))


if __name__ == "__main__":
    # hot_id = HotSector.getHotSectorID()
    # print(hot_id)
    # top_10_sectorAnalysisList = SectorAnalysisDao.getSectorDayAnalysisList(hot_id)
    # top_10_sectorAnalysisList = dataAlign(top_10_sectorAnalysisList)
    # for item in top_10_sectorAnalysisList:
    #     print(len(item.recordTime), " ", len(item.lastTrade))
    # print(len(top_10_sectorInfoList))
    pass
