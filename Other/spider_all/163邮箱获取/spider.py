# POP3（Post Office Protocol 3），即邮局协议的第3个版本，
# 是电子邮件的第一个离线协议标准。该协议把邮件下载到本地计算机，
# 不与服务器同步，缺点是更易丢失邮件或多次下载相同的邮件。
import poplib
# 引入用来解析邮件相关信息的模块
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
# 引入相关时间库
from datetime import datetime
# 引入专门处理时间和日期的模块，arrow是一个轻量级Python库
import arrow
import logging.handlers

# 2、再定义一些与邮件相关的全局变量
class Email_163:
    def __init__(self):
        # 输入自己163的邮箱地址。
        self.user_email_address = 'w2094534819@163.com'
        # 邮箱的授权码，注意：不是登录密码
        self.user_password = 'NOAAVPKTDBXMRKOF'
        # 这个是163邮箱的pop3的服务器地址，各个公司的邮箱平台的POP3的服务器地址都是不同的，自己网上查询下即可
        # 例如：qq邮箱的pop3服务器地址是：pop.qq.com
        self.pop_server_host = 'pop.163.com'
        # 邮箱对应的pop服务器的监听端口
        # （如果设置POP3的SSL加密方式连接的话，则端口为：995），否则就是端口为110
        self.pop_server_port = 995
        self.logger = None
        self.write_log()

    def start(self):
        self.connect_email_by_pop3()

    def write_log(self):
        # 初始化设置
        logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
        # 创建
        self.logger = logging.getLogger("email")
        self.logger.setLevel(logging.INFO)
        # 创建handler
        handler1 = logging.FileHandler("email.log")
        handler1.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
        handler1.setFormatter(formatter)
        handler2 = logging.StreamHandler()
        handler2.setLevel(logging.ERROR)
        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)

    # 3、定义邮箱连接校验的函数
    def connect_email_by_pop3(self):
        try:
            # 连接pop服务器。如果没有使用SSL，将POP3_SSL()改成POP3(),且监听端口改为：110即可
            email_server = poplib.POP3_SSL(host=self.pop_server_host, port=self.pop_server_port, timeout=10)
            # 验证用户邮箱
            email_server.user(self.user_email_address)
            # 验证邮箱密码是否正确，注意不是登录密码，是授权码
            email_server.pass_(self.user_password)
            self.logger.info("连接pop服务器-------成功")
        except Exception as e:
            # 注意：如果出现连接pop服务器问题，可能是自己的邮箱没有设置开启POP3服务，如qq邮箱的。
            self.logger.error("连接pop服务器-------异常，退出 \n 异常原因：{}".format(e))
            exit(1)

        # 开始处理邮箱相关信息
        self.parse_email_server(email_server)

    # 4、定义处理邮箱相关信息的函数
    def parse_email_server(self,email_server):
        resp, mails, octets = email_server.list()
        num, total_size = email_server.stat()
        self.logger.info("邮件数量为：" + str(num))
        # mails存储了邮件编号列表，
        index = len(mails)
        # 倒序遍历邮件
        for i in range(1, index+1):
            self.logger.info("------第{}封邮件--------".format(i))
            resp, lines, octets = email_server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 邮件的原始文本:# lines是邮件内容，列表形式使用join拼成一个byte变量
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # 解析邮件:
            msg = Parser().parsestr(msg_content)
            # 邮件时间,解析时间格式
            mail_datetime = self.parse_mail_time(msg.get("date"))
            max_mail_time_str = arrow.get(mail_datetime).format("YYYY-MM-DD HH:mm")
            # 这个可以作为根据时间进行邮件的过滤解析，这个把时间写死判断，比较局限，可以在第一个接收时，把最新的邮件接收时间写入到自定义的文件中，
            # 等第二次接收邮件时，再取文件中的时间，进行判断，用于过滤
            # if (max_mail_time_str > "2020-01-01 00:00:00"):
            #     continue
            self.logger.info("邮件接收时间为：" + max_mail_time_str)
            # 解析邮件具体内容，包括正文，标题，和附件
            self.parser_content(msg, 0)
        # 别忘记退出
        email_server.quit()


    # 5、定义解析邮件具体内容


    def parser_content(self,msg, indent):
        if indent == 0:
            # 邮件的From, To, Subject存在于根对象上:
            # 调用解析邮件头部内容的函数
            self.parser_email_header(msg)
        # 下载附件
        for part in msg.walk():
            file_name = part.get_filename()  # 获取附件名称类型
            if file_name is None:
                continue
            # 说明不是文本，则作为附件处理
            filename = self.decode_str(file_name)  # 对附件名称进行解码
            data = part.get_payload(decode=True)  # 下载附件
            att_file = open('E:/emailFiles/' + filename, 'wb')  # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
            att_file.write(data)  # 保存附件
            att_file.close()
            self.logger.info("附件：" + filename + "保存成功！")

        if (msg.is_multipart()):
            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                # 递归打印每一个子对象:
                return self.parser_content(part, indent + 1)
        else:
            # 解析正文
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                    self.logger.info('%s正文内容为: %s' % ('  ' * indent, content))


    # 6、定义解析头部内容的相关函数


    # 解析邮件
    def parser_email_header(self,msg):
        # 解析邮件标题
        subject = msg['Subject']
        value, charset = decode_header(subject)[0]
        if charset:
            value = value.decode(charset)
        self.logger.info('邮件标题： {0}'.format(value))

        # 解析发送人信息
        hdr, addr = parseaddr(msg['From'])
        # name 发送人邮箱名称， addr 发送人邮箱地址
        name, charset = decode_header(hdr)[0]
        if charset:
            name = name.decode(charset)
        self.logger.info('发送人邮箱名称: {0}，发送人邮箱地址: {1}'.format(name, addr))

        # 解析接收人信息
        hdr, addr = parseaddr(msg['To'])
        # name 发送人邮箱名称， addr 发送人邮箱地址
        name, charset = decode_header(hdr)[0]
        if charset:
            name = name.decode(charset)
        self.logger.info('接收人邮箱名称: {0}，接收人邮箱地址: {1}'.format(name, addr))


    # 7、其它相关定义函数
    # 解码
    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 猜测字符编码
    def guess_charset(self,msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            for item in content_type.split(';'):
                item = item.strip()
                if item.startswith('charset'):
                    charset = item.split('=')[1]
                    break
        return charset


    # 邮件时间处理函数
    def parse_mail_time(self,mail_datetime):
        GMT_FORMAT = "%a, %d %b %Y %H:%M:%S"
        GMT_FORMAT2 = "%d %b %Y %H:%M:%S"
        index = mail_datetime.find(' +0')
        if index > 0:
            mail_datetime = mail_datetime[:index]  # 去掉+0800
        formats = [GMT_FORMAT, GMT_FORMAT2]
        for ft in formats:
            try:
                mail_datetime = datetime.strptime(mail_datetime, ft)
                return mail_datetime
            except:
                pass
        raise Exception("邮件时间格式解析错误")


# 比较规范写法，象征着程序入口
if __name__ == "__main__":
    email = Email_163()
    email.start()