import smtplib
from email.mime.text import MIMEText
# 发送多种类型的邮件
from datetime import date
from email.mime.multipart import MIMEMultipart
import datetime

def send_email(data):

    name = data[0]
    email = data[2]

    msg_from = '3115688577@qq.com'  # 发送方邮箱
    passwd = 'ryfrdkwzpstldhcb'

    to = [email]  # 接受方邮箱

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    # conntent="这个是字符串"
    # #把内容加进去
    # msg.attach(MIMEText(conntent,'plain','utf-8'))

    # 添加附件
    # att1 = MIMEText(open('result.xlsx', 'rb').read(), 'base64', 'utf-8')  # 打开附件
    # att1['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    # att1['Content-Disposition'] = 'attachment;filename=result.xlsx'  # 设置描述信息

    att2 = MIMEText(open('/dev/a.jpg', 'rb').read(), 'base64', 'utf-8')
    att2['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    att2['Content-Disposition'] = 'attachment;filename=a.jpg'  # 设置描述信息

    # msg.attach(att1)  # 加入到邮件中
    msg.attach(att2)

    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    mytime = str(year) + " 年 " + str(month) + " 月 " + str(day) + " 日 "
    # 构造HTML
    content = '''
                    <html>
                    <body>
                        <h1 align="center">标题：生日祝福</h1>
                        <p><strong>许久不见：</strong></p>
                        <blockquote><p><strong>愿你三冬暖，愿你春不寒。愿你天黑有灯，下雨有伞。愿你路上有良人伴！</strong></p></blockquote>
    
                        <p align="center">王祥腾</p>
                        <p align="center">{mytime}</p>
                    <body>
                    <html>
                    '''.format(mytime=mytime)

    msg.attach(MIMEText(content, 'html', 'utf-8'))
    # 设置邮件主题
    msg['Subject'] = "Happy Birthday To You"
    # 发送方信息
    msg['From'] = msg_from
    # 开始发送
    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print('发送成功')
def translate_yinli(today):
    import sxtwl
    # 日历中文索引
    ymc = [u"11", u"12", u"01", u"02", u"03", u"04", u"05", u"06", u"07", u"08", u"09", u"10"]
    rmc = [u"01", u"02", u"03", u"04", u"05", u"06", u"07", u"08", u"09", u"10", \
           u"11", u"12", u"13", u"14", u"15", u"16", u"17", u"18", u"19", \
           u"20", u"21", u"22", u"23", u"24", u"25", u"26", u"27", u"28", u"29", u"30"] # 阴历没有31天

    # 日历库实例化
    lunar = sxtwl.Lunar()

    # 2.阳历转阴历
    today_list = today.split('-')  # ['2019', '08', '08']
    lunar_day = lunar.getDayBySolar((int)(today_list[0]), (int)(today_list[1]), (int)(today_list[2]))  # 输入年月日
    return ymc[lunar_day.Lmc], rmc[lunar_day.Ldi]

def translate_yangli(year,mon,day):
    import sxtwl
    # 日历库实例化
    lunar = sxtwl.Lunar()
    # 1.阴历转阳历
    solar_day = lunar.getDayByLunar(int(year),int(mon),int(day))
    return '-'.join([str(solar_day.y),str(solar_day.m),str(solar_day.d)])

def __init__():
    birthday = [


        ['陈小敏','2021-09-06','2674089615@qq.com'],
        ['王祥腾','2021-07-19','2094534819@qq.com'],
        # ['王祥腾','2021-10-17','2094534819@qq.com'],
        ['彩自震','2021-08-27','1994196489@qq.com'],
        # ['李昭洁','2021-08-27','1994196489@qq.com'],
        # ['王文龙','2021-08-27','2273525193@qq.com'],
        ['王冲','2021-09-06','1058397280@qq.com'],
        ['邓鸿杰','2021-11-01','2276473611@qq.com'],
        ['吉航帆','2021-03-25','987627639@qq.com'],
        ['祁川','2021-04-17','1363198538@qq.com'],
        ['王亚慧','2021-11-11','2824825919@qq.com'],

                ]

    for data in birthday:
        dateee = data[1]
        value = dateee.split('-')
        year = value[0]
        func = lambda x:x[1]if x.startswith('0') else x
        mon = func(value[1])
        day = func(value[2])

        translated = translate_yangli(year,mon,day)

        translated0 = translated.split('-')[0]
        translated1 = translated.split('-')[1]
        translated2 = translated.split('-')[2]
        if len(translated1) == 1:
            translated1 = '0'+translated1
        if len(translated2) == 1:
            translated2 = '0' + translated2
        translated = '-'.join([translated0,translated1,translated2])

        today = str(date.today())
        if translated == today:
            print('已发')
            send_email(data)
        else:
            print('不符合要求')



if __name__ == '__main__':
    __init__()
