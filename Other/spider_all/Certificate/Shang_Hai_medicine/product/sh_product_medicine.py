import re
import os
import json
import math
import time
import requests
import pymysql
import json

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '120',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=57DAA15E6AD35CE328B15404976F3FED.7; neCYtZEjo8GmS=5LhKVFUZuv89FyACMNP9E.8chxugNTSY6PkTRWoGCeHiztlVF6MAz1pC0pCTRmpTBCVe_W6PS6zwQkHLtst85cA; acw_tc=276aedd516008412021111692e18638ed7629caa83355396dae64c4f28f28b; neCYtZEjo8GmT=5UC.7tYej4oEqqqm0XFj1CqDaeZAwerpQN92uYrXW7PrRrLEJHGcqgOG4ooA5GDgHENgJ6mqsSxMI6lTzeyByR.QGwmELT4tYMqw9HLJtfJlW4oVG7nMkeMCDa6S3VkgLVuMn3VZ6CxYY635UsJuatMsxBCBhj5dlBzlOm9oEN_PqvGxArGOxcUx7a1e3n2vadwiYCCRtv8dJkFCpoUjgXSDsKVQiJ2Td_u8SPs4RleHWZCkm3DMPrF1QFdchOqXFvU79K.4iVgXQgjSj3yYF57rmWdeJgxEOLpbdhGsUu6JGcJNAuAZhOlNDSWVrEkWhg',
    'Host': 'mpa.zjfda.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
proxys = []
def dl():
    dlurl = 'http://dps.kdlapi.com/api/getdps/?orderid=969607686104916&num=1&pt=2&sep=1'
    resp = requests.get(dlurl).text
    time.sleep(4)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])
dl()

def get_time(t):
    import time
    t = int(str(t)[:-3])
    time_local = time.localtime(t)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt
def get_updated():
    db = pymysql.connect(host="192.168.2.99", user="root", password='BOOT-xwork1024', database="spider", port=3306)
    cursor = db.cursor()
    sql = "select record_id from spider_zj_company_medicine"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    # print(db_data)
    # exit()
    data = [i[0] for i in db_data]
    from pybloom_live import ScalableBloomFilter
    bloom = ScalableBloomFilter(initial_capacity=10000,error_rate=0.001)
    for bl in data:
        bloom.add(bl)
    return bloom

def main():
    bloom = get_updated()
    sum = []
    data = {
           'tableId': 25,
           'bcId': 152904713761213296322795806604,
           'tableName': 'TABLE25',
           'viewtitleName': 'COLUMN167',
           'viewsubTitleName': 'COLUMN821, COLUMN170, COLUMN166',
            'curstart': 1,
            'tableView': '%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81',
            'State': 1,
    }
    url = 'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?6SQk6G2z=GBK-5a3m.NGtFyT24ms2BCpBMAlpU0cshARVyupYLYC8_tVGkJCeW9tvZ8ofueqL9ftaoRvLenshmY4HeEMymm8pu5hUgo7mUrfVG0UcqsS91g3jxKVsS1adrPrDDOiPTVmuED6hWLRx25FC.PkU2kyUau_AxGlS4fpW2S8V.xmB4ChjpJXo147FcwLgy5fhk1xyJMwanIpj.lgUHLXHUHUvhVCEav8gyw2CjwvbnuU9pVkmH1FWEu5Wns4PqNhuhfIwRtT0rICBkodcaLsC_UlhfQfXQGLWHIwdTlbMjNvvnP.E4BbBKLXWlsHsv8fp7EhKrX2srF6rfHYWLz6WpRUYTKF1ATPgkRJP1CeoQe.0YlWL'
    response_web = ""
    for IP in range(10):
        response_web = requests.post(url, data=data, headers=headers,timeout=10)
        print(response_web)
        exit()
        if response_web.status_code == 200:
            response_web = response_web.content.decode('utf8')
            break
    print(response_web)
    exit()
    response = json.loads(response_web)
    pages = int(response.get('pAttr').get('pageTotal'))
    print('数据总数：{}页！！！'.format(pages))
    # exit()
    time.sleep(3)
    for page in range(250,pages+1):
        if page == 300:
            break
        data = {
            "search['sKey']": '',
             "search['category']": "yp",
            "search['type']": "CORP",
            "pAttr2['pageCur']": page,
            "pAttr2['infoSize']": 100
        }
        url = "http://mpa.zjfda.gov.cn/xzspajax!listOfInfo.do"
        response_web = ""
        for IP in range(10):
            try:
                response_web = requests.request(method='post', url=url, data = data,headers=headers,proxies=proxys[-1],
                                                timeout=10)
                # print(response)
                if response_web.status_code == 200:
                    response_web = response_web.content.decode('utf8')
                    break
            except Exception:
                dl()
        response = json.loads(response_web)

        results = response.get('list')
        for i in results:
            id = i.get('ID')
            t_name = i.get('TNAME')
            url = "http://mpa.zjfda.gov.cn/xzsp!infoDetail.do?id={}&tableNo={}".format(id,t_name)
            print(url)

            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            }
            response_web = ""
            for IP in range(10):
                try:
                    response_web = requests.request(method='get', url=url, headers=head,
                                                    proxies=proxys[-1],
                                                    timeout=10)
                    # print(response)
                    if response_web.status_code == 200:
                        response_web = response_web.content.decode('utf8')
                        print('break！！！')
                        break
                except Exception:
                    dl()
            try:
                company_name = re.findall(r'企业名称:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                register_addr = re.findall(r'注册地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license = re.findall(r'药品经营（零售）许可证:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                business_addr = re.findall(r'经营地址:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license_mechanism = re.findall(r'证书发放部门:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                business_range = re.findall(r'经营范围:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                legal_people = re.findall(r'法定代表人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                company_principal = re.findall(r'企业负责人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                quality_principal = re.findall(r'质量负责人:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license_valid_date = re.findall(r'经营许可证书发放日期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                license_invalid_date = re.findall(r'经营许可证书有效期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].replace('\t','').replace('\r','').replace('\n','')
                gsp_license_num = re.findall(r'GSP证号:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                gsp_approve_valid_date = re.findall(r'GSP证书发放日期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].strip()
                gsp_approve_invalid_date = re.findall(r'GSP证书有效期:</td>.*?<td>(.*?)</td>', response_web,re.S)[0].replace('\t','').replace('\r','').replace('\n','')
            except Exception as e:
                continue
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            print((id,company_name,register_addr,license,business_addr,license_mechanism,business_range,legal_people,
                   company_principal,quality_principal,license_valid_date,license_invalid_date,gsp_license_num,gsp_approve_valid_date,
                   gsp_approve_invalid_date
                   ))
            if id not in bloom:
                zhilian = Medicine(record_id=id,company_name=company_name,register_addr=register_addr,license=license,business_addr=business_addr
                                   ,license_mechanism=license_mechanism,legal_people=legal_people,
                                   business_range=business_range,company_principal=company_principal,
                                   quality_principal=quality_principal,
                                   license_valid_date=license_valid_date,license_invalid_date=license_invalid_date,gsp_license_num=gsp_license_num,
                                   gsp_approve_valid_date=gsp_approve_valid_date,gsp_approve_invalid_date=gsp_approve_invalid_date,
                                   gmt_created=times, gmt_updated=times)
                sum.append(zhilian)
            time.sleep(1.5)

        time.sleep(2.5)

    if len(sum) == 0:
        print('本次无更新数据！！！')
    else:
        print('本地数据更新了{}条！！！'.format(len(sum)))
        write_db(sum)

def write_db(sum):
    for i in sum:
        session.add(i)
    session.commit()
    session.close()


if __name__ == '__main__':
    main()
