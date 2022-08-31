# yh 33380
import datetime
import time
import asyncio
from functools import wraps

from aiohttp import ClientSession  # pip3 install aiohttp -t .
import sys
import requests
import json
import random
from asyncio.proactor_events import _ProactorBasePipeTransport

def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


sign_api = 'http://106.52.174.151:9000/jd/sign'  # sign接口地址

url_count = 15  # 每个账号生成几条链接
each_url_resend = 1  # 每个链接复用几次
push_plus_token = 'a9a912c174074dba97b6e51073c04980'  # 推送token http://www.pushplus.plus
cks = [
    {
        'name': "祥腾",  # 账号2名
        'ck': "pin=%E7%8E%8B%E7%BF%94%E8%85%BE;wskey=AAJjDujkAEDD_xU4HrZ-57Yy7NmsQBrc8nr7BDfGX8oJiEgWPiSZMDxKBdnbul8AXTj8j-8x9qYAG12l4K4ECoB6NX3qLenK;",
        'request': [],
        'is_active': 1  # 是否激活,0关闭
    }
    # { 多账号依次复制配置
    #     'name': "",  # 账号2名
    #     'ck': "",  # wskey
    #     'request': [],
    #     'is_active': 1  # 是否激活,0关闭
    # },

]

IS_TEST = 0
sleep = 5
deadline_minute = 59
deadline_second = 59
deadline_microsecond_avg = 999999  # 根据cpu network 调整此参数
test_data = {}
host = "https://"
already_push = set()
key = 'convertUrlNew'

account_num = sum([1 for i in cks if i['is_active']])

req_timeout = 6

push_url = "https://www.pushplus.plus/send?token={}&title={}&content={}"

app_version = "11.0.0"
user_agent = f"okhttp/3.12.1;jdmall;android;version/{app_version};build/97235;"
HEADERS = {
    "Host": "api.m.jd.com",
    # "cookie": ck,
    "charset": "UTF-8",
    "user-agent": user_agent,
    "accept-encoding": "br,gzip,deflate",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
}
proxies = {"https": "http://192.168.1.105:8888"}
proxies = None
if not sign_api:
    print('请输入sign接口地址')
    sys.exit(0)


def push_msg(content, title=None, ):
    if not push_plus_token:
        return
    print('推送为：', content)
    r1 = requests.get(push_url.format(push_plus_token, title, content), timeout=10)
    print('server结果2', r1.text)


def randomString(e, flag=False):
    t = "0123456789abcdef"
    if flag: t = t.upper()
    n = [random.choice(t) for _ in range(e)]
    return ''.join(n)


class mt():
    sess = None
    loop = None
    tasks = None
    can_push = True

    def __init__(self, ):

        self.tasks = []

    async def buy_mt(self, name, index, url, payload, headers):
        is_break = False
        can_push = True
        if name in already_push:
            return

        try:
            print('{}-{}开始请求-{}'.format(name, index, datetime.datetime.now()))
            async with self.sess.post(url, data=payload, headers=headers, timeout=req_timeout) as r:
                # r = await self.sess.post(self.url, data=self.data, headers=self.header, timeout=30)
                now = datetime.datetime.now()

                res = await r.json(content_type=None)
                print('{}-{}得到响应-{}-{}'.format(name, index, now, res))
                # print(res)
                result = res.get('result')
                # subCodeMsg = res.get('subCodeMsg')
                subCode = res.get('subCode')
                if result and result['desc'] == '领券成功':
                    print('领券成功')
                    is_break = True


                elif subCode and subCode == 'A1':
                    print('领券成功')
                    is_break = True

                if is_break:
                    already_push.add(name)


        except asyncio.CancelledError:
            print('任务{}-{}取消了'.format(name, index))
        except asyncio.TimeoutError:
            print('任务{}-{}超时了'.format(name, index))
        except Exception as e:
            print('任务{}-{}异常--{}'.format(name, index, e.args))

    def create_task(self):

        start = 0
        end = url_count * each_url_resend

        while start < end:
            task_t = []
            for account in cks:
                if not account['is_active']:
                    continue
                name = account['name']
                headers = account['headers']
                req = account['request'].pop()
                url = req['url']
                body = req['body']
                # print(f'name:{name},url is {url}')
                task = asyncio.ensure_future(self.buy_mt(name, start + 1, url, body, headers))
                task_t.append(task)

            start += 1
            group = asyncio.gather(*task_t, )
            self.tasks.append(group)
        print('任务创建完成-{}'.format(datetime.datetime.now()))
        sleep_time, target = get_sleep()
        if sleep_time > 0:
            print('sleep {} s'.format(sleep_time))
            print(f'预计{target} 开始请求')
            time.sleep(sleep_time)

        return

    def push(self, name, can_push):
        if not can_push:
            return

        print('进入推送')
        content = '{}-jd-ddq-抢券成功'.format(name)
        push_msg(content, title='ddq-抢券成功')
        already_push.add(name)

    async def run(self, ):
        print(' run now at {}'.format(datetime.datetime.now()))
        self.sess = ClientSession()
        self.create_task()
        print('共计{}组任务,每组{}个'.format(len(self.tasks, ), account_num))
        t1 = time.time()
        await asyncio.gather(*self.tasks, )
        t2 = time.time()
        print(f'耗时{t2 - t1}s')
        for name in already_push:
            self.push(name, True)

        await self.sess.close()


def get_sign_api(functionId, body):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }
    data = {
        'functionId': functionId,
        'body': json.dumps(body),
        'clientVersion': app_version
    }

    try:
        if proxies:
            r = requests.post(url=sign_api, headers=headers, data=data, timeout=30, proxies=proxies, verify=False)
        else:
            r = requests.post(url=sign_api, headers=headers, data=data, timeout=30, )
        # print('请求sign结果:{}'.format(r.text))
        res = r.json()

        if res['code'] == 200:
            return res['data']
        else:
            print(res)
            return -1
    except:
        return -1


def getCcFeedInfo(cookie):
    body = {
        "categoryId": 118,
        "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
        "eid": randomString(16),
        "globalLat": "",
        "globalLng": "",
        "lat": "",
        "lng": "",
        "monitorRefer": "appClient",
        "monitorSource": "ccfeed_android_index_feed",
        "pageClickKey": "Coupons_GetCenter",
        "pageNum": 1,
        "pageSize": 20,
        "shshshfpb": ""
    }
    res = get_sign_api('getCcFeedInfo', body)  # st sv sign

    if res == -1:
        return -1
    else:
        #print('优惠券res', res)
        params = res[key]
        functionId = res['functionId']
        body = res['body']
        # params = params.replace(body, '')
        url = f'https://api.m.jd.com?functionId={functionId}&' + params
        # print('url:{}'.format(url))
        headers = {
            "Host": "api.m.jd.com",
            "cookie": cookie,
            "charset": "UTF-8",
            "user-agent": user_agent,
            "accept-encoding": "br,gzip,deflate",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "content-length": str(len(body)),
        }
        if proxies:
            res = requests.post(url=url, headers=headers, data=body, timeout=30, proxies=proxies, verify=False).json()
        else:
            res = requests.post(url=url, headers=headers, data=body, timeout=30, ).json()
        # print('获取优惠券结果：{}'.format(res))
        if res['code'] == '0':
            return res['result']['couponList'][0]['receiveKey']
            for coupon in res['result']['couponList']:
                title = coupon.get('title', '')
                if title is not None and '全品类' in title:
                    receiveKey = coupon['receiveKey']
                    return receiveKey
            print('没有找到59-20券的receiveKey')
            return -1
        else:
            print('获取59-20券的receiveKey失败')
            return -1


def get_receiveNecklaceCoupon_sign(receiveKey):
    body = {"channel": "领券中心",
            "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
            "couponSource": "manual",
            "couponSourceDetail": None,
            "eid": randomString(16),
            "extend": receiveKey,
            "lat": "",
            "lng": "",
            "pageClickKey": "Coupons_GetCenter",
            "rcType": "4",
            "riskFlag": 1,
            "shshshfpb": "",
            "source": "couponCenter_app",
            "subChannel": "feeds流"
            }
    # res = get_sign_api('newReceiveRvcCoupon', body) # 领券
    res = get_sign_api('receiveNecklaceCoupon', body)  # 59-20
    if res == -1:
        return -1
    else:
        params = res[key]
        functionId = res['functionId']
        body = res['body']
        # params = params.replace(body, '')
        url = f'https://api.m.jd.com?functionId={functionId}&' + params
        return [url, body]


def run():
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    a = mt()
    # print('mt id is {}'.format(id(a)))
    if IS_TEST:
        a.same_count = 1

    # try:
    #     ret = loop.run_until_complete(a.run(file_name))
    # except CancelledError:
    #     print('loop CancelledError')
    ret = loop.run_until_complete(a.run())
    if not loop.is_closed():
        loop.close()
    return ret


def get_sleep():
    now = datetime.datetime.now()
    if now.second > 50:
        deadline = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                                     second=deadline_second, microsecond=deadline_microsecond_avg)
        t = (deadline - now).total_seconds()
        return t,deadline

    url = 'https://api.m.jd.com?functionId=receiveNecklaceCoupon&ef=1&ep={"cipher": {"uuid": "EQC0CtYzYzSnENG0CwGnCG=="}, "ciphertype": 5}&body=%7B%22channel%22%3A+%22%5Cu9886%5Cu5238%5Cu4e2d%5Cu5fc3%22%2C+%22childActivityUrl%22%3A+%22openapp.jdmobile%3A%2F%2Fvirtual%3Fparams%3D%7B%5C%22category%5C%22%3A%5C%22jump%5C%22%2C%5C%22des%5C%22%3A%5C%22couponCenter%5C%22%7D%22%2C+%22couponSource%22%3A+%22manual%22%2C+%22couponSourceDetail%22%3A+null%2C+%22eid%22%3A+%22eidA909b81250dseyIEuztctSPuxVfyYc4CRosiBMEaq1mGy3k7cIFYhQtefV8SvcpTogGpyPUzynUt7Mxz4pLJtZiZ9rbikPuoVJH8mLZqJ61ypFXEx%22%2C+%22extend%22%3A+%2288DB80104521161CDFFBD5A8057E28D3865BFEB82B64AED9393ED875CFE88972A213BE06482C2B115ACD30536499B3CB0A01A2E3517769E5B0D9D7A5FEB8B8892408733446962758A6118E20FC69EEA2151C8384F6BBD8C70A8F1DEB3B5A37F1AE24E8A37D24B5E6E3B11DA7D17F9D328E08E2BCBD94F7954B2C3EF96C2246A05C4560B336B0522C122D4360FCDE797D8BC95AFBC44FDECC7F1C00439B22B6F6A643C4F7DC216940F7E871BB198512931C27308F4A99B8DA51BDF775AE235F0DCA85EA05864814196BAD9E2D1232632D22A9665FEA46F9243441328694328E4F49D81EAED0EE9ECAD2A577D619E50339F284A7229BE639B5D43697A7253929B041AD7441B3589E561652F214FF5B52C4AB63DF5A94DBBF45E8E7D8EEAE1EB9D977EA8516460DEA6B372EB50B2BC2DE87%22%2C+%22lat%22%3A+%22%22%2C+%22lng%22%3A+%22%22%2C+%22pageClickKey%22%3A+%22Coupons_GetCenter%22%2C+%22rcType%22%3A+%224%22%2C+%22riskFlag%22%3A+1%2C+%22shshshfpb%22%3A+%22%22%2C+%22source%22%3A+%22couponCenter_app%22%2C+%22subChannel%22%3A+%22feeds%5Cu6d41%22%7D&client=android&clientVersion=11.0.0&st=1654669811088&sv=122&sign=875891242c661b121cc5b3e896b82a83'
    app_version = "11.0.0"
    user_agent = f"okhttp/3.12.1;jdmall;android;version/{app_version};build/97235;"
    ck = "pin=jd_6686cd408b255;wskey=AAJiVSSEAEAFVj8nnjJmbhgvnbAHgykuCVgAhc-FuzQBJmJB9iRmvI5EyOKs2lEY1ckj2j7i3xTS2QgfNnwWYorzzwhDqZ5b"
    HEADERS = {
        "Host": "api.m.jd.com",
        "cookie": ck,
        "charset": "UTF-8",
        "user-agent": user_agent,
        "accept-encoding": "br,gzip,deflate",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "content-length": str(len(body)),
    }
    data = {"channel": "\u9886\u5238\u4e2d\u5fc3",
            "childActivityUrl": "openapp.jdmobile://virtual?params={\"category\":\"jump\",\"des\":\"couponCenter\"}",
            "couponSource": "manual", "couponSourceDetail": None,
            "eid": "eidA809b81250dseyIEuztctSPuxVfyYc4CRosiBMEaq1mGy3k7cIFYhQtefV8SvcpTogGpyPUzynUt7Mxz4pLJtZiZ9rbikPuoVJH8mLZqJ61ypFXFx",
            "extend": "88DB80105521161CDFFBD5A8057E28D3865BFEB82B64AED9393ED875CFE88972A213BE06482C2B115ACD30536499B3CB0A01A2E3517769E5B0D9D7A5FEB8B8892408733446962758A6118E20FC69EEA2151C8384F6BBD8C70A8F1DEB3B5A37F1AE24E8A37D24B5E6E3B11DA7D17F9D328E08E2BCBD94F7954B2C3EF96C2246A05C4560B336B0522C122D4360FCDE797D8BC95AFBC44FDECC7F1C00439B22B6F6FF95CE347D7CE4193EAE56BF4C276D7B1C27308F4A99B8DA51BDF775AE235F0DCA85EA05864814196BAD9E2D1232632DD458E4C2C7B203826593FFADD346BDA50E7215C2BFA5162B580FA4892B27200936F0FD82AF863BB51C99DBA8FCED0D9D96F0912F4DB3394D3200BEA86F5C36FD752E266DDDDEA8D8D7DAF8E42313947BCE23940D82379D3C92DF5C31A01329DA",
            "lat": "", "lng": "", "pageClickKey": "Coupons_GetCenter", "rcType": "4", "riskFlag": 1, "shshshfpb": "",
            "source": "couponCenter_app", "subChannel": "feeds\u6d41"}
    count = 3
    t = []
    print('正在测试网络延迟,提示什么不重要...')
    for i in range(count):
        t1 = time.time()
        r = requests.post(url, data=data, headers=HEADERS)
        # r = requests.post(url, headers=HEADERS)
        print(r.text)
        t2 = time.time()
        diff = t2 - t1
        print(f'耗时{diff}s')
        t.append(diff)
    avg = sum(t) / count
    print('平均耗时{}s'.format(avg))
    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute,
                                 second=deadline_second, microsecond=deadline_microsecond_avg)
    t3 = (deadline - now).total_seconds() - avg
    target = now + datetime.timedelta(seconds=t3)
    return t3,target


def main():
    if account_num == 0:
        return
    for account in cks:
        if not account['is_active']:
            continue
        print('正在获取{} 59-20券key-{}'.format(account['name'], datetime.datetime.now()))
        s = 0
        print(f'账号({account["name"]})准备生成共计{url_count * each_url_resend}条抢券链接')

        headers = HEADERS.copy()
        headers['cookie'] = account['ck']

        account['headers'] = headers
        for i in range(url_count):
            receiveKey = getCcFeedInfo(account['ck'])
            if receiveKey == -1:
                return
            res = get_receiveNecklaceCoupon_sign(receiveKey)
            if res == -1:
                print('没有获取到优惠券')

                return
            url = res[0]
            body = res[1]
            for j in range(each_url_resend):
                account['request'].append({'url': url, 'body': body})
    now = datetime.datetime.now()
    print('生成完毕，等待抢券{}'.format(now))
    print('程序开始-{}'.format(datetime.datetime.now()))
    run()
    print('结束-{}'.format(datetime.datetime.now()))


# def main_handler(event, context):
#     main()
#
#
# def handler(event, context):
#     main()


if __name__ == '__main__':
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, 'cron', day ='1-31', hour="14", minute='04')
    # scheduler.start()
    main()
