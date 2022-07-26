from kafka import KafkaProducer
from decouple import config
import json,time
SERVER = config("KAFKA_SERVER").split(",")
producer = KafkaProducer(bootstrap_servers=SERVER)
for i in range(20):
    dic = {"taxPwd":"zlcw1401","companyId":"2344","companyName":"杭州永亦强起重设备有限公司","handleTaxName":"李耀","localDate":"2022-05-06","taxAccount":"91330105MA2GNX4C4M","handleTaxPwd":"zlcw1401","tenant_code":"ZH-383-20191217145410"}
    print(dic)
    dic = json.dumps(dic)
    producer.send('taxpayer_type_title',dic.encode('utf-8'))

producer.flush()
producer.close()