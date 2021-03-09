import re
import time
import json
import pymysql
import requests

def get_ip():
    dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main():
    headers = {
        'cookie': '_zap=322f132c-829c-4de3-bc53-518a034c450a; d_c0="AAAZJmDxbhGPTpCtW8Hag2g5VG6hlf_8-Q4=|1592283026"; _ga=GA1.2.800688044.1592283027; _xsrf=vu3ouddwSZrmDd3ipRyUJeb4gAi0e3WP; _gid=GA1.2.1682116480.1598231717; q_c1=2d73e23eea324db7af8431ac99a510a8|1598231748000|1598231748000; tst=r; l_n_c=1; o_act=login; r_cap_id="ODc1YzU1ZmQzNTA4NGE0MWEyODY0OGVlMDJlNzEwY2I=|1598256286|369b94994e28d4bd6921d14593700aaa74e47d2c"; cap_id="NjkwNzgwM2QwZTVlNGIwMmJiMjgyZGVhYjEyNDgwMjM=|1598256286|cb8e7081cc2593c248b6cf3e48e2c2fa19938d7d"; l_cap_id="YmM3ZjQ0NDZmMjZkNGZkNmFmOWQ5NzcyYzM5ZTMyYmQ=|1598256286|1c1cfc461dfb932dd78ef845f7ba3092235a22d2"; n_c=1; capsion_ticket="2|1:0|10:1598256464|14:capsion_ticket|44:MWU4NTgwMTRhNTVlNDk4Njg3OTVmMmIxNjI0ZDY0M2M=|90cee30c0a3dc6223cf20efab16ed6b3c26227e82ae7a58e01cc5d2b0c635692"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1598254495,1598256256,1598256327,1598256477; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1598256940; KLBRSID=cdfcc1d45d024a211bb7144f66bda2cf|1598257130|1598256965',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    url = 'https://www.lagou.com/zhaopin/Java/6/?filterOption=3&sid=104b34db442b4ce096e6f1789914af0b'
    response = requests.request(method='get', url=url, proxies=proxys[-1], timeout=10, headers=headers).content.decode('utf-8')
    print(response)

def post_request():
    headers = {
        'first': 'false',
        'pn': '3',
        'kd': 'java',
        'sid': '536056111b424dd0a81647ad391a4769'
    }
    response = requests.post(url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',json=headers,headers=headers).text
    print(response)

if __name__ == '__main__':
    sum = []
    proxys = []
    get_ip()
    main()
    time.sleep(3)
    post_request()