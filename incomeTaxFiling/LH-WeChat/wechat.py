#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
个税 work 调度脚本
用于接收路由信息
收到消息后请求中后台
获取账号密码及人员信息json
"""
import base64
import json
import logging.config
import os
import random
import shutil
import time
import traceback
from ctypes import windll
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import requests
from sys import argv
import pymysql
# 加入pywintypes，打包成功
import pywintypes
import pythoncom
import win32com.client
import win32api
import win32com
import win32con
import win32gui
from Crypto.Cipher import AES
# 导入config里的变量信息
from decouple import config
# from openpyxl import load_workbook
from xlrd import open_workbook
from logger_manager import LoggerManager

MAP_KEYS = windll.user32.MapVirtualKeyA
LoggerManager.init_logging("logs/work_manager.log", need_mail=False, need_console=True)
logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)

HOST = config('DB_TEST_HOST')
USER = config('DB_TEST_USER')
PASSWORD = config('DB_TEST_PASSWORD')
DATABASE = config('DB_TEST_DBNAME')

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
}
# 获取用户目录
USER_PATH = os.environ.get("USERPROFILE")

LOCAL_FILE_PATH = os.path.join(USER_PATH, 'Desktop', '0申报流程')

# 对接外部的个税RPA用不到了
def aes_decode(password):
    key = 'zlcw_tax_secrets'
    decrypted_text = None
    try:
        aes = AES.new(str.encode(key), AES.MODE_ECB)  # 初始化加密器
        decrypted_text = aes.decrypt(base64.decodebytes(bytes(password, encoding='utf8'))).decode("utf8")  # 解密
        decrypted_text = decrypted_text[:-ord(decrypted_text[-1])]  # 去除多余补位
    except Exception as e:
        logger.error('密码解密出现问题，错误如下 ====>>', e)
    finally:
        return decrypted_text


def save_table(content,task_id,task_type,bot_id):

    data = {
            "task_id":task_id,
            "task_type":task_type,
            "bot_id":bot_id,
            "content":content,
            }

    cur_task_dir = os.path.join(USER_PATH, "Desktop", "rpa_wechat_data")
    if not os.path.exists(cur_task_dir):
        os.mkdir(cur_task_dir)

    cur_company_id_file = os.path.join(cur_task_dir, "task_id.txt")
    with open(cur_company_id_file, 'w')as fp:
        fp.write(json.dumps(data,ensure_ascii=False))


def call_uibot():
    """
    唤起uibot 并执行
    :return:
    """
    # 模拟鼠标点击事件，
    windll.user32.SetCursorPos(200, 500)
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.5)
    windows_type = "Chrome_WidgetWin_1"
    windows_name = "UiBot Creator"
    h_wnd = win32gui.FindWindow(windows_type, windows_name)
    win32gui.ShowWindow(h_wnd, win32con.SW_RESTORE)
    time.sleep(.5)
    win32gui.SetActiveWindow(h_wnd)
    time.sleep(.5)
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(h_wnd)
    time.sleep(.5)
    try:
        win32api.keybd_event(win32con.VK_F5, MAP_KEYS(116, 0), 0, 0)  # 按下 F5
        win32api.keybd_event(win32con.VK_F5, MAP_KEYS(116, 0), win32con.WM_KEYUP, 0)
        logger.info("切换 uibot ui 并 发送 F5 命令 成功！！")
    except Exception as e:
        logger.error('唤起 UiBot ui 程序失败，====>>', e)



# 获取本机IP地址
def get_host_ip():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk.connect(('114.114.114.114', 80))
    ip_addr = sk.getsockname()[0]
    return ip_addr


class SimpleHandler(BaseHTTPRequestHandler):
    LOCAL_IP = get_host_ip()

    def connect(self):
        self.conn = pymysql.connect(host='%s' % HOST, user='%s' % USER, password='%s' % PASSWORD, database='%s' % DATABASE,
                               port=3306)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        try:
            self.connect()
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself

            # 显示的收到消息
            response = post_data.decode('utf-8')
            request1 = json.loads(response)
            logger.info(response)

            task_id = request1['task_id']
            task_type = request1['task_type']
            bot_id = request1['bot_id']
            content = request1['content']

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql3 = "update wechat_work_bot set status=2 where bot_ip='{}'".format\
                (SimpleHandler.LOCAL_IP)
            self.cursor.execute(sql3)
            self.conn.commit()
            logger.info('信息获取成功')
            sql4 = "update wechat_work_task set status=2,gmt_updated='{}',bot_ip='{}' where task_id='{}'".format\
                (times,SimpleHandler.LOCAL_IP,task_id)
            self.cursor.execute(sql4)
            self.conn.commit()

            save_table(content,task_id,task_type,bot_id)  # 本地存表
            time.sleep(2)
            call_uibot()

        except Exception as e:
            logger.error(e)
            sql5 = "update wechat_work_bot set status = 1 where bot_ip='{}'".format(
                SimpleHandler.LOCAL_IP)
            self.cursor.execute(sql5)
            self.conn.commit()

            headers2 = {
                'Content-Type': 'application/json;charset=UTF-8',
                'Host': '47.99.96.186:38059'
            }
            if not task_id:
                task_id = 0

            data = {
                "taskId": int(task_id),
                "status": 70018,
                "msg": '{}'.format(e)
            }
            data = json.dumps(data)
            aaa = requests.post(url='http://47.99.96.186:38059/api/wechat/callback', data=data, headers=headers2).text

        finally:
            self.close()
            self.do_HEAD()


    def msg_look(self, paths, path, status):
        if status:
            self.send_response(paths[path]['status'])
        else:
            self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
                     <html><head><title>Title goes here.</title></head>
                     <body><p>This is a test.</p>
                     <p>You accessed path: {}</p>
                     </body></html>
                     '''.format(path)
        response = bytes(content, 'UTF-8')
        self.wfile.write(response)


def run(server_class=HTTPServer, handler_class=SimpleHandler, addr=get_host_ip(), port=4444):
    logger.info("企业微信的 worker 模块启动中，功能：")
    server_address = (addr, port)
    logger.info('当前pc地址为:{},监听：{}端口>>>'.format(addr, port))
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':


    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
