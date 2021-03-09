# import requests
# import re
# import json
# import time
# headers = {
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
# }
# proxys = []
# def dl():
#     dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
#     resp = requests.get(dlurl).text
#     time.sleep(4)
#     resp = re.sub(r'\n', '', resp)
#     proxy = {
#         'http': resp
#     }
#     proxys.append(proxy)
#     print(proxys[-1])
# # dl()
# company_name = "中国人寿保险股份有限公司杭州市分公司"
# page = 1
# url = "https://search.51job.com/list/000000,000000,0000,00,9,99,中国人寿保险股份有限公司杭州市分公司,{},1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=".format(page)
# response_web = ""
# for IP in range(10):
#     try:
#         response_web = requests.request(method='get', url=url,headers=headers,
#                                         timeout=10)
#         print(response_web)
#         if response_web.status_code == 200:
#             response_web = response_web.text
#             break
#     except Exception:
#         dl()
# if response_web == "":
#     raise ValueError('代理IP获取数据有误！！！')
# print(response_web)
# response = json.loads(response_web)
# total_page = response.get('total_page')
# search_results = response.get('engine_search_result')
# for result in search_results:
#     job_id = result.get('')
#     station_name = result.get('')
#     salary = result.get('')
#     position = result.get('')
#     release_time = result.get('')
#     detail_url = result.get('')
#     job_detail = result.get('')
#
#
#     company_name = company_name

from getCompanyId.get_company_id import get_company_id
# from Other.post_es import get_company_id
id = get_company_id('浙江中禄财务咨询有限公司')
print(id)