# coding:utf-8
import pymysql
import requests
import json,datetime,os
content = input('输入：')
data = json.loads(content)
data1 = data['data']['pageList']
data = [i['id'] for i in data1]
company_name = [i['companyName'] for i in data1]
folder = str(datetime.date.today())
path = os.path.join(os.path.abspath('.'),'photo',folder)
if not os.path.exists(path):
    os.mkdir(path)
for name,i in zip(company_name,data):
    headers = {
        "AppId":"zl-saas",
        "Authorization":"2088_f8c5d4f98ad54b7db92e9e45321dbb96",
        "extInfo":'{"declareId":%s}'%i,
        "Host":"api.360jizhang.com",
        "httpMethod":"get",
        "method":"api/saas/tax/declaration/receipt",
        "module":"saas",
        "Origin":"https://cs.360jizhang.com",
        "Referer":"https://cs.360jizhang.com/",
        "rpcType":"http",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    }
    try:
        res = requests.request(method='get',url='https://api.360jizhang.com/',headers=headers).json()['data']
        if '个税(工资薪金所得)' not in str(res):
            print(i,name,'没有个税薪金')
        else:
            for k in res:
                if k['taxName']=='个税(工资薪金所得)':
                    print(i,name,k['fileUrl'])
                    rr = requests.get(k['fileUrl']).content
                    with open(r'{}/{}.jpg'.format(path,name),'wb')as fp:
                        fp.write(rr)
                    break
    except Exception:
        print('error')
        pass