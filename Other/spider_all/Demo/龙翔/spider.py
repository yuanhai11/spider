'''
新增数据获取
'''
import time,re,json
import requests,pymysql
from lxml import etree
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    # 'cookie': 'TYCID=435e2b701e3f11eb93fd6b29e729c6c7; ssuid=8413289216; _ga=GA1.2.1495606244.1604454265; jsid=SEM-BAIDU-PZ-SY-20201109-BIAOTI; __insp_slim=1606196162867; __insp_wid=677961980; __insp_nv=true; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnkvNDAzNDM3NDI5NT9mcm9tPWYz; __insp_norec_sess=true; tyc-user-info={%22claimEditPoint%22:%220%22%2C%22vipToMonth%22:%22false%22%2C%22explainPoint%22:%220%22%2C%22personalClaimType%22:%22none%22%2C%22integrity%22:%2210%25%22%2C%22state%22:%220%22%2C%22score%22:%2296%22%2C%22announcementPoint%22:%220%22%2C%22messageShowRedPoint%22:%220%22%2C%22bidSubscribe%22:%22-1%22%2C%22vipManager%22:%220%22%2C%22onum%22:%220%22%2C%22monitorUnreadCount%22:%220%22%2C%22discussCommendCount%22:%220%22%2C%22showPost%22:null%2C%22messageBubbleCount%22:%220%22%2C%22claimPoint%22:%220%22%2C%22token%22:%22eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA%22%2C%22schoolAuthStatus%22:%222%22%2C%22userId%22:%2235705210%22%2C%22scoreUnit%22:%22%22%2C%22redPoint%22:%220%22%2C%22myTidings%22:%220%22%2C%22companyAuthStatus%22:%222%22%2C%22originalScore%22:%2296%22%2C%22myAnswerCount%22:%220%22%2C%22myQuestionCount%22:%220%22%2C%22signUp%22:%220%22%2C%22privateMessagePointWeb%22:%220%22%2C%22nickname%22:%22%E5%B8%8C%E6%8B%89%E7%91%9E%C2%B7%E8%BE%BE%E8%8A%99%22%2C%22privateMessagePoint%22:%220%22%2C%22bossStatus%22:%222%22%2C%22isClaim%22:%220%22%2C%22yellowDiamondEndTime%22:%220%22%2C%22yellowDiamondStatus%22:%22-1%22%2C%22pleaseAnswerCount%22:%220%22%2C%22bizCardUnread%22:%220%22%2C%22vnum%22:%220%22%2C%22mobile%22:%2218837076355%22%2C%22riskManagement%22:{%22servicePhone%22:null%2C%22mobile%22:18837076355%2C%22title%22:null%2C%22currentStatus%22:null%2C%22lastStatus%22:null%2C%22quickReturn%22:false%2C%22oldVersionMessage%22:null%2C%22riskMessage%22:null}}; tyc-user-info-save-time=1607665672908; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODgzNzA3NjM1NSIsImlhdCI6MTYwNzY2NTY3MSwiZXhwIjoxNjM5MjAxNjcxfQ.8vTjN_t0do4-kc7o2qO5O7f6ujh3J4Ek7jHHSXtjv_YiGQ6jTyS_aRrKUv4i9kN2DIKZcDvrk_gthbsLfP7ZjA; tyc-user-phone=%255B%252218837076355%2522%252C%2522188%25206870%25207561%2522%255D; csrfToken=TVDKWScW3kb0cIWylXkBTid6; Hm_lvt_e9ceb92f9ef221e0401c0d5b35aa93f1=1608283877,1608514528; _gid=GA1.2.587846859.1608514528; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1607997927,1608097031,1608194729,1608520205; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1608520205; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22175cea83fe26fa-0ea05bfb98414a-930346c-2073600-175cea83fe3ccd%22%7D; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e9ceb92f9ef221e0401c0d5b35aa93f1=1608520274'
}

def main3():

    month = '03'

    url = 'https://www.520mojing.com/'
    response = requests.request(method='get', url=url,headers=headers,timeout=10).text
    print(response)
    from lxml import etree

    tree = etree.HTML(response)
    s = tree.xpath("//img")

if __name__ == '__main__':
    main3()



