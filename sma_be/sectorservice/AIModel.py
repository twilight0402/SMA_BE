import torch
from torch import nn
import numpy as np
import pandas as pd
from sma_be.spider import SectorAnalysisSpider
from sma_be.sectorDao import SectorAnalysisDao
from sma_be.sectorDao import DBUtil

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
seq = 14
epoch = 10000
MODEL_PATH = "./model/{}.data"


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=32, num_layers=1, batch_first=True)
        # 输入格式是1，输出隐藏层大小是32，对于序列比较短的数据num_layers不要设置大，否则效果会变差
        # 原来的输入格式是：(seq, batch, shape)，设置batch_first=True以后，输入格式就可以改为：(batch, seq, shape)，更符合平常使用的习惯
        self.linear = nn.Linear(32*seq, 1)

    def forward(self, x):
        x, (h, c) = self.lstm(x)
        x = x.reshape(-1, 32*seq)
        x = self.linear(x)
        return x


def get_train_test_data(sectorID: str, rate=0.75, item="close"):
    '''
    按照比例划分，不打乱数据
    :param rate:
    :return:
    :item: 训练属性
    '''
    day_data = SectorAnalysisSpider.getDayAnalysis(sectorID)
    day_data = pd.DataFrame(day_data)

    feature_data = pd.DataFrame()
    feature_data["close"] = day_data[2]

    for i in range(1, 15):
        feature_data["close-" + str(i) + "d"] = feature_data[item].shift(periods=i, axis=0)

    feature_data.dropna(inplace=True)
    x = feature_data.values[:, 1:]
    y = feature_data.values[:, 0]
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    length = len(x)
    index = int(length * rate)

    train_x = x[:index]
    train_y = y[:index]
    test_x = x[index:]
    test_y = y[index:]

    #     train_x, test_x, train_y, test_y = train_test_split(x, y)
    return train_x, test_x, train_y, test_y, y


def train(sectorID:str, item="close"):
    '''训练模型并保存'''
    # 训练数据，测试数据和完整序列
    train_x, test_x, train_y, test_y, data = get_train_test_data(sectorID, 1, item)
    train_x = train_x / 1000
    test_x = test_x / 1000
    train_y = train_y / 1000
    test_y = test_y / 1000

    # 分训练和测试集
    train_x = (torch.tensor(train_x).float()).reshape(-1, seq, 1).to(device)
    train_y = (torch.tensor(train_y).float()).reshape(-1, 1).to(device)

    test_x = (torch.tensor(test_x).float()).reshape(-1, seq, 1).to(device)
    test_y = (torch.tensor(test_y).float()).reshape(-1, 1).to(device)

    model = Net().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fun = nn.MSELoss()

    model.train()
    for item in range(epoch):
        output = model(train_x)
        loss = loss_fun(output, train_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    torch.save(model.state_dict(), MODEL_PATH.format(sectorID))
    return model


def getModel(sectorID):
    '''读取模型'''
    model = Net().to(device)
    model.load_state_dict(torch.load(MODEL_PATH.format(sectorID)))
    return model


def getPredictData(sectorID: str):
    '''用模型计算预测数据'''
    sql_query = "select data from predictresult where sectorID=%s;"
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    amount = cursor.execute(sql_query, sectorID)
    if amount != 0:
        res = cursor.fetchone()

    return [float(item) for item in res[0].split(",")]


# 更新函数的封装
def trainAllSector():
    idList = SectorAnalysisDao.getAllSectorID()

    index = 0
    for sectorID in idList:
        index += 1
        train(sectorID)
        if index % 10 == 0:
            print(index)


def saveAllPredictData():
    sectorIDList = SectorAnalysisDao.getAllSectorID()
    predictData = []
    for sectorID in sectorIDList:
        model = getModel(sectorID)
        _, _, _, _, data = get_train_test_data(sectorID, rate=1)
        lastData = data[-14:]
        lastData = lastData / 1000
        res = []

        for i in range(7):
            temp = model(torch.tensor(lastData.reshape(-1, 14, 1)).float().to(device))
            for i in range(1, len(lastData) - 1):
                lastData[i] = lastData[i + 1]
            lastData[-1] = temp
            res.append(temp)
        res = [round(item.cpu().data.numpy()[0][0] * 1000, 2) for item in res]
        predictData.append(res)

    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    sql_update = "UPDATE predictresult set data=%s WHERE sectorID=%s"

    for index in range(len(predictData)):
        cursor.execute(sql_update, (",".join([str(i) for i in predictData[index]]), sectorIDList[index]))
        conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    # train("BK0438")
    # a = [1,2,3]
    # print(",".join([str(i) for i in a]))
    # res = getPredictData("BK0438")
    # print(res)
    # saveAllPredictData()
    print(getPredictData("BK0160"))
    # trainAllSector()
    # for sectorID in ['BK0420', 'BK0421', 'BK0422', 'BK0424', 'BK0425', 'BK0427']:
    #     res = getPredictData(sectorID)
    #     print(res)

    # ['BK0420', 'BK0421', 'BK0422', 'BK0424', 'BK0425', 'BK0427']
    # idList = SectorAnalysisDao.getAllSectorID()
    # print(idList)

