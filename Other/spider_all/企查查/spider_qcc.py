import math
import requests,json,re,time
from lxml import etree

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'cookie':'what ever'
}
proxys = []
def dl():
    '''
    正在测试：是否可以用代理IP进行请求
    想达到稳定的目的。

    :return:
    '''
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    time.sleep(3)
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'https': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main(name):
    response = ""
    url = 'https://www.qcc.com/search?key={}'.format(name)
    while 1:
        try:
            response = requests.request(method='get',url=url,proxies=proxys[-1],headers=headers,timeout=10).text
            if '家符合条件的企业' in response:
                break
            else:
                dl()
        except Exception as e:
            print(e)
            dl()

    company_name = re.findall('data-name="(.*?)".*?data-email="">',response,re.S)
    detail_url = re.findall('onclick="batchPostcardClick.*?" value="(.*?)"',response,re.S)
    if len(company_name) ==0:
        print('{} find no data，跳过'.format(company_name))
    else:
        company_name = ''.join(company_name[0].replace("<em>",'').replace("</em>",''))
        detail_url = 'https://www.qcc.com/firm/' + detail_url[0]
        print(company_name,detail_url)
        time.sleep(1.5)
        if name == company_name:
            while 1:
                try:
                    response_detail = requests.request(method='get', url=detail_url, proxies=proxys[-1],headers=headers, timeout=12).text #
                    if company_name in response_detail:
                        break
                    else:
                        dl()
                except Exception as e:
                    print(e)
                    dl()
            count = re.findall(r'>关联(\d)家企业',response_detail,re.S)[0]
            print('关联企业数：',count)


if __name__ =='__main__':
    dl()
    name = '杭州云核企业管理合伙企业（有限合伙）'
    main(name)


