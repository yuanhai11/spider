# coding: utf-8
# 将数据返回给回调中心

#-*- coding: utf-8 -*-
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

# 报税成功分为（正常成功/重复报税）
def cg(id,dz,ip='None'):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.99.96.186:38059'
    }

    with open(dz,"rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data).split("'")[1]
        url = "http://47.111.176.38:48016/oss/upload"
        data = {"imgContent":base64_data}
        data = json.dumps(data)
        aaa = requests.post(url = url,data=data,headers=headers1).text
        aaa = json.loads(aaa)
        zzz = aaa['data']['imageUrl']
        purl = 'http://47.99.96.186:38059/api/task/taskProcess'
        data = {
              "accessUrl": zzz,
              "state": 1,
              "taskId": id,
              "sourceOssStorage": ip
            }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa

# 报税错误 （密码错误、其余未知错误）
def wzcw(id,dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.99.96.186:38059'
    }
    with open(dz,"rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data).split("'")[1]
        url = "http://47.111.176.38:48016/oss/upload"
        data = {"imgContent":base64_data}
        data = json.dumps(data)
        aaa = requests.post(url = url,data=data,headers=headers1).text
        aaa = json.loads(aaa)
        zzz = aaa['data']['imageUrl']
        purl = 'http://47.99.96.186:38059/api/task/taskProcess'
        data = {
            "accessUrl": zzz,
            "state": 0,
            "taskId": id,
            "exceptionCause":'未知错误，原因如下：1.页面卡顿，2.客户端升级...'
        }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa

def mmcw(id,dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.99.96.186:38059'
    }
    with open(dz,"rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data).split("'")[1]
        url = "http://47.111.176.38:48016/oss/upload"
        data = {"imgContent":base64_data}
        data = json.dumps(data)
        aaa = requests.post(url = url,data=data,headers=headers1).text
        aaa = json.loads(aaa)
        zzz = aaa['data']['imageUrl']
        purl = 'http://47.99.96.186:38059/api/task/taskProcess'
        data = {
            "accessUrl": zzz,
            "state": 0,
            "taskId": id,
            'exceptionCause':"个税账号或密码错误"
        }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa



if __name__ == '__main__':
    wzcw('1111',r"D:\RPA\zl-rpa\incomeTaxFiling\a.png")


