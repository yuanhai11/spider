# import requests
# import re,json
# import time
# import requests,pymysql
#
# # url = 'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?6SQk6G2z=GBK-5NMewgTGKRSHGwJa_7ZKnmXWVixnx8KtsW2sT9ZYuUE.wR1zNaXgjKEWgbpKzhAU1tE31p0xTXoIX6wAC_H7xieeB7hq9twZz2rT.3qaoTMshOhxwDN0eScpHt0.P7ePXFBRWSR82OmMFEPe_9vaaBe5bmTdofmC9xO6kN8O4Tq4YIMLQKeIcdOhr_HGDsC3rQAfUdxeGv0htX_kH2JxOYPV8mPu9U9AU6t8sK85XAEgZogWARwv2ug_Zf7oPVViqpgoc.JG2rKIB2.vJW2gCgNp5jzCeq0gubz8yrRFqXPSnmoa.IXBNvUkK1R9Bw29zpA2URqZuVNVoZVaXrYJhU7VGwTVHLQV2NK.Wdix0cfa'
# url = 'http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=28&tableName=TABLE28&title=%BB%A5%C1%AA%CD%F8%D2%A9%C6%B7%D0%C5%CF%A2%B7%FE%CE%F1&bcId=152912030752488832300204864740'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
#     'Cookie': 'JSESSIONID=FFD68A40DCE1E0D52C0FD21650C59EA7.7; neCYtZEjo8GmS=5JBX7VuGSQ2sDmmoW7TGKrz.QA3Ua2w3N8qjn0cY2PmDzUulu0FV7eG3A_8_NQX97h34yoeKUf14juAvRGoEeNG; UM_distinctid=176cc4efd8b169-016e6b9e061161-c791039-1fa400-176cc4efd8c4c9; acw_tc=b65cfd3316115401778147489e25c8d152f92146a0edf9e26ec58157d3bbcd; neCYtZEjo8GmT=53qgb9CqixBVqqqm6JTHDfq279oBNO8HrBqni8Qiqa0BTsUKWDAoHDmTNmqQhHnGHlIzOMpeQlcpIGWYJb8C7dO4.p5yRuBaluKcebLexLYh82QaKSI3rJ.iKnsECBsPL6E9XNxWS28b2dWAZRDDmq.v88qccr36bTnDqI3MlHBJAybs8Ngvx9YBS0ZI7aYFh1uW3cbszIpuPj7XV6.npdZYzLdR5GsLckl7bEXZ4II8qaqzzVJDXS9c31.luKiag7gCYX_pL0Yqe5XxsQuDq0w98A6nVuwRzHfi8lcDFQAVrOiL17jLvFQ8dqEJqtc90V'
# }
# data = {
# 'tableId': 28,
# 'State': 1,
# 'bcId': 152912030752488832300204864740,
# 'State': 1,
# 'curstart': 2,
# 'State': 1,
# 'tableName': 'TABLE28',
# 'State': 1,
# 'viewtitleName': 'COLUMN212',
# 'State': 1,
# 'viewsubTitleName': 'COLUMN210',
# 'State': 1,
# 'tableView': '%E4%BA%92%E8%81%94%E7%BD%91%E8%8D%AF%E5%93%81%E4%BF%A1%E6%81%AF%E6%9C%8D%E5%8A%A1',
# 'State': 1,
# 'cid': 0,
# 'State': 1,
# 'ytableId': 0,
# 'State': 1,
# 'searchType': 'search',
# 'State': 1,
# }
# # response = requests.request(method='post', url=url,headers=headers,json=data,timeout=10).text
# response = requests.request(method='get', url=url,headers=headers,timeout=10).text
# print(response)
import pandas as pd
data = pd.read_excel(r'C:\Users\20945\Desktop\compass.xlsx')
print(data)