#coding:utf-8
import requests
import time
import random
import base64
import random
import cv2

'''
1、电脑下载python，安装。第一页有个Add python 3.9 to PATH的，记得勾选上
2、打开cmd，输入以下命令，安装第三方库
pip install opencv-python
pip install requests==2.20
到此，python部分已经安装好了。
4、抓包。打开抓包软件Fiddler.exe
5、登录电脑版微信，打开知苗易约小程序，登录
6、小程序随便点进一个卫生服务中心
7、在Fildder右边找到Cookie下的ASP.NET_SessionId=ubqnf0phg51uxbvjfenercml，复制这段内容
8、粘贴在脚本文件里的Cookie里面
9、打开脚本,修改里面的身份证号码，手机号码
10、按F5运行'''


def GetCustSubscribeDateDetail():
    print('访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
    time.sleep(int_time)
    payload = {
        'act': 'GetCustSubscribeDateDetail',
        'pid': p_id,
        'id': shequ_id,
        'scdate': yuyue_times,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)

    # 转json
    if int(code.status_code) == 200:
        code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) == 200:
            print(code_json_dict['list'][0]['mxid'])
            mxid = code_json_dict['list'][0]['mxid']
            check_mxid = False
            return check_mxid, mxid
        else:
            check_mxid = True
            mxid = ''
            return check_mxid, mxid
    else:
        print(code.status_code)
        check_mxid = True
        print('访问异常,继续访问')
        mxid = ''
        return check_mxid, mxid


def base64ToImageTarget(str_base64):
    num = random.randint(1, 99)
    name = 'target.jpg'
    img_data = base64.b64decode(str_base64)
    file = open(name, 'wb')
    file.write(img_data)
    file.close()


def base64ToImageBackground(str_base64):
    num = random.randint(1, 99)
    name = 'background.jpg'
    img_data = base64.b64decode(str_base64)
    file = open(name, 'wb')
    file.write(img_data)
    file.close()


def _tran_canny(image):
    """消除噪声"""
    image = cv2.GaussianBlur(image, (3, 3), 0)
    return cv2.Canny(image, 50, 150)


# 图片验证码xy轴


def detect_displacement(img_slider_path, image_background_path):
    """detect displacement"""
    # # 参数0是灰度模式
    image = cv2.imread(img_slider_path, 0)
    template = cv2.imread(image_background_path, 0)

    # 寻找最佳匹配
    res = cv2.matchTemplate(_tran_canny(
        image), _tran_canny(template), cv2.TM_CCOEFF_NORMED)
    # 最小值，最大值，并得到最小值, 最大值的索引
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc[0]  # 横坐标
    # 展示圈出来的区域
    x, y = max_loc  # 获取x,y位置坐标

    w, h = image.shape[::-1]  # 宽高
    cv2.rectangle(template, (x, y), (x + w, y + h), (7, 249, 151), 2)
    # show(template)
    return top_left


# 显示图片

# 显示图片
def show(name):
    '''展示圈出来的位置'''
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getCanSubscribeDateAll():
    print('(0)开始获取能预约的日期信息：GetCustSubscribeDateAll')
    time.sleep(int_time)
    payload = {
        'act': 'GetCustSubscribeDateAll',
        'pid': p_id,
        # 'pid': 66,
        'id': shequ_id,
        'month': month,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    if int(code.status_code) == 200:
        code_json_date = code.json()
        print(code.json())
        if int(code_json_date['status'] == 200):

            dateList = code_json_date['list']
            dateArr = []
            ChecksTime = True
            if len(dateList) > 0:
                for index in range(len(code_json_date['list'])):
                    if code_json_date['list'][index]['enable']:
                        dateArr.append(code_json_date['list'][index]['date'])
                        print('能预约的日期是：')
                        print(dateArr)

                        ChecksTime = False
                return ChecksTime, dateArr
            else:
                print('该社区暂时没有能预约的日期')
                return ChecksTime, dateArr


def Code_1():
    # 此处可能出现问题
    print('（1）开始访问获取客户订阅日期详细信息：GetCustSubscribeDateDetail')
    time.sleep(int_time)
    payload = {
        'act': 'GetCustSubscribeDateDetail',
        'pid': p_id,
        'id': shequ_id,
        'scdate': yuyue_times,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    resp = code.reason
    print(resp)
    exit()
    if int(code.status_code) == 200:

        code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) == 200:
            if code_json_dict['list']:
                print(code_json_dict['list'][0]['mxid'])
                mxid = code_json_dict['list'][0]['mxid']
                check_mxid = False
                return check_mxid, mxid
            else:
                print('九价还没开放')
                check_mxid = True
                mxid = ''
                return check_mxid, mxid
        else:
            check_mxid = True
            mxid = ''
            return check_mxid, mxid
    else:
        print(code.status_code)
        check_mxid = True
        print('访问异常,继续访问')
        mxid = ''
        return check_mxid, mxid


def Code_2():
    # 获取验证码
    print('（2）访问验证码：GetCaptcha')
    time.sleep(int_time)
    payload = {
        'act': 'GetCaptcha',
        'mxid': mxid,
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    print(code.json())
    if int(code.status_code) == 200:
        if int(code.json()['status']) == 0:
            dragon = code.json()['dragon']
            tiger = code.json()['tiger']
            base64ToImageBackground(dragon)
            # if(tiger is not None):
            #     base64ToImageTarget(tiger)
            ck_s = YanZheng302()
            return ck_s
        else:
            ck_s = True
            return ck_s
    else:
        print('访问异常,继续访问%s' % code.status_code)
        ck_s = True
        return ck_s


def YanZheng302():
    print("（3）开始验证：CaptchaVerify")
    x = detect_displacement("target.jpg", "background.jpg")
    print(x)
    time.sleep(int_time)
    payload = {
        'act': 'CaptchaVerify',
        'token': '',
        'x': x,
        'y': '5',
    }
    code = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    if int(code.status_code) == 200:
        code_json_dict = code.json()
        print(code_json_dict)
        if int(code_json_dict['status']) != 204 and int(code_json_dict['status']) != 201:
            if int(code_json_dict['status']) != 408:
                print('验证码-验证成功')
                print('guid:%s' % code_json_dict['guid'])
                guid = code_json_dict['guid']
                Checks = False
                # 成功后去访问Save20结果去提交数据=预约成功
                print('（4）马上提交')
                Save20(yuyue_times, p_id, mxid, guid)
                return Checks
            else:
                Checks = True
                print('请重新授权Cookies')
                return Checks
        else:
            Checks = True
            print('继续验证')
            return Checks


def Save20(times, p_id, mxid, guid):
    payload = {
        'act': 'Save20',
        'birthday': "1997-07-05",  # 出生年月日
        'tel': "13137668458",  # 手机号码
        'sex': "2",  # 性别2 女  1 男
        'cname': "无限性",
        'doctype': "1",
        'idcard': "412726199707053757",
        'mxid': mxid,
        'date': times,
        'pid': p_id,
        'Ftime': "1",
        'guid': guid,
    }
    print(payload)
    tongyong = requests.get(
        url="https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx",
        headers=headers, params=payload, verify=False)
    # 转json
    json_dict = tongyong.json()
    print(json_dict)
    if int(json_dict['status']) == 200:
        print(json_dict)
        print('预约成功')
    else:
        print('预约失败，原因是：')
        print(json_dict['msg'])
        pass


if __name__ == '__main__':
    # 延迟时间
    int_time = 0.3

    # Cookies
    '''
    ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDc4NDEzNDEuMTc0NjAxOCwiZXhwIjoxNjQ3ODQ0OTQxLjE3NDYwMTgsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIyMDMyMTAxNDIyMSIsInZhbCI6Ik1VOVRBUUlBQUFBUU1ETTNNREJrWkdGa05tRTBOV0kxTWh4dmNYSTFielZNTTJsaFRtMXFWR2R6ZFVWVWFXVndRV2hSYlcwd0FCeHZcclxuVlRJMldIUTViMmh4Y2prek5HOXZSVEJyU1hOdWJVTkRORGhKRHpFeE5TNHhPVEl1TVRNMExqRTJPQUFRVFZVNVZFRmFObkpCUVVOcFxyXG5hVlJSUWdFQUFBQUEifQ.gwZqsPHmwoK0gffyDJGylEDqpXf_AXyDwe9PXDDbhRk
    '''
    cookies = 'ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDc4NDEzNDEuMTc0NjAxOCwiZXhwIjoxNjQ3ODQ0OTQxLjE3NDYwMTgsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIyMDMyMTAxNDIyMSIsInZhbCI6Ik1VOVRBUUlBQUFBUU1ETTNNREJrWkdGa05tRTBOV0kxTWh4dmNYSTFielZNTTJsaFRtMXFWR2R6ZFVWVWFXVndRV2hSYlcwd0FCeHZcclxuVlRJMldIUTViMmh4Y2prek5HOXZSVEJyU1hOdWJVTkRORGhKRHpFeE5TNHhPVEl1TVRNMExqRTJPQUFRVFZVNVZFRmFObkpCUVVOcFxyXG5hVlJSUWdFQUFBQUEifQ.gwZqsPHmwoK0gffyDJGylEDqpXf_AXyDwe9PXDDbhRk'
    cookies = 'ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDc4NDMxMDguNzc3MzMwNCwiZXhwIjoxNjQ3ODQ2NzA4Ljc3NzMzMDQsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIyMDMyMTAyMTE0OCIsInZhbCI6Ik1VOVRBUUlBQUFBUU56ZzJNakV5WXpJd05ERTJaRFZsTkJ4dmNYSTFielZNTTJsaFRtMXFWR2R6ZFVWVWFXVndRV2hSYlcwd0FCeHZcclxuVlRJMldIUTViMmh4Y2prek5HOXZSVEJyU1hOdWJVTkRORGhKRHpFeE5TNHhPVEl1TVRNMExqRTJPQUFBQUFBQUFBQT0ifQ.k-IYf9uAZxN8tdMCwmkq__lG0IhYGiqk1kKFRK0VWYo'
    cookies = 'ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDc4NDYwNDkuNzgxNjkyNywiZXhwIjoxNjQ3ODQ5NjQ5Ljc4MTY5MjcsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIyMDMyMTAzMDA0OSIsInZhbCI6Ik1VOVRBUUlBQUFBUVlUTTVZekppTm1FNU5UbGtOV1ppWVJ4dmNYSTFielZNTTJsaFRtMXFWR2R6ZFVWVWFXVndRV2hSYlcwd0FCeHZcclxuVlRJMldIUTViMmh4Y2prek5HOXZSVEJyU1hOdWJVTkRORGhKRHpFeE5TNHhPVEl1TVRNMExqRTJPQUFBQUFBQUFBQT0ifQ.OmXwpsNLYsQ1JRNNLTUneK2QQQZ3hL-qHvTckcETjpU'

    headers = {
        'charset': 'utf-8',
        'Accept-Encoding': 'gzip, deflate, br',
        'referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/73/page-frame.html',
        'cookie': cookies,
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Redmi Note 7 Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/7.0.6.1460(0x27000634) Process/appbrand0 NetType/4G Language/zh_CN',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',

        'Host': 'cloud.cn2030.com',
        'Connection': 'Keep-Alive',
        'zftsl': 'b8e425ef383e9eb2616f6861200718cf'
    }
    requests.packages.urllib3.disable_warnings()

    # 猜测验证码的X
    x = '33'
    Checks = True

    ChecksYuyueTime = True
    # 1= 九价
    # 疫苗id
    p_id = '1'

    # 社区id
    shequ_id = '1921'

    # 月份
    month = 202203
    # 填写预约时间
    # yuyue_times = '2021-08-26'
    # 获取能够预约的日期
while ChecksYuyueTime:
    ChecksYuyueTime, yuyue_timesArr = getCanSubscribeDateAll()

    # 获取订阅日期mxid
while Checks:
    for timesarr in yuyue_timesArr:
        yuyue_times = timesarr
        print('开始尝试预约日期为：' + yuyue_times)
        Checks, mxid = Code_1()

# 获取验证码
Checks2 = True
while Checks2:
    Checks2 = Code_2()

    # 7Q90AC5oAABeYzQB = 26670
