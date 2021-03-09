import json,time
import requests
from lxml import etree
from threading import Thread

sum = []

def spider1():
    for page in range(1,21):
        url = "http://www.bookschina.com/kinder/46000000_0_0_11_0_1_{}_0_0_/".format(page)
        headers = {
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
        response = requests.request(method='get',url=url,headers=headers).text
        response = etree.HTML(response)
        book_name = response.xpath('//div[@class="bookList"]/ul/li[1]//h2[@class="name"]/a/text()')
        print(book_name)
        time.sleep(2)
def spider2():
    for page in range(1,21):
        url = "http://www.bookschina.com/kinder/46000000_0_0_11_0_1_{}_0_0_/".format(page)
        headers = {
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
        response = requests.request(method='get',url=url,headers=headers).text
        response = etree.HTML(response)
        book_name = response.xpath('//div[@class="bookList"]/ul/li[1]//h2[@class="name"]/a/text()')
        print(book_name)
        time.sleep(2)

def spider():
    for page in range(1,41):
        url = "http://www.bookschina.com/kinder/46000000_0_0_11_0_1_{}_0_0_/".format(page)
        headers = {
            'user_agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
        }
        response = requests.request(method='get',url=url,headers=headers).text
        response = etree.HTML(response)
        li_lists = response.xpath('//div[@class="bookList"]/ul/li')
        for li in li_lists:
            book_name = li.xpath('.//h2[@class="name"]/a/text()')[0]
            print(book_name)
            sum.append(book_name)
            time.sleep(0.1)
        time.sleep(1)

if __name__ == '__main__':
    start  = time.time()
    t1 = Thread(target=spider1)
    t2 = Thread(target=spider2)
    t1.start()
    t2.start()
    end = time.time()

    print(end-start)

