from kafka import KafkaProducer
from decouple import config
import json,time
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
