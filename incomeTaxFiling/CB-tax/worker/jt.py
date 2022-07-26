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
        'Host': '114.55.27.34:48014'
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
        purl = 'http://114.55.27.34:48014/api/saas/tax/returnReceipt/operate'
        data = {
              "fileName": "个税(工资薪金所得)",
              "fileUrl": zzz,
              "status": 1,
              "taxDeclarationId": id,
              "taxName": "个税(工资薪金所得)",
              "ip_addr": ip
            }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa


# 密码错误
def mmcw(id,dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '114.55.27.34:48014'
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
        purl = 'http://114.55.27.34:48014/api/saas/tax/returnReceipt/operate'
        data = {
              "exceptionCause": "个税账号或密码错误",
              "fileName": "个税(工资薪金所得)",
              "fileUrl": zzz,
              "status": 0,
              "taxDeclarationId": id,
              "taxName": "个税(工资薪金所得)"
            }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa


# 报税失败，其他错误
def jgcw(id,dz,jg):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '114.55.27.34:48014'
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
        purl = 'http://114.55.27.34:48014/api/saas/tax/returnReceipt/operate'
        data = {
              "exceptionCause":  "个税错误: "+jg,
              "fileName": "个税(工资薪金所得)",
              "fileUrl": zzz,
              "status": 0,
              "taxDeclarationId": id,
              "taxName": "个税(工资薪金所得)"
            }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa


# 未知错误（程序卡滞/报税时，公司本身问题）
def wzcw(id,dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '47.111.176.38:48016'
    }
    headers2 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': '114.55.27.34:48014'
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
        purl = 'http://114.55.27.34:48014/api/saas/tax/returnReceipt/operate'
        data = {
              "exceptionCause":  "个税未知错误",
              "fileName": "个税(工资薪金所得)",
              "fileUrl": zzz,
              "status": 0,
              "taxDeclarationId": id,
              "taxName": "个税(工资薪金所得)"
            }
        data = json.dumps(data)
        aaa = requests.post(url = purl,data=data,headers=headers2).text
        return aaa

