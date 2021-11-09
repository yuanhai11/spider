# import requests
# import random
# MY_USER_AGENT = [
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
#     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
#     "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
#     "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
#     ]
# headers = {
#     'user-agent':random.choice(MY_USER_AGENT),
#     'cookie':'__jsluid_h=82fe16f5c29ceec3158cde6ca30b1702; SECTOKEN=7456514189471517975; __jsl_clearance=1624238402.194|0|a3Xp7y5CZMIrflcejCzQGtQjf0E%3D; JSESSIONID=c21c6a2c98ed768ebae6650e9340; gsxtBrowseHistory1=%0FS%04%06%1D%04%1D%10SNS%24%26%3B%22%3D%3A71%3A%3B01%3A%219%40ADDDDE%40ADDDEDD%40FCCCMCL%40SXS%11%1A%00%1A%15%19%11SNS%E8%A4%8B%E6%9F%A3%E5%8F%8B%E7%BA%8B%E4%B8%BF%E6%BB%A4%E6%B1%80%E6%9F%A8%E4%BB%93%E9%95%B4%E5%87%A8%E6%B1%A5%E4%B9%A7%E4%B9%AE%E5%91%BC%E4%BC%A8%E7%A5%8ASXS%11%1A%00%00%0D%04%11SNMEDDXS%02%1D%07%1D%00%00%1D%19%11SNEBF%40FGLFDF%40AL%09; gsxtBrowseHistory2=%0FS%04%06%1D%04%1D%10SNS%24%26%3B%22%3D%3A71%3A%3B01%3A%219GEDDDDGEDEEADDDDFFDEADGF%40DDGD%40SXS%11%1A%00%1A%15%19%11SNS%E4%B9%BE%E6%B4%83%E4%B9%B3%E8%BF%8A%E7%BC%A5%E7%BA%A8%E9%86%A5%E8%9F%B9%E6%9D%B9%E5%8B%95%E6%9D%BD%E9%98%A4%E5%84%98%E5%8E%8CSXS%11%1A%00%00%0D%04%11SNEEMDXS%02%1D%07%1D%00%00%1D%19%11SNEBF%40FGMG%40CLCC%09; tlb_cookie=S172.16.12.71'
#
# }
#
# print(headers)
# data = {
#     # 'province': 100000,
#     'searchword': '上海万达网络金融服务有限公司',
#     'token': 109990349,
#     # 'tab':
#     'geetest_challenge': '72431a1dfc2b515bab707608139feb94',
#     'geetest_validate': '4ec698eba7f361f25fdd9067dd030f8b',
#     'geetest_seccode': '4ec698eba7f361f25fdd9067dd030f8b|jordan'
# }
# d = requests.request(method='post',headers=headers,url='http://www.gsxt.gov.cn/corp-query-search-1.html',data=data ).text
# print(d)

import hashlib
import json
import re
import execjs
import requests

def get_hash256(data: str):
    hash256 = hashlib.sha256(data.encode('utf-8'))
    return hash256.hexdigest()


def get_hashsha1(data:str):
    sha = hashlib.sha1(data.encode('utf-8'))
    return sha.hexdigest()

def get_hashmd5(data:str):
    hl = hashlib.md5(data.encode('utf-8'))
    return hl.hexdigest()

def get_cookies():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.gsxt.gov.cn',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }

    url1 = 'http://www.gsxt.gov.cn/SearchItemCaptcha?'


    # proxies = {'http': 'http://'+host+':'+port+''}
    # print(proxies)

    r1 = requests.get(url1, headers=headers, verify=False)

    js = r1.text
    js = js.replace('<script>document.cookie=', '').replace(';location.href=location.pathname+location.search</script>', '')
    result=execjs.eval(js)

    __jsluid_h = r1.headers['Set-Cookie']
    __jsl_clearance = result

    cookies = {
        '__jsluid_h': __jsluid_h.replace('__jsluid_h=', ''),
        '__jsl_clearance': __jsl_clearance.replace('__jsl_clearance=', '')
    }

    url2 = 'http://www.gsxt.gov.cn/index.html'
    r2 = requests.get(url2, headers=headers,verify=False, cookies=cookies)

    data_org = re.findall(';go(.*)</script>', r2.text)[0]
    data = {"bts":["1624255820.461|0|NnX","XjUHU1prYon6Er6YhGot4Y%3D"],"chars":"RNvGJxaamMqWZKFlnjfuSx","ct":"9abb4a904d47983f3dd340c390608b26e466900aab471fee004b349e5f456c7b","ha":"sha256","tn":"__jsl_clearance","vt":"3600","wt":"1500"}
    # data = data_org.replace('(', '').replace(')', '')

    # data = json.loads(data_org)

    bts = data['bts']
    chars = data['chars']
    ct = data['ct']
    ha = data['ha']
    vt = data['vt']

    counti = 0
    countj = 0
    if ha == 'sha256':
        print('加密算法-' + ha)
        for i in range(len(bts[0])):
            for j in range(len(chars)):
                cookieTemp = bts[0] + chars[i] + chars[j] + bts[1]
                if get_hash256(cookieTemp) == ct:
                    counti = i
                    countj = j
                    break
    elif ha == 'sha1':
        print('加密算法-' + ha)
        for i in range(len(bts[0])):
            for j in range(len(chars)):
                cookieTemp = bts[0] + chars[i] + chars[j] + bts[1]
                if get_hashsha1(cookieTemp) == ct:
                    counti = i
                    countj = j
                    break
    elif ha == 'md5':
        print('加密算法-' + ha)
        for i in range(len(bts[0])):
            for j in range(len(chars)):
                cookieTemp = bts[0] + chars[i] + chars[j] + bts[1]
                if get_hashmd5(cookieTemp) == ct:
                    counti = i
                    countj = j
                    break

    __jsl_clearance = bts[0] + chars[counti] + chars[countj] + bts[1]
    __jsl_clearance = __jsl_clearance +';max-age='+vt +';'
    print(__jsl_clearance)
    exit()
    cookies1 = {
        '__jsluid_h': __jsluid_h.replace('__jsluid_h=', ''),
        '__jsl_clearance': __jsl_clearance,
    }
    url3 = 'http://www.gsxt.gov.cn/index.html'
    r3 = requests.get(url3, headers=headers, verify=False, cookies=cookies1)

    r3cookies = r3.headers['Set-Cookie']
    r3cookies = r3cookies.split(',')
    JSESSIONID = ''
    SECTOKEN = ''
    tlb_cookie = ''
    for i in r3cookies:
        if 'JSESSIONID' in i:
            JSESSIONID = i.replace('JSESSIONID=', '').strip()
        if 'SECTOKEN' in i:
            SECTOKEN = i.replace('SECTOKEN=', '').strip()
        if 'tlb_cookie' in i:
            tlb_cookie = i.replace('tlb_cookie=', '').strip()
    # cookies2为取数据所需要的cookie
    cookies2 = {
        '__jsluid_h': __jsluid_h.replace('__jsluid_h=', ''),
        '__jsl_clearance': __jsl_clearance,
        'JSESSIONID': JSESSIONID,
        'SECTOKEN': SECTOKEN,
        'tlb_cookie': tlb_cookie,
    }
    print(cookies2)

    # url3 = 'http://www.gsxt.gov.cn/SearchItemCaptcha?'
    # r3 = requests.get(url3, headers=headers, verify=False, cookies=cookies1).text
    # print(r3)

    url7 = 'http://www.gsxt.gov.cn/affiche-query-area-info-paperall.html?noticeType=11&areaid=100000&noticeTitle=&regOrg=110000'
    form_data = {
        "draw": 1, "start": 0, "length": 10
    }
    r7 = requests.post(url7, headers=headers, data=form_data,verify=False, cookies=cookies2)
    print(r7.text)

if __name__ == '__main__':
    get_cookies()
