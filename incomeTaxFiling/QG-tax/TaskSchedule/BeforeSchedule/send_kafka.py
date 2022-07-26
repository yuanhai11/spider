from kafka import KafkaProducer
import json,time
producer = KafkaProducer(bootstrap_servers=['192.168.2.99:9091','192.168.2.99:9092','192.168.2.99:9093'])

import time

t = int(time.time())

for i in range(t,t+2):

    dic = {"taskId": '{}'.format(i), "taskType": "个税申报", "orgType": "个税", "orgName": "sh", "requestParams": {
            "data": {"loginname": "91330101MA2CDKYG4B", "password": "g4nUy2wY+NOcOD1Xfgr8mA==", "taxStaffRpaVOS": [
                {"id": 63821, "companyId": 2132, "identifyDate": "2021-07", "name": "李文龙", "certificateType": "居民身份证",
                 "certificateNumber": "420102198109240319", "nationality": "中国", "gender": "男",
                 "birthday": "1981-09-24", "status": "正常", "remark": "None", "quitDate": "None", "mob": "18611345690",
                 "otherCertificateNumber": "", "birthCountry": "", "employedType": "雇员", "employedDate": "2018-08-13",
                 "taxRelatedMatters": "", "entryDate": "None", "departureDate": "None"}], "staffSalaryVOS": [
                {"identifyDate": "2021-07", "companyId": 2132, "taxStaffId": 1204, "currentIncome": 0.00,
                 "insurance": 0.00, "medicalInsurance": 0.00, "unemploymentInsurance": 0.00, "accumulationFund": 0.00,
                 "name": "李文龙", "certificateType": "居民身份证", "certificateNumber": "420102198109240319"}]}}}
    dic = json.dumps(dic)
    producer.send('ptax_zero_declare',dic.encode('utf-8'))
    producer.flush()
producer.close()
