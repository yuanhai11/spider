import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    'Accept': '/*',
    'Referer': 'https://www.nta.go.jp/about/organization/sapporo/statistics/h30/sake.htm',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-platform': 'Windows',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0'

}

res = requests.request('get',"https://www.meti.go.jp/policy/economy/hyojun/techno_infra/14_gaiyou_ryoumoku.html", headers=headers).content

print(res)

with open('aa.html','wb')as fp:
    fp.write(res)
