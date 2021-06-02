import time
import requests

headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8',
'cache-control': 'no-cache',
'Connection': 'keep-alive',
'Content-Length': '343',
    'Content-Type': 'application/x-www-form-urlencoded',
    'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'Referer': 'http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=41&tableName=TABLE41&title=%D2%A9%C6%B7%BE%AD%D3%AA%C6%F3%D2%B5&bcId=152911863995882985662523838679&CbSlDlH0=qGcqkakxnQvxnQvxnV3CRpz.vd5v8JRkxJS1hw645QqqqW9'
    ,'cookie':"JSESSIONID=4B69F39D026617DAABA4F7F2A2E4DB6E.7; neCYtZEjo8GmS=5JBX7VuGSQ2sDmmoW7TGKrz.QA3Ua2w3N8qjn0cY2PmDzUulu0FV7eG3A_8_NQX97h34yoeKUf14juAvRGoEeNG; UM_distinctid=176cc4efd8b169-016e6b9e061161-c791039-1fa400-176cc4efd8c4c9; neCYtZEjo8GmT=53ma..DrQhkQqqqmgFr5tUagUZQxqaBsXiLFL_x8v9yXeOGQsYZOyvx399PwK9JsiVASNXsWOPO5zYxPCwM4ruPnED4G44Tk.tHoDHcowowD_txZDgL97jyLCgAtF5hCRnAcbMos5vvCHaQOxrklcBxgEbpBcvKWdkFBDXEXcuscJBJBSoh6SUlhVoGkAQcsFnpc80c1WUnilidBIPfJ.6UEC8MCXpRkZAWONsFmWOPvOZxk6sX7nblhPmtMupq00D1cJJN3eRmXpv1.bUZVdBXXfp_mhgs4Bz7Je0iFmAdBMMwZMexmLLYFwCUePX4lRW"
}

# url = 'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?tableId={}&State=1&bcId={}&State=1&curstart={}&State=1&tableName={}&State=1&viewtitleName={}&State=1&viewsubTitleName={}&State=1&tableView={}&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'.format(
#     41,'152911863995882985662523838679',9,'TABLE41','COLUMN438','COLUMN437','%E8%8D%AF%E5%93%81%E7%BB%8F%E8%90%A5%E4%BC%81%E4%B8%9A')
url = 'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?tableId=25&bcId=152904713761213296322795806604&curstart=1'
res = requests.request(method='post',url=url,headers= headers,timeout=10)
print(res)