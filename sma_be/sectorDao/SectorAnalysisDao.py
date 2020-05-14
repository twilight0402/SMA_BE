# import pymysql
from sma_be.sectorDao import DBUtil
from sma_be.entity.entity import SectorAnalysis
from sma_be.entity.entity import SectorInfo


def getAllSectorID():
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT sectorID FROM sectorinfo;"

    cursor.execute(sql_query)
    idList = cursor.fetchall()
    idList = [item[0] for item in idList]
    return idList


def getSectorInfoListByIDList(id_list):
    '''
    查询sectorinfo表
    查询idlist中对应的版块的最新信息，如果list为空，那么返回所有版块的信息
    '''
    sql_query = "SELECT sectorID, sectorName, sectorType.sectorTypeName,  recordTime, lastTrade, changeAmount, " \
                "changeRate, totalCapit, turnoverRate, riseNumber, fallNumber " \
                "FROM sectorinfo JOIN sectorType " \
                "ON sectorinfo.sectorType=sectorType.sectorTypeID " \
                "WHERE sectorinfo.sectorID=%s;"
    conn = DBUtil.getConnection()
    cursor = conn.cursor()

    sectorInfoTupleList = []
    sectorInfoList = []

    if 0 == len(id_list):
        sql_query = sql_query[:sql_query.index("WHERE")] + ";"
        amount = cursor.execute(sql_query)
        sectorInfoTupleList = cursor.fetchall()
    else:
        amount = cursor.executemany(sql_query, id_list)
        sectorInfoTupleList = DBUtil.query_many(sql_query, id_list)

    for item in sectorInfoTupleList:
        sectorInfo = SectorInfo()
        sectorInfo.sectorID = item[0]
        sectorInfo.sectorName = item[1]
        sectorInfo.sectorType = item[2]
        sectorInfo.recordTime = str(item[3])
        sectorInfo.lastTrade = item[4]
        sectorInfo.changeAmount = item[5]
        sectorInfo.changeRate = item[6]
        sectorInfo.totalCapit = item[7]
        sectorInfo.turnoverRate = item[8]
        sectorInfo.riseNumber = item[9]
        sectorInfo.fallNumber = item[10]
        sectorInfoList.append(sectorInfo)

    cursor.close()
    conn.close()
    return sectorInfoList


def getSectorDayAnalysisList(id_list):
    '''
    查询sectorpredict表
    返回list中的板块对应的kline数据，如果list为空，则返回所有数据
    返回所有版块的kline数据
    '''
    # db
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT sectorID, sectorName FROM sectorinfo WHERE sectorID=%s;"

    # 查找 list(tuple(id, name))
    sectorDayAnalysisTupleList = []
    sectorAnalysisList = []

    if 0 == len(id_list):
        sql_query = sql_query[: sql_query.index("WHERE")]
        cursor.execute(sql_query)
        sectorDayAnalysisTupleList = cursor.fetchall()
    else:
        sectorDayAnalysisTupleList = DBUtil.query_many(sql_query, id_list)

    # 根据 list(tuple(id, name)) 查询k线数据
    for sectorID, sectorName in sectorDayAnalysisTupleList:
        sql_query = "SELECT * from sectorpredictioninfo WHERE sectorID=%s"
        res_number = cursor.execute(sql_query, sectorID)

        if 0 != res_number:
            sectorData = cursor.fetchone()
            sectorAnalysis = SectorAnalysis()
            sectorAnalysis.sectorID = sectorData[0]
            sectorAnalysis.sectorName = sectorName
            sectorAnalysis.recordTime = sectorData[1].strip().split(",")
            sectorAnalysis.lastTrade = [round(float(x), 2) for x in sectorData[2].strip().split(",") if x != ""]
            sectorAnalysis.changeAmount = [round(float(x)) for x in sectorData[3].strip().split(",") if x != ""]
            sectorAnalysis.changeRate = [round(float(x)) for x in sectorData[4].strip().split(",") if x != ""]
            sectorAnalysis.totalCapit = [round(float(x)) for x in sectorData[5].strip().split(",") if x != ""]
            sectorAnalysis.turnoverRate = [round(float(x)) for x in sectorData[6].strip().split(",") if x != ""]
            sectorAnalysisList.append(sectorAnalysis)

    cursor.close()
    conn.close()
    return sectorAnalysisList


def getSectorMonthAnalysisList(id_list):
    '''
    查询sectorpredict表
    返回list中的板块对应的kline数据，如果list为空，则返回所有数据
    返回所有版块的kline数据
    '''
    # db
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT sectorID, sectorName FROM sectorinfo WHERE sectorID=%s;"

    # 查找 list(tuple(id, name))
    sectorDayAnalysisTupleList = []
    sectorAnalysisList = []

    if 0 == len(id_list):
        sql_query = sql_query[: sql_query.index("WHERE")]
        cursor.execute(sql_query)
        sectorDayAnalysisTupleList = cursor.fetchall()
    else:
        sectorDayAnalysisTupleList = DBUtil.query_many(sql_query, id_list)

    # 根据 list(tuple(id, name)) 查询k线数据
    for sectorID, sectorName in sectorDayAnalysisTupleList:
        sql_query = "SELECT * from sectorpredictioninfo_month WHERE sectorID=%s"
        res_number = cursor.execute(sql_query, sectorID)

        if 0 != res_number:
            sectorData = cursor.fetchone()
            sectorAnalysis = SectorAnalysis()
            sectorAnalysis.sectorID = sectorData[0]
            sectorAnalysis.sectorName = sectorName
            sectorAnalysis.recordTime = sectorData[1].strip().split(",")
            sectorAnalysis.lastTrade = [round(float(x), 2) for x in sectorData[2].strip().split(",") if x != ""]
            sectorAnalysis.changeAmount = [round(float(x)) for x in sectorData[3].strip().split(",") if x != ""]
            sectorAnalysis.changeRate = [round(float(x)) for x in sectorData[4].strip().split(",") if x != ""]
            sectorAnalysis.totalCapit = [round(float(x)) for x in sectorData[5].strip().split(",") if x != ""]
            sectorAnalysis.turnoverRate = [round(float(x)) for x in sectorData[6].strip().split(",") if x != ""]
            sectorAnalysisList.append(sectorAnalysis)

    cursor.close()
    conn.close()
    return sectorAnalysisList



def getSectorWeekAnalysisList(id_list):
    '''
    查询sectorpredict表
    返回list中的板块对应的kline数据，如果list为空，则返回所有数据
    返回所有版块的kline数据
    '''
    # db
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT sectorID, sectorName FROM sectorinfo WHERE sectorID=%s;"

    # 查找 list(tuple(id, name))
    sectorDayAnalysisTupleList = []
    sectorAnalysisList = []

    if 0 == len(id_list):
        sql_query = sql_query[: sql_query.index("WHERE")]
        cursor.execute(sql_query)
        sectorDayAnalysisTupleList = cursor.fetchall()
    else:
        sectorDayAnalysisTupleList = DBUtil.query_many(sql_query, id_list)

    # 根据 list(tuple(id, name)) 查询k线数据
    for sectorID, sectorName in sectorDayAnalysisTupleList:
        sql_query = "SELECT * from sectorpredictioninfo_week WHERE sectorID=%s"
        res_number = cursor.execute(sql_query, sectorID)

        if 0 != res_number:
            sectorData = cursor.fetchone()
            sectorAnalysis = SectorAnalysis()
            sectorAnalysis.sectorID = sectorData[0]
            sectorAnalysis.sectorName = sectorName
            sectorAnalysis.recordTime = sectorData[1].strip().split(",")
            sectorAnalysis.lastTrade = [round(float(x), 2) for x in sectorData[2].strip().split(",") if x != ""]
            sectorAnalysis.changeAmount = [round(float(x)) for x in sectorData[3].strip().split(",") if x != ""]
            sectorAnalysis.changeRate = [round(float(x)) for x in sectorData[4].strip().split(",") if x != ""]
            sectorAnalysis.totalCapit = [round(float(x)) for x in sectorData[5].strip().split(",") if x != ""]
            sectorAnalysis.turnoverRate = [round(float(x)) for x in sectorData[6].strip().split(",") if x != ""]
            sectorAnalysisList.append(sectorAnalysis)

    cursor.close()
    conn.close()
    return sectorAnalysisList



def getSectorDayAnalysis(sectorID: str, sectorName: str):
    '''
    根据id获取某一天的kline数据
    '''
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT * from sectorpredictioninfo WHERE sectorID=%s"
    res_number = cursor.execute(sql_query, sectorID)

    if 0 != res_number:
        sectorData = cursor.fetchone()

    sector = SectorAnalysis()
    sector.sectorID = sectorData[0]
    sector.sectorName = sectorName
    sector.recordTime = sectorData[1].strip().split(",")
    sector.lastTrade = [float(x) for x in sectorData[2].strip().split(",")]
    sector.changeAmount = [float(x) for x in sectorData[3].strip().split(",")]
    sector.changeRate = [float(x) for x in sectorData[4].strip().split(",")]
    sector.totalCapit = [float(x) for x in sectorData[5].strip().split(",")]
    sector.turnoverRate = [float(x) for x in sectorData[6].strip().split(",")]

    cursor.close()
    conn.close()
    return sector


if __name__ == "__main__":
    id_list = ['BK0908', 'BK0732', 'BK0902', 'BK0547', 'BK0916', 'BK0890', 'BK0891', 'BK0734', 'BK0703', 'BK0706']
    res = getSectorWeekAnalysisList(id_list)
    print(res)