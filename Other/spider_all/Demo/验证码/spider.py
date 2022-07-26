import ddddocr

ocr = ddddocr.DdddOcr(old=True)

import requests

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}
d = requests.get("https://puser.zjzwfw.gov.cn/sso/usp.do?action=verifyimg",
             headers = headers).content
with open("test.jpg",'wb')as fp:
    fp.write(d)

with open("test.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)
print(res[-4:])
