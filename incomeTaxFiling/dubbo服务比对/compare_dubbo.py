# encoding=utf-8
# 加入pywintypes，打包成功
import time

import win32api
import win32con
# 加入pywintypes，打包成功
# 导入config里的变量信息
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    options = Options()
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    #  开启无头模式，浏览器窗口不太好看。默认不开启
    # options.add_argument('--headless')  # 无头
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-javascript')
    # options.add_argument('--disable-software-rasterizer')
    # options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-extensions")
    options.add_argument(
        "–user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'")
    options.add_argument("-incognito")  # 无痕
    # options.add_argument("–window-size=1200,768")
    # options.add_argument(('--proxy-server=http://{}'.format(proxys[-1])))
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
    # 下面代码为避免网站对selenium的屏蔽
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 以设定好的方式打开谷歌浏览器
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\20945\Downloads\Compressed\chromedriver_win32_2\chromedriver.exe',
        options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
           Object.defineProperty(navigator, 'webdriver', {
             get: () => undefined
           })
     """
    })
    driver.get("http://121.196.16.204:29000/dubbo-admin-2.5.10/governance/applications/saas-provider/services")
    # win32api.PostMessage("nihao") root root
    win32api.keybd_event(16, 0, 0, 0)
    win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)
    # root
    win32api.keybd_event(82, 0, 0, 0)
    win32api.keybd_event(82, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(79, 0, 0, 0)
    win32api.keybd_event(79, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(79, 0, 0, 0)
    win32api.keybd_event(79, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(84, 0, 0, 0)
    win32api.keybd_event(84, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)

    win32api.keybd_event(9, 0, 0, 0)
    win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)

    # root
    win32api.keybd_event(82, 0, 0, 0)
    win32api.keybd_event(82, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(79, 0, 0, 0)
    win32api.keybd_event(79, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(79, 0, 0, 0)
    win32api.keybd_event(79, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(84, 0, 0, 0)
    win32api.keybd_event(84, 0, win32con.KEYEVENTF_KEYUP, 0)

    # 发送回车
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    # print(driver.page_source)
    # S = Select(driver.find_element_by_xpath('//table[@id="table_o"]//tr[1]/th[3]//select')).select_by_value("provided")
    gaga = driver.page_source
    tree = etree.HTML(gaga)
    lists = tree.xpath("//a//text()")
    # print(lists)
    lists_filter = [i for i in lists if "com.jizhang.saas" in i]
    # print(lists_filter)
    con = aa()

    more = []
    less = []

    for j in lists_filter:
        if j not in con:
            more.append(j)

    for j in con:
        if j not in lists_filter:
            less.append(j)

    # print(more)
    # print(less)
    driver.close()
    if len(more) != 0:
        for i in more:
            con.append(i)
        bb(con)
    alert(more, less)


def bb(con):
    with open(r"C:\Users\20945\Desktop\dubbo.txt", 'w')as fp:
        fp.write(str(con))


def aa():
    with open(r"C:\Users\20945\Desktop\dubbo.txt")as fp:
        con = eval(fp.read())
    return con


def alert(more, less):
    import pyautogui
    a = pyautogui.alert(text='本次上线:\n service新增：【{}】 \n service缺少：【{}】'.format(more, less), title='Fuck')
    print(a)


if __name__ == '__main__':
    main()
    # print(aa())
    # alert([],['com.jizhang.saas.bizlog.BizLogService1:prod'])
    # bb(["a","b"])
