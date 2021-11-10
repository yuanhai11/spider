import requests
import re,time


def get_token():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    # options.add_argument(('--proxy-server=http://{}'.format(proxys[-1])))
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
    # 下面代码为避免网站对selenium的屏蔽
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 以设定好的方式打开谷歌浏览器
    driver = webdriver.Chrome(executable_path=r'E:\chrome_downloading\chromedriver_win32\chromedriver.exe',options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => undefined
           })
     """
    })

    driver.get('https://www.zhipin.com/c101210100-p100120/')
    time.sleep(3)
    token = str(driver.get_cookies()[0]).split('value')[-1].replace('/','').replace(':','').replace('}','')[3:-1]
    print(token)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'cookie': 'lastCity=101210100; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1620870236,1620955629,1621222868,1621320356; __g=-; __l=l=%2Fwww.zhipin.com%2Fc101210100-p100120%2F&s=3&friend_source=0&s=3&friend_source=0; __c=1621320357; __a=70004417.1619060840.1621222868.1621320357.247.14.61.247; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1621321090;__zp_sseed__=yXnA6Qkzwpe0iyPF5CTRs2pBvJBtHgqltSWXV+i6SCM=; __zp_sname__=c8e6fbc4; __zp_sts__=1621321090493;__zp_stoken__={}'.format(
            token)
    }
    # driver.close()
    return headers

def dl():
    dlurl = 'http://api.goubanjia.com/dynamic/get/d490a5d4debefc8980ae6ee4c4148552.html?sep=3'
    resp = requests.get(dlurl).text
    resp = re.sub(r'\n', '', resp)
    proxy = {
        'http': resp
    }
    proxys.append(proxy)
    print(proxys[-1])

def main():
    headers = get_token()
    # token = '7ddfpVjWOwaoZjRIB6fhgIhZY%2FGHP6K%2Bhz5%2FOII2jK8twjorjFDfx6JruZAF%2Fcc7McmQ2d815omoEyN4xALzECdWQfw%2BF2h1%2FSl04a5DJ1j2tEgDf1TAxRxn2cxrAB7PtC30iImak65N16aeWRY8C8m5moiJmpOuTdemnlkWPAvJuZo%3D'
    # token =   '5bc4cKRgcPn8oHwFRL0BgQGAPTyUwHEJASDp%2FQ38wM1QmaXtuOR9TIj4WDgJYQHMtT0xuSAQcNzdfBhY2QWN5H1FRVnwhbHh0Igs7LxoUam8KXyBXDAYlRF9%2FcSMlTAUEf29%2BdQ4cVkhVNk0W'
    # token=       '059dcW3FzWnJ1eyhUaQZMXg8HNAFVR2QrRiB3OG9OBF1BDXheIHszYWtqW39%2BQUJsLTsPOmNsWVUwencFNE5ccGgWRRg4Gm1Bc3dvEmhweWNjekFxQ0AfFjoDFE9Zb2IRHRgfB0M%2FX1RNOGUl'

    while 1:
        time.sleep(2.6485)
        data = requests.request('get', headers=headers, url='https://www.zhipin.com/job_detail/?query=%E6%B5%99%E6%B1%9F%E4%B8%AD%E7%A6%84%E8%B4%A2%E5%8A%A1%E5%92%A8%E8%AF%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&city=101210100&industry=&position=140399',
                               ).text  # 拿到第一次的cookie后，再次发出4次请求后即失效。
        from lxml import etree
        data = etree.HTML(data)
        ele_len = data.xpath("//a[@ka='search_list_company_1_custompage']/text()")
        print(ele_len)

if __name__ == '__main__':
    proxys = []
    # dl()
    main()

