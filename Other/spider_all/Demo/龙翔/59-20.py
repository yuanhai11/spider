import json
import random
import re
import threading
import time
#pip3 install requests
import urllib
from urllib import parse

import requests
from urllib.parse import urlencode, unquote

# starttime = 1652115839000  #开始时间戳 13位 网址：https://tool.lu/timestamp/  59:59
starttime = 1654497080510  #开始时间戳 13位 网址：https://tool.lu/timestamp/  59:59
# cookie = 'pt_key=AAJifhwDADACFrVe_bjjL4KMDB1Oidovpld-EloK_OSMYQO4u21jnl3ncwbHhKHiW_Ok0alWusw;pt_pin=jd_xwzqyqWOxTTa;'
cookie = 'pin=%E7%B2%BE%E7%81%B5%E8%80%B3%E6%9C%B5%E5%85%88%E7%94%9F;wskey=AAJiiwWzAFA_v3CaIzj2yIdjZUdw3RoIgYpEpk24-OD-h0YlSIiv7zqnXfI_fTdYNEFgmPsa_o4bWxMwa36Z-N4woHxfe8cy9RZc3GquQRH6gLn9PWPniQ;whwswswws=JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp~n9zx+EhUkbynGit+ZWEFz0+Cp4cn+G9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN;unionwsws={devicefinger:eidAf88f8122e6sfjj96vPLKTtiORkUkZ2AHKo4/fDrdfe+kkeIKo5PX3AXE+GtigSqzU0kxK7ewujreKnC5QU57qV+QkNzrHqlEUg/89pNKdDtykeZr,jmafinger:JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp~n9zx+EhUkbynGit+ZWEFz0+Cp4cn+G9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN};'

range_n = 2  # 4个不同链接  8个线程 5/6
range_sleep = 0.25  # 间隔时间
delay_time = 0.4

#辅助参数
atime = 0
re_body = re.compile(r'body=.*?&')

COMMON_PARAMS = {
        'clientVersion': '11.0.2',
        'build': '97565',
        'client': 'android',
        'd_brand': 'Xiaomi',
        'd_model': '2014813',
        'osVersion': '5.1.1',
        'screen': '1280*720',
        'partner': 'jingdong',
        'harmonyOs': '0',
        'uemps': '0 - 2',
        'ef': '1',
        'ext': '{"prstate":"0","pvcStu":"1"}',
        'bef': '1',
        'sdkVersion': '28',
        'lang': 'zh_CN',
        'area': '',
        'networkType': 'wifi'
    }

def get_sign_api(functionId, body):
    sign_api = 'http://127.0.0.1:9000/jd/sign'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    body = json.dumps(body, ensure_ascii=False)
    print(urlencode(body))
    data = {
        'functionId': functionId,
        'body': parse.urlencode(str(body).encode("UTF-8")),
    }
    try:
        res = requests.post(url=sign_api, headers=headers, data=data, timeout=30).json()
        if res['code'] == 200:
            return res.get('data')
        else:
            print(res['msg'])
            return -1
    except:
        return -1


#潘达  https://api-jds-codes-zoopanda.doc.coding.io/#bef6470ec68104fdc926fce8b5d17b82
def get_sign_api1(functionId, body):
    sign_api = 'http://api.jds.codes/jd/sign'
    jdPandaToken = ''
    headers = {
        'Accept': '*/*',
        "accept-encoding": "gzip, deflate, br",
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + jdPandaToken
    }
    print(body)
    exit()
    data = {
        'fn': functionId,
        'body': body,
    }
    res = requests.post(url=sign_api, headers=headers, json=data, timeout=30).json()
    if res['code'] == 200:
        return res['data']
    else:
        print(res['msg'])
        return -1




def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)

def __add_params(url, query_params=None):
    if query_params is None:
        query_params = {}
    params = parse.urlencode(query_params)
    if not url.__contains__('?'):
        url = url + '?'

    if url.endswith('?') or url.endswith('&'):
        url = url + params
    else:
        url = url + '&' + params
    return url

def getCcFeedInfo(cookie):
    body = {
        "categoryId": 118,
        "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
        "eid": "eidAf88f8122e6sfjj96vPLKTtiORkUkZ2AHKo4/fDrdfe+kkeIKo5PX3AXE+GtigSqzU0kxK7ewujreKnC5QU57qV+QkNzrHqlEUg/89pNKdDtykeZr",
        "globalLat": "0e46e12a7ead1c2b7df0929dd63927ca",
        "globalLng": "7baec0c500a5f9e539a2cb1699e45cbd",
        "lat": "08f8d0ab437c440a5c6e31e582f4ee25",
        "lng": "db954ffe32435cb6939cf5973ed7e91b",
        "monitorRefer": "appClient",
        "monitorSource": "ccfeed_android_index_feed",
        "pageClickKey": "Coupons_GetCenter",
        "pageNum": 1,
        "pageSize": 20,
        "shshshfpb": "JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp~n9zx+EhUkbynGit+ZWEFz0+Cp4cn+G9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN"
    }
    signRes = get_sign_api('getCcFeedInfo', body) #st sv sign
    if signRes == -1:
        return -1
    else:
        # params = signRes['sign']
        # functionId = signRes['functionId']
        # body = res['resbody']
        # body1 = re_body.findall(params)[0]
        # params = params.replace(body1, '')
        # url = f'https://api.m.jd.com/client.action?functionId={functionId}&' + params
        # # print(url)
        # headers = {
        #     "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        # }
        # res = requests.post(url=url, headers=headers, data=body, timeout=30).json()

        # ep = signRes['ep'] + ",\"ciphertype\":5}"
        # params = {
        #     'clientVersion': '11.0.2',
        #     'client': 'android',
        #     'ef': '1',
        #     'ep': str(ep),
        #     'st': signRes['st'],
        #     'sign': signRes['sign'],
        #     'sv': signRes['sv']
        # }
        # headers = {
        #     "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        # }
        # url = 'https://api.m.jd.com/client.action?functionId=getCcFeedInfo'
        # jd_url = __add_params(url, params)
        # data = "body=%7B%22categoryId%22%3A118%2C%22childActivityUrl%22%3A%22openapp.jdmobile%3A%2F%2Fvirtual%3Fparams%3D%7B%5C%22category%5C%22%3A%5C%22jump%5C%22%2C%5C%22des%5C%22%3A%5C%22couponCenter%5C%22%7D%22%2C%22eid%22%3A%22eidAf88f8122e6sfjj96vPLKTtiORkUkZ2AHKo4%2FfDrdfe%2BkkeIKo5PX3AXE%2BGtigSqzU0kxK7ewujreKnC5QU57qV%2BQkNzrHqlEUg%2F89pNKdDtykeZr%22%2C%22globalLat%22%3A%220e46e12a7ead1c2b7df0929dd63927ca%22%2C%22globalLng%22%3A%227baec0c500a5f9e539a2cb1699e45cbd%22%2C%22lat%22%3A%2208f8d0ab437c440a5c6e31e582f4ee25%22%2C%22lng%22%3A%22db954ffe32435cb6939cf5973ed7e91b%22%2C%22monitorRefer%22%3A%22appClient%22%2C%22monitorSource%22%3A%22ccfeed_android_index_feed%22%2C%22pageClickKey%22%3A%22Coupons_GetCenter%22%2C%22pageNum%22%3A1%2C%22pageSize%22%3A20%2C%22shshshfpb%22%3A%22JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp%7En9zx%2BEhUkbynGit%2BZWEFz0%2BCp4cn%2BG9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN%22%7D&"
        # res = requests.request("POST", jd_url, headers=headers, data=data, verify=False).json()


        functionId = signRes['functionId']
        params = signRes['convertUrlNew']
        index1 = "body"
        index2 = "&"
        a = params.index(index1)
        b = params.index(index2, params.index(index1))
        params = params[:a] + params[b + 1:]

        # url = 'https://api.m.jd.com/client.action?functionId=getCcFeedInfo&' + params
        url = 'https://api.m.jd.com/client.action?functionId=getCcFeedInfo&ef=1&ep={"cipher": {"uuid": "EQHrCQY2ZWYnZQDwENvvCG=="}, "ciphertype": 5}&client=android&clientVersion=11.0.2&st=1654569699575&sv=122&sign=776b9af25e378cdbe60d41a787031848'
        print(url)
        headers = {
            "host": "api.m.jd.com",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "content-length": str(len(body))
        }
        data = "body=%7B%22categoryId%22%3A118%2C%22childActivityUrl%22%3A%22openapp.jdmobile%3A%2F%2Fvirtual%3Fparams%3D%7B%5C%22category%5C%22%3A%5C%22jump%5C%22%2C%5C%22des%5C%22%3A%5C%22couponCenter%5C%22%7D%22%2C%22eid%22%3A%22eidAf88f8122e6sfjj96vPLKTtiORkUkZ2AHKo4%2FfDrdfe%2BkkeIKo5PX3AXE%2BGtigSqzU0kxK7ewujreKnC5QU57qV%2BQkNzrHqlEUg%2F89pNKdDtykeZr%22%2C%22globalLat%22%3A%220e46e12a7ead1c2b7df0929dd63927ca%22%2C%22globalLng%22%3A%227baec0c500a5f9e539a2cb1699e45cbd%22%2C%22lat%22%3A%2208f8d0ab437c440a5c6e31e582f4ee25%22%2C%22lng%22%3A%22db954ffe32435cb6939cf5973ed7e91b%22%2C%22monitorRefer%22%3A%22appClient%22%2C%22monitorSource%22%3A%22ccfeed_android_index_feed%22%2C%22pageClickKey%22%3A%22Coupons_GetCenter%22%2C%22pageNum%22%3A1%2C%22pageSize%22%3A20%2C%22shshshfpb%22%3A%22JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp%7En9zx%2BEhUkbynGit%2BZWEFz0%2BCp4cn%2BG9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN%22%7D&"
        res = requests.post(url, headers=headers, data=data, verify=False).json()


        print(res)

        url = "https://api.m.jd.com/client.action?functionId=getCcFeedInfo&clientVersion=11.0.2&client=android&ef=1&ep={\"cipher\": {\"uuid\": \"EJHwYzOnDJVrZQDsZwOmYq==\"}, \"ciphertype\": 5}&st=1654498521716&sign=74ed69a7dd18a80eb2b9d5dde6c1994e&sv=122"
        print(url)
        payload = "body=%7B%22categoryId%22%3A118%2C%22childActivityUrl%22%3A%22openapp.jdmobile%3A%2F%2Fvirtual%3Fparams%3D%7B%5C%22category%5C%22%3A%5C%22jump%5C%22%2C%5C%22des%5C%22%3A%5C%22couponCenter%5C%22%7D%22%2C%22eid%22%3A%22eidAf88f8122e6sfjj96vPLKTtiORkUkZ2AHKo4%2FfDrdfe%2BkkeIKo5PX3AXE%2BGtigSqzU0kxK7ewujreKnC5QU57qV%2BQkNzrHqlEUg%2F89pNKdDtykeZr%22%2C%22globalLat%22%3A%220e46e12a7ead1c2b7df0929dd63927ca%22%2C%22globalLng%22%3A%227baec0c500a5f9e539a2cb1699e45cbd%22%2C%22lat%22%3A%2208f8d0ab437c440a5c6e31e582f4ee25%22%2C%22lng%22%3A%22db954ffe32435cb6939cf5973ed7e91b%22%2C%22monitorRefer%22%3A%22appClient%22%2C%22monitorSource%22%3A%22ccfeed_android_index_feed%22%2C%22pageClickKey%22%3A%22Coupons_GetCenter%22%2C%22pageNum%22%3A1%2C%22pageSize%22%3A20%2C%22shshshfpb%22%3A%22JD012145b9t9Q5U1bXyW165448515759602fN8enZeDfydxdhnUEnIOXSGJrWBA0gD0CaPa-4QRHmkhEa6j2KFEMLG0bSV74vi4mTFluMFNTbm86qaZSRaqNcMYwESdLRhA19p40xp%7En9zx%2BEhUkbynGit%2BZWEFz0%2BCp4cn%2BG9j1R0gTqCU3BIN8l6fhSWTWWVC85uNQpEGN%22%7D&"
        headers = {
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print("text"+response.text)




        if res['code'] == '0':
            # return res['result']['couponList'][0]['receiveKey']
            for coupon in res['result']['couponList']:
                if coupon['title'] != None and '每周可领一次' in coupon['title']:
                    receiveKey = coupon['receiveKey']
                    return receiveKey
            print('没有找到59-20券的receiveKey')
            return -1
        else:
            print('获取59-20券的receiveKey失败')
            return -1


def get_receiveNecklaceCoupon_sign(receiveKey):
    body = {"channel": "领券中心",
            "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
            "couponSource": "manual",
            "couponSourceDetail": None,
            "eid": randomString(16),
            "extend": receiveKey,
            "lat": "",
            "lng": "",
            "pageClickKey": "Coupons_GetCenter",
            "rcType": "4",
            "riskFlag": 1,
            "shshshfpb": "",
            "source": "couponCenter_app",
            "subChannel": "feeds流"
            }
    # res = get_sign_api('newReceiveRvcCoupon', body) # 领券
    res = get_sign_api('receiveNecklaceCoupon', body)  # 59-20
    if res == -1:
        return -1
    else:
        params = res['sign']
        functionId = res['fn']
        body = re_body.findall(params)[0]
        params = params.replace(body, '')
        url = f'https://api.m.jd.com?functionId={functionId}&' + params
        return [url, body]


def receiveNecklaceCoupon(url, body, cookie):
    headers = {
        "Host": "api.m.jd.com",
        "cookie": cookie,
        "charset": "UTF-8",
        "user-agent": "okhttp/3.12.1;jdmall;android;version/10.1.4;build/90060;screen/720x1464;os/7.1.2;network/wifi;",
        "accept-encoding": "br,gzip,deflate",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "content-length": str(len(body)),
    }
    res = requests.post(url=url, headers=headers, data=body, timeout=30).json()
    # print(res)
    try:
        if res['code'] == '0' and res['msg'] == '响应成功':
            if res['result']['optCode'] == '9000':
                desc = res['result']['desc']
                quota = res['result']['couponInfoList'][0]['quota']
                discount = res['result']['couponInfoList'][0]['discount']
                endTime = res['result']['couponInfoList'][0]['endTime']
                timeStamp = int(endTime) / 1000
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
                msg = f'{desc}，满{quota}减{discount}({otherStyleTime}过期)'
                print(msg)
            else:
                print(res['result']['desc'])
        else:
            print(res['msg'])
    except:
        pass


def jdtime():
    url = 'http://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5'
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=1).json()
        return int(res['currentTime2'])
    except:
        return 0

#ck -> receiveKey ->
if __name__ == '__main__':

    print('59-20准备...')
    while True:
        if starttime - int(time.time() * 1000) <= 120000:
            break
        else:
            if int(time.time() * 1000) - atime >= 30000:
                atime = int(time.time() * 1000)
                print(f'等待获取log中，还差{int((starttime - int(time.time() * 1000)) / 1000)}秒')

    print('正在获取59-20券key')
    receiveKey = getCcFeedInfo(cookie)
    if receiveKey != -1:
        print(receiveKey)
        print(f'正在生成{range_n * 2}条抢券链接')

        tasks = list()
        s = 0
        while s < range_n:
            res = get_receiveNecklaceCoupon_sign(receiveKey)
            if res != -1:
                url = res[0]
                body = res[1]
                tasks.append(threading.Thread(target=receiveNecklaceCoupon, args=(url, body, cookie)))
                tasks.append(threading.Thread(target=receiveNecklaceCoupon, args=(url, body, cookie)))
                s = s + 1
        print('生成完毕，等待抢券')
        while True:
            if jdtime() >= starttime:
                time.sleep(delay_time)
                for task in tasks:
                    task.start()
                    time.sleep(range_sleep)
                for task in tasks:
                    task.join()
                break
