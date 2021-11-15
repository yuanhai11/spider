import requests
import time
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}
# url = 'https://dev.kdlapi.com/api/getipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4'
# res = requests.get(url, headers=headers).json()
# print(res)
#
# url = 'https://dev.kdlapi.com/api/setipwhitelist?orderid=922450652890692&signature=p2u9t67sss8qlqx54aq9bchr1nfso2m4&iplist='
# res = requests.get(url, headers=headers).json()
# print(res)

confirm_ip_url = 'http://soft.data5u.com/wl/myip/fba1729fce7d27397dc2db1dc5db9977.html'
confirm_ip = requests.get(url=confirm_ip_url, headers=headers).text
white_lists_url = 'http://soft.data5u.com/wl/mywhitelist/fba1729fce7d27397dc2db1dc5db9977.html'
white_lists_data = requests.get(url=white_lists_url, headers=headers).text
if confirm_ip not in white_lists_data:
    add_white_url = 'http://soft.data5u.com/wl/setip/fba1729fce7d27397dc2db1dc5db9977.html?ips={}&clear=true'.format(
        confirm_ip)
    res = requests.get(url=add_white_url, headers=headers).text
    time.sleep(70)





