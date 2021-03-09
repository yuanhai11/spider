'''
食品许可证：上海
'''
import re
import time
import requests,pymysql
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def main():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'cookie':'JSESSIONID=B5ECE9D68081169ABEBFC1F0AE464C2A.7'
    }
    data = {
    'tableId': 28,
    'bcId': 152912030752488832300204864740,
    'State': 1,
    'tableName': 'TABLE28',
    'viewtitleName': 'COLUMN212',
    'viewsubTitleName': 'COLUMN210',
    'curstart': 2,
    'tableView': '%E4%BA%92%E8%81%94%E7%BD%91%E8%8D%AF%E5%93%81%E4%BF%A1%E6%81%AF%E6%9C%8D%E5%8A%A1',
    }
    url = "http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?"
    response_web = requests.request(method='post', url=url,data=data, headers=headers,timeout=10).text
    print(response_web)

if __name__ == '__main__':
    main()
