import pymysql


def getConnection():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='shareanalysis')
    return conn


def query_many(sql, params):
    '''
    根据params给的参数，查询所有结果
    (坑：executemany不能执行查询操作不能返回所有结果)
    :param sql:
    :param params:
    :return: list(tuple(key1, key2,...))
    '''
    conn = getConnection()
    cursor = conn.cursor()
    res = []
    for param in params:
        amount = cursor.execute(sql, param)
        if amount != 0:
            res.append(cursor.fetchone())

    cursor.close()
    conn.close()
    return res
