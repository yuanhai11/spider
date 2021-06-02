import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# 下面代码为设置端口、忽略证书错误以及指定文件夹
# options.add_argument(('--proxy-server=127.0.0.1:8080'))
# options.add_argument("--ignore-certificate-errors")
# options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
# No_Image_loading = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", No_Image_loading)
# 下面代码为避免网站对selenium的屏蔽
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# options.add_argument("'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'")

# 以设定好的方式打开谷歌浏览器
driver = webdriver.Chrome(executable_path=r'E:\chrome_downloading\chromedriver_win32\chromedriver.exe',options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
       Object.defineProperty(navigator, 'webdriver', {
         get: () => False
       })
 """
})

driver.get('http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=41&tableName=TABLE41&title=%D2%A9%C6%B7%BE%AD%D3%AA%C6%F3%D2%B5&bcId=152911863995882985662523838679&CbSlDlH0=qGrqqqq8ofg8ofg8o93CR3Yb8uvn44yRM.Wgtg1syRWqqrg')
time.sleep(2)
driver.refresh()

driver.find_element_by_xpath('//div[@id="content"]//table[4]/tbody/tr/td[4]').click()
time.sleep(10)
driver.find_element_by_xpath('//div[@id="content"]//table[4]/tbody/tr/td[5]').click()
time.sleep(1)
driver.find_element_by_xpath('//div[@id="content"]//table[4]/tbody/tr/td[5]').click()
time.sleep(1)
print(driver.page_source)
