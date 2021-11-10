import requests
import time
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
url = 'https://dev.kdlapi.com/api/getipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4'
res = requests.get(url, headers=headers).json()
print(res)

url = 'https://dev.kdlapi.com/api/setipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4&iplist='
res = requests.get(url, headers=headers).json()
print(res)








