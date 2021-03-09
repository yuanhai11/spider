import requests
import json,time

url = 'http://seal.zj.gov.cn/seal/rest/organize/getTreeWithAreaAndName'
headers = {
    'type': 'apply',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'cookie':'SESSION=OTU4MTM2OTYtYjUzNi00MTRkLTgwNjUtMDkzMThhZmFhNWQ1; SERVERID=f71ca4d53b890a16610c6a0a445c01fa|1606871464|1606870935'
}
data = {
    'fullName':'',
    'uuid':'d5fd64547886483fa192199a9b1e2e54'
}
response = requests.request(method='post',url=url,headers=headers,json=data).text
print(response)
response = json.loads(response)['data']

def get_data(uuid):
    time.sleep(2.5)
    data = {
        'fullName': '',
        'uuid': uuid
    }
    response = json.loads(requests.request(method='post', url=url, headers=headers, json=data).text)['data']
    # print(len(response))
    # exit()
    return response

for i in response:
    uuid = i['uuid']
    fullName = i['fullName']
    subFlag = i['subFlag']
    print(fullName)
    # continue
    if subFlag == 1:
        res = get_data(uuid)
        for j in res:
            uuid1 = j['uuid']
            fullName1 = j['fullName']
            print(fullName,'-',fullName1)
            # continue
            subFlag = j['subFlag']
            if subFlag == 1:
                res1 = get_data(uuid1)

                for h in res1:
                    uuid2 = h['uuid']
                    fullName2 = h['fullName']
                    print(fullName, '-', fullName1,'---',fullName2)
                    subFlag = h['subFlag']
                    if subFlag == 1:
                        res2 = get_data(uuid2)

                        for m in res2:
                            uuid3 = m['uuid']
                            fullName3 = m['fullName']
                            print(fullName, '-', fullName1,'---',fullName2,'-----',fullName3)
                            subFlag = m['subFlag']
                            if subFlag == 1:

                                res3 = get_data(uuid3)

                                for l in res3:
                                    uuid4 = l['uuid']
                                    fullName4 = l['fullName']
                                    print(fullName, '-', fullName1, '---', fullName2, '-----', fullName3,'-------',fullName4)
                                    subFlag = l['subFlag']
                                    if subFlag == 1:
                                        print('还有第五层数据！！！')
