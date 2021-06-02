# # import time
# # import re
# # import json
# # import requests, pymysql
# # from sqlalchemy import Column, String, create_engine, Integer
# # from sqlalchemy.orm import sessionmaker
# # from sqlalchemy.ext.declarative import declarative_base
# #
# # # 创建对象的基类:
# # Base = declarative_base()
# #
# # # 定义User对象:
# #
# # class Medicine(Base):
# #     # 表的名字:
# #     __tablename__ = 'qcwy_old'
# #     id = Column(Integer(), primary_key=True, autoincrement=True)
# #     job_id = Column(String(256))
# #     post_name = Column(String(256))
# #     company_name = Column(String(256))
# #     work_place = Column(String(256))
# #     work_pay = Column(String(256))
# #     release_time = Column(String(256))
# #
# #     gmt_created = Column(String(256))
# #     gmt_updated = Column(String(256))
# #     details_url = Column(String(256))
# #     company_url = Column(String(256))
# #
# #
# # # 初始化数据库连接:
# # engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# # # 创建DBSession类型:
# # DBSession = sessionmaker(bind=engine)
# # # 创建session对象:
# # session = DBSession()
# #
# # proxys = []
# #
# #
# # def dl():
# #     while 1:
# #         try:
# #             dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
# #             resp = requests.get(dlurl).text
# #             break
# #         except Exception:
# #             pass
# #     time.sleep(3)
# #     resp = re.sub(r'\n', '', resp)
# #     proxy = {
# #         'http': resp
# #     }
# #     proxys.append(proxy)
# #     print(proxys[-1])
# #
# # dl()
# #
# # def get_updated():
# #     db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
# #     cursor = db.cursor()
# #     sql = "select job_id from qcwy_old"
# #     cursor.execute(sql)
# #     db_data = cursor.fetchall()
# #     data = [i[0] for i in db_data]
# #     from pybloom_live import ScalableBloomFilter
# #     bloom = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001)
# #     for bl in data:
# #         bloom.add(bl)
# #     return bloom
# #
# # def get_response(url):
# #     response_deta = requests.request(method='post', url=url,headers=headers, timeout=10, allow_redirects=False)
# #     if response_deta.status_code == 200:
# #         res = response_deta.text
# #     return res
# #
# # def main():
# #
# #         url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E6%9D%AD%E5%B7%9E&district=%E8%A5%BF%E6%B9%96%E5%8C%BA&needAddtionalResult=false'
# #         res = requests.request(method='post', url=url, proxies=proxys[-1],headers=headers,data=data, timeout=10,)
# #         print(res)
# #         print(res.text)
# #         exit()
# #
# # if __name__ == '__main__':
# #     data = {
# #         "first": "true",
# #         "pn": 1,
# #         # "kd": "",
# #         "sid": "da56155fefff4024829dfc77a53325d4",
# #     }
# #     headers = {
# #         'cookie':'user_trace_token=20210311171306-9cd83c10-7c40-4fb9-823f-8410255be438; _ga=GA1.2.620402020.1615453988; LGUID=20210311171306-6677facc-fa35-4065-bfe5-abf0b9b93425; RECOMMEND_TIP=true; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; PRE_HOST=www.baidu.com; LGSID=20210329102639-022f57fa-94d9-4a99-9696-a1be1286c322; PRE_UTM=m_cf_cpt_baidu_pcbt; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fother.php%3Fsc.Ks0000a8Zd9oCe4-o1JM7LjIhncpZsDN%5FfnVe0hjBS3WcLsxpNy22k3rsUoiutCupCXk0-TGyAmN6Z7zwrmOmJNoC5gUqvlW5IwagB6FidtZJtqxNe5K0h6e72CogwwkSBlf9Z5qd8xMnWyP16PLUzcseV6izsezwkhyfiZy2rKHOPlKJmhr20YEyd12JE5glu6ogE84HLBiZ-wAfJyeylvFHmV6.7Y%5FNR2Ar5Od663rj6tJQrGvKD77h24SU5WudF6ksswGuh9J4qt7jHzk8sHfGmYt%5FrE-9kYryqM764TTPqKi%5FnYQZHuukL0.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqs2v4%5FsKdTvNzgLw4TARqn0K9u7qYXgK-5Hn0IvqzujL0oUhY0ZFWIWYk0ZNzU7qGujYkPHcYP1f3njcL0Addgv-b5HDYnWfYP1610AdxpyfqnH03rH03PWm0UgwsU7qGujYknWcLnsKsI-qGujYs0A-bm1dribGH0APzm1YdnWR1%26ck%3D9436.6.165.895.163.701.155.331%26dt%3D1616984783%26wd%3D%25E6%258B%2589%25E9%2592%25A9%26tpl%3Dtpl%5F12273%5F24677%5F20875%26l%3D1524748027%26us%3DlinkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598-%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E6%25258B%25259B%2525E8%252581%252598%2525E3%252580%252591%2525E5%2525AE%252598%2525E6%252596%2525B9%2525E7%2525BD%252591%2525E7%2525AB%252599%252520-%252520%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E9%2525AB%252598%2525E8%252596%2525AA%2525E5%2525A5%2525BD%2525E5%2525B7%2525A5%2525E4%2525BD%25259C%2525EF%2525BC%25258C%2525E4%2525B8%25258A%2525E6%25258B%252589%2525E5%25258B%2525BE%21%2526linkType%253D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flanding-page%2Fpc%2Fsearch.html%3Futm%5Fsource%3Dm%5Fcf%5Fcpt%5Fbaidu%5Fpcbt; JSESSIONID=ABAAABAABAGABFA5D153AF44E238FD4D37E1500AABE3BE7; WEBTJ-ID=20210329%E4%B8%8A%E5%8D%8810:26:45102645-1787bce12035a1-067ec323cb52a4-5771031-2073600-1787bce1204c6b; sensorsdata2015session=%7B%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1615866924,1616984797,1616984800,1616984806; _gid=GA1.2.467680783.1616984806; __lg_stoken__=baebb794a98bd291950f05ea1db8ed59ff6ad42aa9c85bb01b34488fd69e01cbb820c4a083b612038673dfb46ec4292b013176607ec1bbfe6221a844f9121720d671687e0c18; gate_login_token=d197104acac1c3e0ae6ccc372cb7d5d58770dc4ddd9644b491fac50962029ecf; LG_LOGIN_USER_ID=ec120e6e9742eee2c6bf06981a3ec11fe5a5b627e870ecde1db5f750b1fa36e2; LG_HAS_LOGIN=1; _putrc=3A3AB49AC7E03DC4123F89F2B170EADC; login=true; unick=%E7%94%A8%E6%88%B76355; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; privacyPolicyPopup=false; SEARCH_ID=6e08545541124d7b8a3cacdf96123fa1; X_HTTP_TOKEN=7bea1e7ce28caa5d7515896161d62c557dca4ce0c7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215956014%22%2C%22first_id%22%3A%22178208fb6812cc-090af0e5f953ee-5771133-2073600-178208fb682c32%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2289.0.4389.90%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%22178208fb6812cc-090af0e5f953ee-5771133-2073600-178208fb682c32%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1616985158; TG-TRACK-CODE=search_code; LGRID=20210329103305-947f1d56-615f-44de-858d-f0f8f094a0b6',
# #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
# #     }
# #     main()
# # import re
# # import time
# # import json
# # import pymysql
# # import requests
# #
# # def get_ip():
# #     dlurl = 'http://dynamic.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
# #     resp = requests.get(dlurl).text
# #     resp = re.sub(r'\n', '', resp)
# #     proxy = {
# #         'http': resp
# #     }
# #     proxys.append(proxy)
# #     print(proxys[-1])
# #
# # def main():
# #     headers = {
# #         'cookie':'user_trace_token=20210311171306-9cd83c10-7c40-4fb9-823f-8410255be438; _ga=GA1.2.620402020.1615453988; LGUID=20210311171306-6677facc-fa35-4065-bfe5-abf0b9b93425; RECOMMEND_TIP=true; index_location_city=%E6%9D%AD%E5%B7%9E; LGSID=20210329102639-022f57fa-94d9-4a99-9696-a1be1286c322; JSESSIONID=ABAAABAABAGABFA5D153AF44E238FD4D37E1500AABE3BE7; WEBTJ-ID=20210329%E4%B8%8A%E5%8D%8810:26:45102645-1787bce12035a1-067ec323cb52a4-5771031-2073600-1787bce1204c6b; sensorsdata2015session=%7B%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1615866924,1616984797,1616984800,1616984806; _gid=GA1.2.467680783.1616984806; __lg_stoken__=baebb794a98bd291950f05ea1db8ed59ff6ad42aa9c85bb01b34488fd69e01cbb820c4a083b612038673dfb46ec4292b013176607ec1bbfe6221a844f9121720d671687e0c18; gate_login_token=d197104acac1c3e0ae6ccc372cb7d5d58770dc4ddd9644b491fac50962029ecf; LG_LOGIN_USER_ID=ec120e6e9742eee2c6bf06981a3ec11fe5a5b627e870ecde1db5f750b1fa36e2; LG_HAS_LOGIN=1; _putrc=3A3AB49AC7E03DC4123F89F2B170EADC; login=true; unick=%E7%94%A8%E6%88%B76355; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; privacyPolicyPopup=false; TG-TRACK-CODE=search_code; _gat=1; SEARCH_ID=c2e88d813f8d456aac8f42a2c69bdf8c; X_HTTP_TOKEN=7bea1e7ce28caa5d7287896161d62c557dca4ce0c7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215956014%22%2C%22first_id%22%3A%22178208fb6812cc-090af0e5f953ee-5771133-2073600-178208fb682c32%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2289.0.4389.90%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%22178208fb6812cc-090af0e5f953ee-5771133-2073600-178208fb682c32%22%7D; LGRID=20210329111707-2a7e4c29-d679-4bbc-8557-676686cadb5f; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1616987828',
# #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
# #     }
# #     url = 'https://www.lagou.com/zhaopin/Java/6/?filterOption=3&sid=104b34db442b4ce096e6f1789914af0b'
# #     response = requests.request(method='get', url=url, proxies=proxys[-1], timeout=10, headers=headers).content.decode('utf-8')
# #     print(response)
# #
# # def post_request():
# #     headers = {
# #         'first': 'false',
# #         'pn': '3',
# #         'kd': 'java',
# #         'sid': '536056111b424dd0a81647ad391a4769'
# #     }
# #     response = requests.post(url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',json=headers,headers=headers).text
# #     print(response)
# #
# # if __name__ == '__main__':
# #     sum = []
# #     proxys = []
# #     get_ip()
# #     main()
# #     time.sleep(3)
# #     post_request()
#
# import requests
#
# url = ' https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
#
#
# def get_json(url, num):
#     """
#     从指定的url中通过requests请求携带请求头和请求体获取网页中的信息,
#     :return:
#     """
#     url1 = 'https://www.lagou.com/jobs/list_python%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88?labelWords=&fromSearch=true&suginput='
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
#         'Host': 'www.lagou.com',
#         'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
#         'X-Anit-Forge-Code': '0',
#         'X-Anit-Forge-Token': 'None',
#         'X-Requested-With': 'XMLHttpRequest'
#     }
#     data = {
#         'first': 'true',
#         'pn': num,
#         'kd': 'python工程师'}
#     s = requests.Session()
#     print('建立session：', s, 'nn')
#     s.get(url=url1, headers=headers, timeout=3)
#     cookie = s.cookies
#     print('获取cookie：', cookie, 'nn')
#     res = requests.post(url, headers=headers, data=data, cookies=cookie, timeout=3)
#     res.raise_for_status()
#     res.encoding = 'utf-8'
#     page_data = res.json()
#     print('请求响应结果：', page_data, 'nn')
#     return page_data
#
#
# print(get_json(url, 1))