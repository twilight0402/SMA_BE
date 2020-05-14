from django.http import HttpResponse
from django.http.response import JsonResponse
from sma_be.sectorservice import SectorAnalysis
from sma_be.sectorDao import SectorAnalysisDao
import json


def getHotSectorID():
    '''
    返回top10的id
    根据最新数据(sectorInfo)排序的结果
    :return:  top_10_id
    '''
    sectorDayList = SectorAnalysisDao.getSectorInfoListByIDList([])
    id_changeRate = [(sector.sectorID, float(sector.changeRate)) for sector in sectorDayList]
    id_changeRate_sorted = sorted(id_changeRate, key=lambda x: x[1], reverse=True)
    top_10_id = [x[0] for x in id_changeRate_sorted[:10]]
    return top_10_id


def getHotSectorFullInfo():
    '''
    根据top10的id，返回top10的sector对象
    :return:  list(sector)
    '''
    top_10_id = getHotSectorID()
    top_10_sectorInfoList = SectorAnalysisDao.getSectorInfoListByIDList(top_10_id)
    return top_10_sectorInfoList


# 下面的函数用来处理请求
def getHotSectorInfor(request):
    '''
    返回当前最热门版块信息 ： 转换了getHotSectorFullInfo() 返回的数据
    '''
    top_10_sectorInfoList = getHotSectorFullInfo()
    data = {"status": 200, "dataName": "hotsectorinfo", "hotSectorList": []}
    json_obj = json.loads(json.dumps(data))
    for sector in top_10_sectorInfoList:
        json_obj["hotSectorList"].append(json.loads(json.dumps(sector.__dict__)))

    return HttpResponse(json.dumps(json_obj))


if __name__ == "__main__":
    id_list = getHotSectorID()
    print(id_list)
