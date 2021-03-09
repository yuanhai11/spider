'''
:argument
    标题 job_title
    薪资 salary
    工作详情URL work_detail_url
    工作区域 work_area
    工作地点 work_position
    工作经验 work_experience
    学历要求 education
    福利待遇 social_benefits
    公司名称 company_title
    经营类型 management_type
    人员数量 person_number
    公司详情 company_detail_url
    技能要求 skill_requirement
'''
import time
import json
import pymysql
import requests
import time
import random
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()
# 定义Zhilian对象:
class ZhiLian(Base):
    # 表的名字:
    __tablename__ = 'zhi_lian'

    # 表的结构:
    id = Column(Integer(), primary_key=True,autoincrement=True)
    job_title = Column(String(20))
    salary = Column(String(20))
    work_detail_url = Column(String(100))
    work_area = Column(String(20))
    work_experience = Column(String(20))
    education = Column(String(20))
    social_benefits = Column(String(60))
    company_title = Column(String(20))
    management_type = Column(String(20))
    person_number = Column(String(20))
    company_detail_url = Column(String(100))
    gmt_created = Column(String(20))
    gmt_updated = Column(String(20))
def sqlachmy_db(data):
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/spider')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    ses = DBSession()
    for i in data:
        ses.add(i)
        ses.commit()
    ses.close()
def insert_into(data):
    global sum
    for i in data:
        job_title = i[0][0]
        salary = i[1][0]
        work_detail_url = i[2][0]
        work_area = i[3][0]
        work_experience = i[4][0].strip()
        education = i[5][0]
        social_benefits = "".join(i[6])
        company_title = i[7][0]
        management_type = i[8][0]
        person_number = i[9][0]
        company_detail_url = i[10][0]

        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        gmt_created, gmt_updated = times, times

        sql = """insert into zhi_lian (id,job_title,salary,work_detail_url,work_area,work_experience,education,social_benefits,company_title,management_type,person_number,
                    company_detail_url,gmt_created, gmt_updated)values(NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""" \
            .format(job_title, salary, work_detail_url, work_area, work_experience, education, social_benefits,
                    company_title, management_type, person_number,
                    company_detail_url, gmt_created, gmt_updated)
        cursor.execute(sql)

    db.commit()
    sum = []


def parse_data(driver):

    response = etree.HTML(driver.page_source)
    res_lists = response.xpath('//div[@class="contentpile__content__wrapper clearfix"]')
    for i in res_lists:
        job_title = i.xpath('./div/a/@title')[0]
        salary = i.xpath('.//p[@class="contentpile__content__wrapper__item__info__box__job__saray"]/text()')[0]
        work_detail_url = i.xpath('./div/a/@href')[0]
        work_area = i.xpath(
            './/div[@class="contentpile__content__wrapper__item__info__box__job jobDesc"]/ul/li[1]/text()')[0]
        work_experience = i.xpath(
            './/div[@class="contentpile__content__wrapper__item__info__box__job jobDesc"]/ul/li[2]/text()')[0].strip()
        education = i.xpath(
            './/div[@class="contentpile__content__wrapper__item__info__box__job jobDesc"]/ul/li[3]/text()')[0]
        social_benefits = "".join(i.xpath(
            './/div[@class="contentpile__content__wrapper__item__info__box__welfare job_welfare"]//text()'))
        company_title = i.xpath(
            './/a[@class="contentpile__content__wrapper__item__info__box__cname__title company_title"]/text()')[0]
        management_type = i.xpath(
            './/span[@class="contentpile__content__wrapper__item__info__box__job__comdec__item"][1]/text()')[0]
        person_number = i.xpath(
            './/span[@class="contentpile__content__wrapper__item__info__box__job__comdec__item"][2]/text()')[0]
        company_detail_url = i.xpath(
            './/a[@class="contentpile__content__wrapper__item__info__box__cname__title company_title"]/@href')[0]
        print((
            job_title, salary, work_detail_url, work_area, work_experience, education, social_benefits, company_title,
            management_type, person_number, company_detail_url))

        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        zhilian = ZhiLian(job_title=job_title, salary=salary, work_detail_url=work_detail_url, work_area=work_area,
                          work_experience=work_experience, education=education, social_benefits=social_benefits, company_title=company_title,
                          management_type=management_type, person_number=person_number, company_detail_url=company_detail_url, gmt_created=times,
                          gmt_updated=times)
        sum.append(zhilian)
    sqlachmy_db(sum)

def main():
    options = Options()
    # 下面代码为设置端口、忽略证书错误以及指定文件夹
    # options.add_argument(('--proxy-server=127.0.0.1:8080'))
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--user-data-dir=C:\\Users\\20945\\Desktop\\data')
    # 下面代码为避免网站对selenium的屏蔽
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # 以设定好的方式打开谷歌浏览器
    # webdriver.Firefox(executable_path=)
    driver = webdriver.Chrome(executable_path=r'D:\wxt-new\chromedriver_win32\chromedriver.exe',options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
  """
})
    driver.get('https://passport.zhaopin.com/login?bkUrl=%2F%2Fi.zhaopin.com%2Fblank%3Fhttps%3A%2F%2Fwww.zhaopin.com%2F')
    time.sleep(100000)
    # driver.find_element_by_xpath('//div[@class="zppp-panel-qrcode-bar__img"]').click()
    # time.sleep(1)
    # driver.find_element_by_xpath('//li[@class="zppp-panel-tab"]').click()
    # time.sleep(1)
    # driver.find_element_by_xpath('//input[@id="input_6YLMN"]').send_keys('18837076355')
    # time.sleep(1)
    # driver.find_element_by_id('//input[@id="input_73K6T"]').send_keys('wxt906906')
    # time.sleep(15)
    url = 'https://sou.zhaopin.com/?p=1&jl=653&sf=0&st=0&kw=Java%E5%BC%80%E5%8F%91&kt=3'
    driver.get(url)
    time.sleep(3)

    while 1:
        parse_data(driver)
        try:
            # 滚轮 滑到页面底部
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(6)
            driver.find_element_by_xpath('//button[@class="btn soupager__btn"]').click()
            time.sleep(5)
        except Exception as e:
            break

    # driver.close()


if __name__ == '__main__':
    sum = []
    db = pymysql.connect(host='192.168.2.222', password='123456', database='spider', user='root')
    cursor = db.cursor()
    main()
    db.close()