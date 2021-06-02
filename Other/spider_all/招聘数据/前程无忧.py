import time
import re
import json
import requests, pymysql
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:

class Medicine(Base):
    # 表的名字:
    __tablename__ = 'zp_qcwy_old'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    job_id = Column(String(256))
    post_name = Column(String(256))
    company_name = Column(String(256))
    work_place = Column(String(256))
    work_pay = Column(String(256))
    release_time = Column(String(256))

    gmt_created = Column(String(256))
    gmt_updated = Column(String(256))
    details_url = Column(String(256))
    company_url = Column(String(256))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:BOOT-xwork1024@192.168.2.97:3306/spider')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()

proxys = []


def dl():
    while 1:
        try:
            dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
            resp = requests.get(dlurl).text
            break
        except Exception:
            pass
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

dl()

def get_updated():
    db = pymysql.connect(host="192.168.2.97", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select job_id from zp_qcwy_old"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=1000000, error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def get_response(url):
    while 1:
        try:
            response_deta = requests.request(method='get', url=url, proxies=proxys[-1],
                                             headers=headers, timeout=10, allow_redirects=False)
            if response_deta.status_code == 200:
                res = response_deta.text
                break
        except Exception as e:
            print(e)
            dl()
    return res


def main():
    bloom = get_updated()
    for area in ['01','02','03','04','05','06','07','08','09','10','11','12','13']:

        url = 'https://search.51job.com/list/080200,0802{},0000,00,9,99,+,2,1.html?'.format(area)
        res = get_response(url)
        total_page = int(re.findall(r'"total_page":"(.*?)",',res)[0])
        print(total_page)
        for page in range(1,total_page+1):

            url = 'https://search.51job.com/list/080200,0802{},0000,00,9,99,+,2,{}.html?'.format(area,page)
            time.sleep(5)

            res = get_response(url)
            data = re.findall(r'window.__SEARCH_RESULT__ = (.*?),"jobid_count"', res)[0] + '}'
            data = json.loads(data)['engine_search_result']
            print(len(data))
            for d in data:
                job_id = d.get('jobid')
                post_name = d.get('job_name')
                company_name = d.get('company_name')
                work_place = d.get('workarea_text')
                work_pay = d.get('providesalary_text')
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                release_time = d.get('issuedate')
                details_url = d.get('job_href')
                company_url = d.get('company_href')

                if job_id not in bloom:
                    medicine = Medicine(job_id=job_id, post_name=post_name, company_name=company_name, work_place=work_place,
                                        work_pay=work_pay,
                                        release_time=release_time, gmt_created=times, gmt_updated=times,
                                        details_url=details_url, company_url=company_url)
                    session.add(medicine)
                    print('没有job_id',job_id)
                    continue

                medi = session.query(Medicine).filter(Medicine.job_id==job_id).all()
                print('有job_id', job_id)
                for m in medi:
                    session.delete(m)

                medicine = Medicine(job_id=job_id, post_name=post_name, company_name=company_name, work_place=work_place,
                                    work_pay=work_pay,
                                    release_time=release_time, gmt_created=times, gmt_updated=times,
                                    details_url=details_url, company_url=company_url)
                session.add(medicine)
            session.commit()
        time.sleep(10)


if __name__ == '__main__':
    headers = {
        'cookie':'guid=e7012553653123b841c9a8fc0ac4f1b9; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; adv=adsnew%3D1%26%7C%26adsnum%3D7093970%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.K00000jBQdve1ESlLldt9tsl1vMqYR51x8ASMb0h6aJf6d9ZgrMqy4SFQ323Caysp6H36aNsJ4tzkRk32Isfs9fT9lgsyOYFLi6HvH7NMRiWU3KXba-ohLBOE-D-aK75pmGyPevYcjKRrDK1ekp0CFjc49F7hN9JafZSnqXKX5bTxvLaMjLplr1i2BdhhlI4hxqnN3mFUanxgEwBnJsNqRxXxjo3.DR_NR2Ar5Od66CHnsGtVdXNdlc2D1n2xx81IZ76Y_XPhOWEtUrorgAs1SOOo_9OxOBI5lqAS61kO56OQS9qxuxbSSjO_uPqjqxZOg7SEWSyWxSrOSFO_OguCOBxQetZO03x501SOOoCgOQxG9YelZ4EvOqJGMqEOggjSS4Wov_f_lOA7MuvyNdleQeAI1PMAeB-5Wo9Eu88lN2s1f_TTMHYv00.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqPH7JUvc0IgP-T-qYXgK-5H00mywxIZ-suHY10ZIEThfqPH7JUvc0ThPv5HD0IgF_gv-b5HDdnWfLnW0krHT0UgNxpyfqnHfzPjnvrHb0UNqGujYknj63rHTvnfKVIZK_gv-b5HDznWT10ZKvgv-b5H00pywW5R42i-n0mLFW5HmYPH64%2526ck%253D3629.2.803.765.157.760.150.285%2526dt%253D1615874188%2526wd%253D51job%2526tpl%253Dtpl_12273_24677_20875%2526l%253D1524720197%2526us%253DlinkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E3%25252580%25252590%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A751Job%252525E3%25252580%25252591-%25252520%252525E5%252525A5%252525BD%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%2521%252526linkType%25253D%26%7C%26ad_logid_url%3Dhttps%253A%252F%252Ftrace.51job.com%252Ftrace.php%253Fadsnum%253D6776250%2526ajp%253DaHR0cHM6Ly9ta3QuNTFqb2IuY29tL3RnL3NlbS9MUF8yMDIwXzEuaHRtbD9mcm9tPWJhaWR1YWQ%253D%2526k%253Dd946ba049bfb67b64f408966cbda3ee9%2526bd_vid%253D8103717553595172002%26%7C%26; search=jobarea%7E%60080200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%BA%BC%D6%DD%C3%F7%BA%CD%D7%B0%CA%CE%B9%A4%B3%CC%D3%D0%CF%DE%B9%AB%CB%BE%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60080200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%BA%BC%D6%DD%D1%D5%D5%DF%BB%AF%D7%B1%C6%B7%D3%D0%CF%DE%B9%AB%CB%BE%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%BA%BC%D6%DD%BC%F2%BF%C7%CE%C4%BB%AF%B4%B4%D2%E2%D3%D0%CF%DE%B9%AB%CB%BE%A1%FB%A1%FA1%A1%FB%A1%FA1%7C%21collapse_expansion%7E%601%7C%21;',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        "lang": "c",
        "postchannel": "0000",
        "workyear": "99",
        "cotype": "99",
        "degreefrom": "99",
        "jobterm": "99",
        "companysize": "99",
        "ord_field": "0",
        "dibiaoid": "0",
        "line": "",
        "welfare": "",
    }
    main()
