import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def web_d():

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
    driver.get('https://bj.58.com/job/')
    driver.maximize_window()
    time.sleep(3)
    for company_name in ['北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司',
                         '北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司',
                         '北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司',
                         '北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司',
                         '北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司',
                         '北京青苗永兴商贸有限公司','北京永兴通岱信息科技有限公司','北京蓝萨科技有限公司','浙江中禄财务咨询有限公司']:
        driver.find_element_by_id("keyword").clear()
        time.sleep(3)
        driver.find_element_by_id('keyword').send_keys(company_name)
        driver.find_element_by_id('searchbtn').click()
        time.sleep(2)
        from lxml import etree
        tree = etree.HTML(driver.page_source)
        company_lists = tree.xpath("//div[@class='comp_name']/a/@title")
        print(company_lists)
        if company_name in company_lists:
            print(company_name,1)
        else:
            print(company_name,0)

if __name__ == '__main__':
    web_d()