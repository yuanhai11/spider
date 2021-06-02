import requests
import time

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'cookie':'cna=2FIdGFp9A1oCATy6uaKfRDey; tracknick=%5Cu5047%5Cu5982%5Cu4E3A%5Cu7231%5Cu72AF%5Cu7684%5Cu9519; enc=IN0hd4yjt6GF3gyQUYRpO%2BUfTumpOD2BBM7KeGMjW4HzhL2xUl9WFZpZ4%2BY6nIUb3psG%2FF0yqL9VJ%2B4y2KQOiA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; miid=423670081954453422; lgc=%5Cu5047%5Cu5982%5Cu4E3A%5Cu7231%5Cu72AF%5Cu7684%5Cu9519; t=4cf5d664ab1a853276c2e5b25ba1951a; _m_h5_tk=8ecc5882923c837e83181e181997499a_1616143825389; _m_h5_tk_enc=b90c25a9555978a7eba6c740f4f69949; sgcookie=E1006B3w2G8V4v6o403WJH18DzSUZJtlapioRsdS467xxwg0XwaRs17l6eIXMKtrRZJ29L47N422dx8fk1j%2BEkGXfw%3D%3D; uc3=id2=UUGrcetj%2F5jNlw%3D%3D&vt3=F8dCuAoorwKu1OPg6Ig%3D&nk2=30D%2F7R8Bl5%2BcG1rpM4A%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; uc4=id4=0%40U2OcQUxLfBstLgLVlMPDdV4H9aXG&nk4=0%403bTZGnT9uLWeBzQBr7yEKgb8ysKqOt65TA%3D%3D; _cc_=VFC%2FuZ9ajQ%3D%3D; isg=BBgYuoWbzK_KlN_okTaDSr4U6UaqAXyL8pKLVlIItNPy7bPX-hP0GsOEISVdfTRj; lLtC1_=1; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zfvmw%2Fq5v217KPpvlTT5GFx61mzoFnXhP4XXJ4j1NKToIg%2Bb4Ki2DCPbHS7tDjrJWpeh3L39di3LnwTBp8XBpFIA2uOU3Wl%2BQVgiP0vxm5%2B%2B24UponlTplKPknJVjqFRsn2crd5leNC9bxqCRZ78l6m4UaYs%2BxYOf5J1qUm%2F1bhBKvzbMbMqT6S%2BJ%2Bxj2jNeR%2FSxEIaSvE3agBDoBH1QC%2BFhdth767yZIGDdX2fjkXr%2FjvF8sVXW88XNxM%2Bqv3ugU%3D; _samesite_flag_=true; cookie2=16ecd55d84345c2bdfb9e41d84f6796a; _tb_token_=f655e54e733eb',
    # 'cookie':'cq=ccp%3D1; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=E1006B3w2G8V4v6o403WJH18DzSUZJtlapioRsdS467xxwg0XwaRs17l6eIXMKtrRZJ29L47N422dx8fk1j%2BEkGXfw%3D%3D; t=4cf5d664ab1a853276c2e5b25ba1951a; tracknick=%5Cu5047%5Cu5982%5Cu4E3A%5Cu7231%5Cu72AF%5Cu7684%5Cu9519; lid=%E5%81%87%E5%A6%82%E4%B8%BA%E7%88%B1%E7%8A%AF%E7%9A%84%E9%94%99; enc=IN0hd4yjt6GF3gyQUYRpO%2BUfTumpOD2BBM7KeGMjW4HzhL2xUl9WFZpZ4%2BY6nIUb3psG%2FF0yqL9VJ%2B4y2KQOiA%3D%3D; _tb_token_=f655e54e733eb; cookie2=16ecd55d84345c2bdfb9e41d84f6796a; UM_distinctid=1785de577c4dc-0592d66980477b-5771031-1fa400-1785de577c5581; CNZZDATA1000427971=1275951677-1616482808-https%253A%252F%252Fwww.tmall.com%252F%7C1616482808; cna=2FIdGFp9A1oCATy6uaKfRDey; xlly_s=1; pnm_cku822=098%23E1hv%2FpvUvbpvUpCkvvvvvjiWPLdpgjYbPLqpAj3mPmPpljDvPLLWQjE8P2spzjtURpgCvvpvvPMMvvhvC9vhvvCvpv9CvhQvuMpvCluQiNoxdByaUK2ylW9aejnHtb2XSfpAOH2%2BFOcn%2B3CApJFEDaVTRogRD7zyaXTAVAEldUkEnBH%2BCNLpsnm4HFXXiXVvQbT%2Fuvhvmvvv92QatqU9kvhvC99vvOCgpf9Cvm9vvvvvphvvvvvv96CvpvsHvvm2phCvhRvvvUnvphvppvvv96CvpCCvRvhvCvvvvvmevpvhvvmv99%3D%3D; isg=BPn5lItHvbHflmElGREkkH_ECGXTBu24-w3KFRsudSCfohk0Y1b9iGfwJKZUAYXw; l=eBNCSC_PjhYZZt4LBOfanurza77OSIRYYuPzaNbMiOCPOI5B5GzcW6w6GZT6C3GVh6mwR3yf4eUwBeYBq3xonxv9G-QXeLHmn; tfstk=cAkABgNjGUYm2wE-YjdlfYjvPwLhw7YTPiaGBnF1QHKSvz10fvDKOWAbfZeJ2',
    "isUseInventoryCenter":"true",
    "cartEnable":"true",
    "service3C":"false",
    "isApparel":"false",
    "isSecKill":"false",
    "tmallBuySupport":"true",
    "isAreaSell":"true",
    "tryBeforeBuy":"false",
    "offlineShop":"false",
    "itemId":"574055171774",
    "showShopProm":"false",
    "isPurchaseMallPage":"false",
    "itemGmtModified":"1616404494000",
    "isRegionLevel":"true",
    "household":"false",
    "sellerPreview":"false",
    "queryMemberRight":"false",
    "addressLevel":"3",
    "isForbidBuyItem":"false",
    "callback":"setMdskip",
    "timestamp":"{}".format(str(time.time()).replace('.','')[0:13]),
    "isg":"eBNCSC_PjhYZZO09BOfanurza77OSIRYYuPzaNbMiOCP_81B5hIlW6w65NL6C3GVh6mwR3yf4eUwBeYBq3xonxv9G-QXeLHmn",
    "isg2":"BNnZ9EPu3RGHP4GF-fEEcJ8k6MWzZs0Ym60q9fuOVYB_AvmUQ7bd6EcQBMZ0oWVQ",
    "ref":"https://www.tmall.com/",
}

res = requests.request('get',headers=headers,url='https://mdskip.taobao.com/core/initItemDetail.htm?').text
print(res)