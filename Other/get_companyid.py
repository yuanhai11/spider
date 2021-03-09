import requests
import time
def get_company_id(keyword):
    time.sleep(0.5)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }
    data = {
        'keyword': keyword,
        "page": 1,
        "pageSize": 20,
        "searchList": ["companyName.keyword"],
    }
    dd = requests.post(url='http://192.168.2.95:18018/api/compass/data/search', headers=headers, json=data).json()
    print(dd)

    list = dd.get('data').get('records')
    if len(list) != 0:
        return list[0].get('companyId')
    else:
        return None

