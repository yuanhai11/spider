import time
import requests
import base64
#
def get_code():

    headers = {
                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                  "Content-Type":"application/json; charset=utf-8",
    }

    res = requests.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/kaptcha.jpg?v={}".format(0.35730024379260295),

                         headers=headers).content
    with open('1.jpg','wb')as fp:
        fp.write(res)
    ss = base64.b64encode(res).decode()
    data = {"data":ss}
    code = requests.post("http://192.168.2.132:28052/ocr/api/4words/", json=data, headers=headers).json()
    # code = requests.post("http://192.168.2.98:28052/ocr/api/4words/", json=data, headers=headers).json()['data']
    print(code)
    # code_res = requests.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/Yybs/validateYzm.do?yzm={}".format(code),
    #                     headers=headers).text
    # print(code_res)

def get_rsa_key():

    headers = {
                  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                  "Content-Type":"application/json; charset=utf-8",
    }

    local_time = time.localtime(time.time())
    date_format_localtime = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    hours = date_format_localtime.split(" ")[-1].split(":")[0]
    month = date_format_localtime.split(" ")[0].split("-")[1]
    year = date_format_localtime.split(" ")[0].split("-")[0]
    day = date_format_localtime.split(" ")[0].split("-")[2]
    if month.startswith("0"):
        month = month[1]
    date = year+"-"+month+"-"+day+"-"+hours
    keys = requests.get("https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/main/util/publicKey.js?v={}".format(date),
     headers=headers).text
    import re
    k =  re.findall(r'publicNewKey = "(.*?)"',keys)[0]
    return k

def get_encode():
    pass



# def get_cookie():
#
#     retStr = client.doGetRequest(
#         "https://etax.zhejiang.chinatax.gov.cn/zjgfdzswj/LoginController/loginBsry.do?username=" + taxUserVO.getUuid() + "&password=" + Utils.urlEncode(
#             ePwd,
#             "utf-8") + "&loginType=PWD&service=https%3A%2F%2Fetax.zhejiang.chinatax.gov.cn%2Fzjgfdzswj%2Fmain%2Fhome%2Fwybs%2Findex.html",
#         map);

if __name__ == '__main__':
    pass
    get_code()
    # get_rsa_key()