'''
识别图片中的文字
'''
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# 下面代码为设置端口、忽略证书错误以及指定文件夹
# options.add_argument(('--proxy-server=127.0.0.1:8080'))
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
driver.get('https://web.baimiaoapp.com/')
driver.implicitly_wait(2)

driver.find_element_by_xpath('//div[@class="board-content"]/input').send_keys(r'C:\Users\20945\Desktop\图片\手机号.png')
driver.implicitly_wait(2)

driver.find_element_by_xpath('//div[@class="board-content"]/div[4]').click()
driver.implicitly_wait(2)

driver.find_element_by_xpath('//div[@class="board-content"]/div[4]').click()
data = driver.find_element_by_xpath('//div[@id="quill-container"]/div[1]/p').text
print(data)

