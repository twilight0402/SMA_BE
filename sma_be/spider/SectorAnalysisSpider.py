import requests
import json
import numpy as np
from sma_be.sectorDao import DBUtil


def getDayAnalysis(sectorID: str, start="20190101", end="20220101"):
    kline_day = "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery17207924994156058143_1585709402318&secid=90.{}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg={}&end={}&_=1585709782237"
    url = kline_day.format(sectorID, start, end)

    response = requests.get(url)
    raw_data = response.text
    raw_data = raw_data[raw_data.index("(") + 1: raw_data.index(")")]

    data_json = json.loads(raw_data)
    kline_data = data_json["data"]['klines']

    sector_day_record = [day.strip().split(",") for day in kline_data]
    return np.array(sector_day_record)


def generateChangeRate_Amount(closePrice):
    '''根据收盘价计算涨跌幅和涨跌额'''
    changeRate = np.zeros(len(closePrice))      # 涨跌幅
    changeAmount = np.zeros(len(closePrice))    # 涨跌额

    for i in range(1, len(closePrice)):
        changeAmount[i] = (closePrice[i] - closePrice[i - 1])
        changeRate[i] = changeAmount[i] / closePrice[i - 1] * 100
    return changeAmount, changeRate


def saveSectorWeekDataList(sectorInfo, start='20190101', end='20220101'):
    kline_month = "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery17204904664961208407_1586056009415&secid=90.{}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=102&fqt=0&beg={}&end={}&_=1586057491061"
    for sectorID, sectorName in sectorInfo:
        url = kline_month.format(sectorID, start, end)

        response = requests.get(url)
        raw_data = response.text
        raw_data = raw_data[raw_data.index("(")+1: raw_data.index(")")]

        data_json = json.loads(raw_data)
        kline_data = data_json["data"]['klines']
        sector_day_record = np.array([day.strip().split(",") for day in kline_data])

        recordTime = sector_day_record[:, 0]        # 记录时间
        lastTrade = sector_day_record[:, 1]         # 最新价变动
        tradePrice = sector_day_record[:, 5]        # 成交额

        # 计算涨跌幅和涨跌额
        closePrice = np.array(sector_day_record[:, 1], dtype=float)     # 收盘价
        changeAmount, changeRate = generateChangeRate_Amount(closePrice)

        # 将数组转化为字符串
        recordTimeStr = ",".join([str(i) for i in recordTime])
        lastTradeStr = ",".join([str(i) for i in lastTrade])
        changeAmountStr = ",".join([str(i) for i in changeAmount])
        changeRateStr = ",".join([str(i) for i in changeRate])

        # print(recordTimeStr)

        # 入库
        conn = DBUtil.getConnection()
        cursor = conn.cursor()

        # 检查是否已经存在
        sql_query = "select * from sectorpredictioninfo_week where sectorID=%s"
        changelines = cursor.execute(sql_query, sectorID)
        if changelines != 0:
            # 存在就更新
            sql_update = "UPDATE sectorpredictioninfo_week SET recordTime=%s, lastTrade=%s, " \
                         "changeAmount=%s, changeRate=%s, totalCapit=%s, turnoverRate=%s WHERE sectorID=%s"
            cursor.execute(sql_update, (recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", "", sectorID))
        else:
            # 不存在就插入
            sql_insert = "INSERT INTO sectorpredictioninfo_week " \
                  "(sectorID, recordTime, lastTrade, changeAmount, changeRate, totalCapit, turnoverRate) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_insert, (sectorID, recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", ""))

        conn.commit()
    cursor.close()
    conn.close()


def saveSectorMonthDataList(sectorInfo, start='20190101', end='20220101'):
    kline_month = "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery17204904664961208407_1586056008500&secid=90.{}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=103&fqt=0&beg={}&end={}&_=1586056018617"

    for sectorID, sectorName in sectorInfo:
        url = kline_month.format(sectorID, start, end)

        response = requests.get(url)
        raw_data = response.text
        raw_data = raw_data[raw_data.index("(")+1: raw_data.index(")")]

        data_json = json.loads(raw_data)
        kline_data = data_json["data"]['klines']
        sector_day_record = np.array([day.strip().split(",") for day in kline_data])

        recordTime = sector_day_record[:, 0]        # 记录时间
        lastTrade = sector_day_record[:, 1]         # 最新价变动
        tradePrice = sector_day_record[:, 5]        # 成交额

        # 计算涨跌幅和涨跌额
        closePrice = np.array(sector_day_record[:, 1], dtype=float)     # 收盘价
        changeAmount, changeRate = generateChangeRate_Amount(closePrice)

        # 将数组转化为字符串
        recordTimeStr = ",".join([str(i) for i in recordTime])
        lastTradeStr = ",".join([str(i) for i in lastTrade])
        changeAmountStr = ",".join([str(i) for i in changeAmount])
        changeRateStr = ",".join([str(i) for i in changeRate])

        # print(recordTimeStr)

        # 入库
        conn = DBUtil.getConnection()
        cursor = conn.cursor()

        # 检查是否已经存在
        sql_query = "select * from sectorpredictioninfo_month where sectorID=%s"
        changelines = cursor.execute(sql_query, sectorID)
        if changelines != 0:
            # 存在就更新
            sql_update = "UPDATE sectorpredictioninfo_month SET recordTime=%s, lastTrade=%s, " \
                         "changeAmount=%s, changeRate=%s, totalCapit=%s, turnoverRate=%s WHERE sectorID=%s"
            cursor.execute(sql_update, (recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", "", sectorID))
        else:
            # 不存在就插入
            sql_insert = "INSERT INTO sectorpredictioninfo_month " \
                  "(sectorID, recordTime, lastTrade, changeAmount, changeRate, totalCapit, turnoverRate) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_insert, (sectorID, recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", ""))

        conn.commit()
    cursor.close()
    conn.close()


def saveSectorDayDataList(sectorInfo, start='20190101', end='20220101'):
    '''给定一个(id, name)的元素的数组，查找对应的kline数据并保存到数据库'''
    kline_day = "http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery17207924994156058143_1585709402318&secid=90.{}&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=101&fqt=0&beg={}&end={}&_=1585709782237"

    for sectorID, sectorName in sectorInfo:
        url = kline_day.format(sectorID, start, end)

        response = requests.get(url)
        raw_data = response.text
        raw_data = raw_data[raw_data.index("(")+1: raw_data.index(")")]

        data_json = json.loads(raw_data)
        kline_data = data_json["data"]['klines']
        sector_day_record = np.array([day.strip().split(",") for day in kline_data])

        recordTime = sector_day_record[:, 0]        # 记录时间
        lastTrade = sector_day_record[:, 1]         # 最新价变动
        tradePrice = sector_day_record[:, 5]        # 成交额

        # 计算涨跌幅和涨跌额
        closePrice = np.array(sector_day_record[:, 1], dtype=float)     # 收盘价
        changeAmount, changeRate = generateChangeRate_Amount(closePrice)

        # 将数组转化为字符串
        recordTimeStr = ",".join([str(i) for i in recordTime])
        lastTradeStr = ",".join([str(i) for i in lastTrade])
        changeAmountStr = ",".join([str(i) for i in changeAmount])
        changeRateStr = ",".join([str(i) for i in changeRate])

        # print(recordTimeStr)

        # 入库
        conn = DBUtil.getConnection()
        cursor = conn.cursor()

        # 检查是否已经存在
        sql_query = "select * from sectorpredictioninfo where sectorID=%s"
        changelines = cursor.execute(sql_query, sectorID)
        if changelines != 0:
            # 存在就更新
            sql_update = "UPDATE sectorpredictioninfo SET recordTime=%s, lastTrade=%s, " \
                         "changeAmount=%s, changeRate=%s, totalCapit=%s, turnoverRate=%s WHERE sectorID=%s"
            cursor.execute(sql_update, (recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", "", sectorID))
        else:
            # 不存在就插入
            sql_insert = "INSERT INTO sectorpredictioninfo " \
                  "(sectorID, recordTime, lastTrade, changeAmount, changeRate, totalCapit, turnoverRate) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql_insert, (sectorID, recordTimeStr, lastTradeStr, changeAmountStr, changeRateStr, "", ""))

        conn.commit()
    cursor.close()
    conn.close()


def updateSectorData():
    '''
    从sectorinfo表中读取所有版块的id和name，然后爬取他们的kline数据
    :return: NULL
    '''
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_query = "SELECT sectorID, sectorName FROM sectorinfo"
    amount = cursor.execute(sql_query)

    if amount == 0:
        cursor.close()
        conn.close()
        return

    sectorList = cursor.fetchall()
    saveSectorDayDataList(sectorList, start="20200101", end="22000101")
    saveSectorMonthDataList(sectorList, start="20190101", end="22000101")
    saveSectorWeekDataList(sectorList, start="20190101", end="22000101")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    updateSectorData()
