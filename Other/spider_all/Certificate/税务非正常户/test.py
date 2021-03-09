import requests
import time,re
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
names = ['嘉兴','金华','台州','湖州','绍兴','衢州','舟山','丽水']
urls = ['http://zhejiang.chinatax.gov.cn/col/col19851/index.html','http://zhejiang.chinatax.gov.cn/col/col19903/index.html','http://zhejiang.chinatax.gov.cn/col/col19955/index.html'
        ,'http://zhejiang.chinatax.gov.cn/col/col19877/index.html','http://zhejiang.chinatax.gov.cn/col/col19825/index.html','http://zhejiang.chinatax.gov.cn/col/col19929/index.html',
        'http://zhejiang.chinatax.gov.cn/col/col19981/index.html','http://zhejiang.chinatax.gov.cn/col/col20007/index.html'
        ]
gagaga = zip(names,urls)
for name,url in gagaga:
    if name != '衢州':
        continue
    sum = []
    time.sleep(1)
    data = requests.request(method='get',url=url,headers = headers).text
    for i in re.findall(r'<a href="(.*?)" target="_blank"',data):

        detail_url = 'http://zhejiang.chinatax.gov.cn' + i
        time.sleep(1)
        data1 = requests.request(method='get', url=detail_url, headers=headers).text
        import re
        code = re.findall(r'vc_xxgkarea=(.*?)";',data1)[0]
        print(code)
        json_data = {
            'divid': 'div11930',
            'infotypeId': 'Z0713',
            'jdid': 15,
            'area': code,
            'sortfield': 'createdatetime:0',
            'standardXxgk': 0,
        }
        time.sleep(1)
        search_url = 'http://zhejiang.chinatax.gov.cn/module/xxgk/search.jsp?'
        response = requests.request(method='post', url=search_url, headers=headers, data=json_data).text
        urlsssss = re.findall(r"<a href='(.*?)' target='_blank'", response, re.S)
        print((name,urlsssss))
        # exit()