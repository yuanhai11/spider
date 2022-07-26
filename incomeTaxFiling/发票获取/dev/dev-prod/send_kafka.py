from kafka import KafkaProducer
from decouple import config
import json,time
SERVER = config("KAFKA_SERVER").split(",")
producer = KafkaProducer(bootstrap_servers=SERVER)

dic = {"taxPwd":"zlcw1401","companyId":"2344","companyName":"杭州永亦强起重设备有限公司","handleTaxName":"李耀","localDate":"2022-05-06","taxAccount":"91330105MA2GNX4C4M","handleTaxPwd":"zlcw1401","tenant_code":"ZH-383-20191217145410"}
print(dic)
dic = json.dumps(dic)
producer.send('invoice_info',dic.encode('utf-8'))

dic = {"taxPwd":"zlcw1401","companyId":"1967","companyName":"杭州铸品科技有限公司","handleTaxName":"陈洋","localDate":"2022-05-06","taxAccount":"91330110MA2B09PQ7N","handleTaxPwd":"Zlcw1401","tenant_code":"ZH-383-20191217145410"}
print(dic)
dic = json.dumps(dic)
producer.send('invoice_info',dic.encode('utf-8'))
producer.flush()
producer.close()