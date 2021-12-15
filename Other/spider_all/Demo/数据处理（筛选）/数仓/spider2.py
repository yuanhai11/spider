import requests

headers = {
   'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'AppId': 'zl-saas',
'Authorization': '892_9fdaae7d250a40c6ab9f22b6c5d9d752',
'Connection': 'keep-alive',
'Content-Length': '721',
'Content-Type': 'application/json;charset=UTF-8',
'Host': 'api.360jizhang.com',
'httpMethod': 'post',
'method': 'api/compass/data/search',
'module': 'zl-compass',
'Origin': 'https://cs.360jizhang.com',
'Referer':'https://cs.360jizhang.com/',
'rpcType': 'http',
'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
'sec-ch-ua-platform': "Windows",
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-site',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}
import json
import time
print(requests)
# 418
for page in range(1017,1840):
    time.sleep(5)
    data = {"page":page,"pageSize":200,"keyword":"","searchList":[],"regMoney":"","applyDate":"2020-12-01,2021-02-28","insuranceNum":"0,3","brandNum":"","iprNum":"","patentNum":"","authorNum":"","softwareNum":"","jobNum":"","moreConditions":{"isBusinessRisk":"","isCityTech":"","isCountriesTech":"","isDaChuang":"","isEagleTech":"","isEmail":"","isMobile":"","isPhone":1,"isTel":"","isConnect":"","isNet":"","isParasiticAddr":"","isPeerNumber":"","isProvinceTech":"","isTechEnterprise":"","isRealTel":""},"industry":{"first":[],"second":[],"third":[]},"location":{"province":[],"city":[],"area":[]},"enumStatus":{"businessCode":2,"capitalType":"","companyCode":1},"sequence":0,"multiDimensionalList":[],"customerStatus":0,"userId":892}
    res = requests.post(url="https://api.360jizhang.com/api/compass/data/search",headers=headers,json=data).json()
    code = res["code"]
    data = res["data"]
    if code != 0:
        print("数据出错了，page:----------------",page)
        exit()
    else:
        d = data['records']
        print(len(d))
        for d_single in d:
            sum = {}
            company_name =d_single['companyName']
            insurance_num =d_single['insuranceNum']
            reg_date =d_single['applyDate']
            phone = d_single['mobiles']
            company_status =d_single['businessStatus']
            company_type =d_single['companyType']
            sum['company_name'] = company_name
            sum['insurance_num'] = insurance_num
            sum['reg_date'] = reg_date
            sum['phone'] = phone
            sum['company_status'] = company_status
            sum['company_type'] = company_type
            with open('data1.txt','a',encoding='utf-8')as fp:
                fp.write(json.dumps(sum,ensure_ascii=False)+'\n')
        print("第{}页跑完:".format(page))
