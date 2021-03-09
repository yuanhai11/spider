# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '3115688577@qq.com'
password = 'jlkjcogtbxymdeab'
# 收信方邮箱
to_addr = '2094534819@qq.com'
# 发信服务器
smtp_server = 'smtp.qq.com'

message = MIMEMultipart()
message['From'] = from_addr
message['To'] = to_addr
message['Subject'] = Header('this is come from xiangteng simida', 'utf-8')
o = open('{}'.format(r'C:\Users\20945\Desktop\GIF\3_133a1ce090c3722fe7e34f98e5eaaab3_0.gif'), 'rb').read()
att2 = MIMEText(o, 'base64', 'utf-8')
att2["Content-Type"] = 'application/octet-stream'
att2["Content-Disposition"] = 'attachment; filename="123.jpg"'
message.attach(att2)

# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP()
server.connect(smtp_server, 587)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, message.as_string())
# 关闭服务器
server.quit()