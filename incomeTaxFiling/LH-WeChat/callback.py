# coding: utf-8
# 将数据返回给回调中心

# -*- coding: utf-8 -*-
import requests
import socket
import base64
import json


# 获取本机IP
def get_host_ip():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.connect(('114.114.114.114', 80))
    ip_addr = sk.getsockname()[0]
    return ip_addr

headers2 = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Host': '47.99.96.186:38059'
}
purl = "http://47.99.96.186:38059/api/wechat/callback"

def error(taskId,status,msg):

    data = {
        "taskId": int(taskId),
        "status": int(status),
        "msg": str(msg),
    }

    data = json.dumps(data)
    aaa = requests.post(url=purl, data=data, headers=headers2).text
    return aaa


# 报税成功分为（正常成功/重复报税）
def check_wechat(task_id, status, wechat_status, username):
    if status == 200:
        msg = "success"
        data = {
            "taskId": int(task_id),
            "status": int(status),
            "msg": str(msg),
            "botWechatStatus": int(wechat_status),
            "botWechatUsername": str(username),
        }

        data = json.dumps(data)
        aaa = requests.post(url=purl, data=data, headers=headers2).text
        return aaa

    elif status == 400:
        msg = "错误1"
        error(task_id,status,msg)


def login(task_id,status,dz):
    if status == 200:
        msg = "success"
        with open(dz, "rb") as f:
            base64_data = base64.b64encode(f.read())
            base64_data = str(base64_data).split("'")[1]

        data = {
            "taskId": int(task_id),
            "base64Url": str(base64_data),
            "status": int(status),
            "msg": str(msg),
        }

        data = json.dumps(data)
        aaa = requests.post(url=purl, data=data, headers=headers2).text
        return aaa

    elif status == 70018:
        msg = "登录超时！！"
        error(task_id, status, msg)

    elif status == 70021:
        status = 200
        msg = "success"
        data = {
            "taskId": int(task_id),
            "status": int(status),
            "msg": str(msg),
            "isSuccess":1
        }
        data = json.dumps(data)
        aaa = requests.post(url=purl, data=data, headers=headers2).text
        return aaa


def logout(task_id, status):
    if status == 200:
        msg = "success"
        data = {
            "taskId": int(task_id),
            "status": int(status),
            "msg": str(msg),
        }

        data = json.dumps(data)
        aaa = requests.post(url=purl, data=data, headers=headers2).text
        return aaa

    elif status == 400:
        msg = "错误1"
        error(task_id, status, msg)



def add(task_id, status,add_result):
    if status == 200:
        msg = "success"
        data = {
            "taskId": int(task_id),
            "status": int(status),
            "msg": str(msg),
            "addResult": str(add_result)
        }

        data = json.dumps(data)
        aaa = requests.post(url=purl, data=data, headers=headers2).text
        return aaa

    elif status == 400:
        msg = "错误1"
        error(task_id, status, msg)

def base():
    with open(r"D:\RPA\zl-rpa\incomeTaxFiling\LH-WeChat\645423.png", "rb") as f:
        base64_data = base64.b64encode(f.read())
        print(base64_data)
        base64_data = str(base64_data).split("'")[1]
        print(base64_data)

if __name__ == '__main__':
    pass
    base()