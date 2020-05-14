from django.http import HttpResponse
from sma_be.sectorDao import DBUtil
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import json


def getUserInfo(username: str):
    sql_query = "select username , password from user where username=%s;"
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    amount = cursor.execute(sql_query, username)
    if amount == 0:
        return None
    userInfo = cursor.fetchone()

    cursor.close()
    conn.close()
    return userInfo


def saveUserInfo(username: str, password: str, email: str):
    sql_query = "select username from user where username=%s;"
    conn = DBUtil.getConnection()
    cursor = conn.cursor()
    amount = cursor.execute(sql_query, username)
    if amount != 0:
        return False
    sql_insert = "INSERT INTO user(username, password, email) VALUES(%s, %s, %s);"
    cursor.execute(sql_insert, (username, password, email))

    conn.commit()
    cursor.close()
    conn.close()
    return True


# 搞定
def checkUserInfo(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    keepLive = request.GET.get("keepLive")
    response=None

    cookie = request.COOKIES.get("username")
    # print("###cookie:", cookie)
    # print(keepLive == "true")

    userInfo = getUserInfo(username)
    if userInfo is None or userInfo[1] != password.strip():
        res = {"check": 0}
        response = HttpResponse(json.dumps(res))
    else:
        res = {"check": 1}
        response = HttpResponse(json.dumps(res))
        if keepLive == "true":
            response.set_cookie("username", username)
            response.set_cookie("password", password)

    return response


def register(request):
    '''用户注册'''
    username = request.GET.get("username")
    password = request.GET.get("password")
    email = request.GET.get("email")

    res = saveUserInfo(username, password, email)
    if res:
        response_msg = {"status": 1, "msg": "注册成功"}
    else:
        response_msg = {"status": 0, "msg": "用户名已存在"}

    return HttpResponse(json.dumps(response_msg))
