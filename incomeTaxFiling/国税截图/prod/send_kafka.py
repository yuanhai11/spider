import base64

import requests
from kafka import KafkaProducer
from decouple import config
import json,time



def aa():

    SERVER = config("KAFKA_SERVER").split(",")
    producer = KafkaProducer(bootstrap_servers=SERVER)
    t = int(time.time())
    for i in range(t,t+2):
        url = "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/home/wybs/index.html?ticket=ST-16641204-RhnmxfC3pMm6sgpkx2Gs-com.hz.zkxx.ydzhz"
        dic = {"taskId": '{}'.format(i),"companyName": '{}'.format("杭州曼好时电子商务有限公司"),"Url": '{}'.format(url) }
        print(dic)
        dic = json.dumps(dic)
        producer.send('rpa-country-screen',dic.encode('utf-8'))
        producer.flush()
    producer.close()


def image_to_url(dz):
    headers1 = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': "47.111.176.38:48016"
    }
    with open(dz, "rb") as f:
        base64_data = base64.b64encode(f.read())
        base64_data = str(base64_data).split("'")[1]
        url = "http://47.111.176.38:48016/oss/upload"
        data = {"imgContent": base64_data}
        data = json.dumps(data)
        for k in range(5):
            try:
                gaga = requests.post(url=url, data=data, headers=headers1)
                gaga1 = json.loads(gaga.text)
                gaga.close()
                break
            except Exception:
                continue

        zzz = gaga1['data']['imageUrl']
    return zzz

if __name__ == '__main__':
    print(image_to_url(r"D:\RPA\zl-rpa\incomeTaxFiling\国税截图\prod\1.png"))
'http://oss-xwork.oss-cn-hangzhou.aliyuncs.com/f86f0e66-a7eb-446a-ba68-286063e8f081.jpg'