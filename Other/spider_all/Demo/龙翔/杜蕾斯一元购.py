
import time

import requests

def main():
    result_list = []
    while 1:
        if len(result_list) >= 10:
            for index, i in enumerate(result_list):
                if i.done():
                    result_list.remove(result_list[index])
            time.sleep(1)
            continue
        result = executor.submit(run)
        result_list.append(result)

def run():

    url = "https://api.m.jd.com/client.action"

    payload = 'functionId=centerReceiveCoupon&body=%7B%22extend%22%3A%220AD05650024676E8B98A0CCA4D559C9541FDFB6BA97ED401DD7040DD97D81004B02187C8ED1FE5C84DA470B0C96C01BAB1DA7F79BF316E599EA2B24106BE59DE6B8A6160AC012ADDDE7362D4FAC56DBE4D16DA5371A98D254B38463F15EE94E547ABA2B1C26F0E78A475DB7E2EAC9CE9B6C0DA5E57AFF2165E49E8734D1DEAB675F838E2BC1B086A5B0BBD0306869BCFEEBD2B5CE1D79AF1B1599E5E3902201557823A172A2572C1A0ACE8A16CCA4D2B8A924DD43CDA287F42500680E9863E4C14405032DBE9E9E8783025EEB5A8250D3BF1611BFA19E40CDDC876733FD3F9A8%22%2C%22rcType%22%3A%221%22%2C%22source%22%3A%22couponCenter_app%22%2C%22random%22%3A%226472801%22%2C%22couponSource%22%3A%221%22%2C%22extraData%22%3A%22%7B%5C%22log%5C%22%3A%5C%221656050401110~1RPGhWTr9zTMDFVWXNiSDAxMQ%3D%3D.ZG9GVHhgaUBWfmdrRRxxY2BBBS09ODkUNmR1RU59eWgNUDZkJxsufTQ9RA84JRcbFjwhKkMTCRc%2FEiMZKw%3D%3D.aa4408a3~5%2C1~B18EAABA70A7C53E04C9EA0CA08E340C5A454D7E~0hvv347~C~SRRMVBAKbGgVGkxfVBAMYxtWBRoMdRQOdBUDAQhrHgEZBQkIFEUbHhRcDh8JexkPfRQADgAFFAgcAAcFFUwabBUQUUpXEAoGGRtLSxMDEAcODAQAAgUKDAwACwEPAAwCEhsXTl1cEwMQQkxNRkQVGRtPXVAbCBReX0ZEQ0FMWRodG0JSVhsIawMZAQ0LHQ8eBwkVAxwCaBUaUlsbCAcUG1FDFQ8bDAEGWlNQWwgBA1VTCFwBAlsEAF0PVwAHBwtaXVIJBAUaFRBeRxcDGnRYV0dOGFhTQlRdDwwaHRtGFAIIBAUBBQwIDAEIAwcIFRBaXBcDGhVUWlYGAV9QUlICXAkVBQACAQEJUwQHAA8JDwQBCxtdDgoCAAIBDwsACwJTD1gDAFIBAVwOVV9XVwwNAgABVA5dW1QJEBoaX0JSFQ8bUHQEWFYBVUlCfl9BTUxLAUhzdF5Yc2EVGRtWThMDEHFXVlVcUhVwVlsfGx4UVlhEEg0XAA8NBwwQGhpKUUIVD2IOAQgVAQ8LZB4SRVobAmMTdHsWDhseElZbXUpXWF0QGhoAEBwVBAgWCB8LEBoaAAUFAQAbFBoJCgQFDgoEAwIGDQsIAgoBBAsBAQgEDAoICwkKHw4LfQAFAQYPDA4BCgsFDg8ABgUDDA4PAgwEBwsbHhIGF2QUGlhWUxQCG1RWUVNfXkxFGx4UWVMQChVAGxQaUlAQDBpOAR4GGwkaFBNaVGlOGwgSBwQbFBpTXRAMGktTXlNaVAUOBQ4ADggIEBwVWFMaAmoIHgYUCW8cFVdVV18TAxAHDgwEAAIFCgwNBggCSAlPXmVRDGp0UUlVf3J%2BTFZ1R2RvQnlJdFULBRdqAH0aY1VcU2t6RldgXkR1VlAMdmZrQVhifQp2c1wNAHNjUWt7cEELYVxgCWJRXV9xX2pJfmJtU31CX3J7YG9CaVpxf3R%2BfXNwekFPdX5wCHtkaxN1S1V0ewt0BGpdTXx0aWBUfmV%2BDHdYA1Jte2JcdGNvVnFjYXZ6anFyUH57VHdRQVdyXFIOdnAEDxgLXQUDVAEOAEZLFQNIRkdwTmNNb3BpRk5hcEBOUGZPZHdpbl5tZwYJbGZ1dVBhQFtob3dwfG5VRHRwUVNrZlFje35oe2hjZ2B5bQNjcXNPAHVyUGRuf0BSb3R3V2FwYQN9e1BuYX9FXn9oYwhVd3sIfWNRXW5vbFFoYE1oeXpweHhwelZkcXFNfXxTd25xXld9dQFuYGp5BQxHAl0AQARBABcVGlVCXhAMGhtP~1njepum%5C%22%2C%5C%22sceneid%5C%22%3A%5C%22couponNinePointNineHome%5C%22%7D%22%7D&client=m&monitorSource=&appid=XPMSGC2019&eu=8363636353430333238383930383&fv=83D2563646039366262656735613'
    headers = {
        'Host': 'api.m.jd.com',
        'content-length': '2355',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'jdapp;android;11.0.2;;;appBuild/97565;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1656050080462%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22EG%3D%3D%22%2C%22ad%22%3A%22DNumDzumYJGmDJYnDzU4EG%3D%3D%22%2C%22od%22%3A%22CWY0CJu4DNDrDWO1CwYyCq%3D%3D%22%2C%22ov%22%3A%22Ctq%3D%22%2C%22ud%22%3A%22ENY2DtU0CNCyENq5CNq4BWVtZNK5ZwTsZJdvCG%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1-wesley_iui-19.12.12; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046011 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://h5.m.jd.com',
        'x-requested-with': 'com.jingdong.app.mall',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://h5.m.jd.com/',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'pt_key=AAJiqUq4ADAUxIS06uEeQ227Id1FUU5KNQY99Xrvszd6Rycma5cG0Tnh6bgqCxHTxc7wGWezldQ;pt_pin=%E7%8E%8B%E7%BF%94%E8%85%BE'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(str(time.time()))
    print(response.text)


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor

    executor = ThreadPoolExecutor(max_workers=10)
    main()
