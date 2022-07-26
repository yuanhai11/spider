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
import shutil
import time
from ctypes import windll

import requests
# 加入pywintypes，打包成功
import pywintypes
import pythoncom
import win32com.client
import win32api
import win32con
import win32gui
from Crypto.Cipher import AES
# 导入config里的变量信息
from decouple import config
from kafka import KafkaConsumer
# from openpyxl import load_workbook
from xlrd import open_workbook

from logger_manager import LoggerManager

# kafka server conf
SERVER = config("SERVER").split(",")
TOPIC = config("TOPIC")

MASTER_URL = config('MASTER_URL')
SPECIAL_URL = config('SPECIAL_URL')
HEADERS_HOST_2 = config('HEADERS_HOST_2')
PURL = config('PURL')

MAP_KEYS = windll.user32.MapVirtualKeyA

LoggerManager.init_logging("logs/work_manager.log", need_mail=False, need_console=True)
logger = logging.getLogger('loggerManager')
logger.setLevel(logging.DEBUG)

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
}
# 获取用户目录
USER_PATH = os.environ.get("USERPROFILE")

LOCAL_FILE_PATH = os.path.join(USER_PATH, 'Desktop', '0申报流程')


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


def save_salary(data, mkpath):
    """
    保存薪水
    :param data:
    :param mkpath:
    :return:
    """
    from xlutils.copy import copy
    oldp = os.path.join(USER_PATH, "Desktop", '正常工资薪金所得.xls')
    file_home = os.path.join(mkpath, '正常工资薪金所得.xls')
    shutil.copyfile(oldp, file_home)
    time.sleep(1)
    wb = open_workbook(filename=file_home)  # 打开excel文件
    excel = copy(wb=wb)
    sheet_table = excel.get_sheet(0)  # 根据Sheet1这个sheet名字来获取该sheet
    personnel_information = data['staffSalaryVOS']
    for u in personnel_information:
        name = str(u['name'])
        sheet_table.write(1, 1, name)
        certificateType = str(u['certificateType'])
        sheet_table.write(1, 2, certificateType)
        certificateNumber = str(u['certificateNumber'])
        sheet_table.write(1, 3, certificateNumber)
        currentIncome = str(u['currentIncome'])
        sheet_table.write(1, 4, currentIncome)
        insurance = str(u['insurance'])
        sheet_table.write(1, 6, insurance)
        medicalInsurance = str(u['medicalInsurance'])
        sheet_table.write(1, 7, medicalInsurance)
        unemploymentInsurance = str(u['unemploymentInsurance'])
        sheet_table.write(1, 8, unemploymentInsurance)
        accumulationFund = str(u['accumulationFund'])
        sheet_table.write(1, 9, accumulationFund)

    excel.save(file_home)  # 保存修改后的excel


def save_person_msg(mkpath, data):
    """
    保存人员信息（仅修改‘人员信息.xlsx’模板）    只能使用xlsx
    :param mkpath:
    :param data:
    :return:
    """
    from xlutils.copy import copy
    oldp = os.path.join(USER_PATH, "Desktop", '人员信息.xls')
    file_home = os.path.join(mkpath, '人员信息.xls')
    shutil.copyfile(oldp, file_home)
    time.sleep(1)
    wb = open_workbook(filename=file_home)  # 打开excel文件
    excel = copy(wb=wb)
    sheet_table = excel.get_sheet(0)  # 根据Sheet1这个sheet名字来获取该sheet
    personnel_information = data['taxStaffRpaVOS']

    for u in personnel_information:
        name = str(u['name'])
        sheet_table.write(1, 1, name)
        certificateType = str(u['certificateType'])
        sheet_table.write(1, 2, certificateType)
        certificateNumber = str(u['certificateNumber'])
        sheet_table.write(1, 3, certificateNumber)
        nationality = str(u['nationality'])
        sheet_table.write(1, 4, nationality)
        gender = str(u['gender'])
        sheet_table.write(1, 5, gender)
        birthday = str(u['birthday'])
        sheet_table.write(1, 6, birthday)
        status = str(u['status'])
        sheet_table.write(1, 7, status)
        jobType = str(u['employedType'])
        sheet_table.write(1, 8, jobType)
        quitDate = str(u['quitDate'])
        if quitDate == 'None':
            quitDate = ''
        sheet_table.write(1, 9, quitDate)
        mob = str(u['mob'])
        sheet_table.write(1, 10, mob)
        jobDate = str(u['employedDate'])
        sheet_table.write(1, 11, jobDate)

        entryDate = str(u['entryDate'])
        if entryDate == 'None':
            entryDate = ''
        sheet_table.write(1, 26, entryDate)
        departureDate = str(u['departureDate'])
        if departureDate == 'None':
            departureDate = ''
        sheet_table.write(1, 25, departureDate)
        birthCountry = str(u['birthCountry'])
        if birthCountry == 'None':
            birthCountry = ''
        sheet_table.write(1, 24, birthCountry)
        otherCertificateNumber = str(u['otherCertificateNumber'])
        if otherCertificateNumber == 'None':
            otherCertificateNumber = ''
        sheet_table.write(1, 28, otherCertificateNumber)
        remark = str(u['remark'])
        if remark == 'None':
            remark = ''
        sheet_table.write(1, 21, remark)
        taxRelatedMatters = str(u['taxRelatedMatters'])
        if taxRelatedMatters == 'None':
            taxRelatedMatters = ''
        sheet_table.write(1, 23, taxRelatedMatters)

    excel.save(file_home)  # 保存修改后的excel


def save_table(response, declare_id):
    res = json.loads(response)
    code = res['code']
    data = res['data']
    tax_number = data['username']  # 账号
    password = data['taxDeclarePwd']  # 密码

    cur_task_dir = os.path.join(USER_PATH, "Desktop", "rpa_data")
    if not os.path.exists(cur_task_dir):
        os.mkdir(cur_task_dir)

    cur_company_id_file = os.path.join(cur_task_dir, "idcode.txt")
    with open(cur_company_id_file, 'w')as fp:
        fp.write(declare_id)
    password = aes_decode(password)
    otherStyleTime = time.strftime("%Y%m%d", time.localtime(time.time()))
    # 定义要创建的目录  当前路径+依赖文件夹+公司id+当前日期
    cur_task_file_dir = os.path.join(USER_PATH, "Desktop", "rpa_data", "{}".format(tax_number),
                                     "{}".format(otherStyleTime))
    # 存c盘下txt路径
    if os.path.exists(cur_task_file_dir):
        logger.info("路径：{}已经存在，该task:{}已经执行过!!".format(cur_task_file_dir, declare_id))
    else:
        os.makedirs(cur_task_file_dir)
    # 保存当前任务 文件路径到 task_file.txt
    with open(os.path.join(cur_task_dir, 'task_file.txt'), "w") as f:
        f.write(cur_task_file_dir)

    save_account_pwd(tax_number, password, cur_task_file_dir)  # 账号密码xls
    save_person_msg(cur_task_file_dir, data)  # 人员信息xlsx
    save_salary(data, cur_task_file_dir)  # 正常工资薪金所得
    return str(code)


def save_account_pwd(tax_number, password, mkpath):
    """
    保存账号密码表（创建并覆盖）
    :param tax_number:
    :param password:
    :param mkpath:
    :return:
    """
    with open(os.path.join(mkpath, '账号密码.csv'), 'w', encoding='utf-8') as f:
        f.write("{},{}".format(tax_number, password))


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


def handle_window(hwnd, extra, ):
    if win32gui.IsWindowVisible(hwnd):
        if 'UiBot' in win32gui.GetWindowText(hwnd):
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def close_api():
    win32gui.EnumWindows(handle_window, None)  # 枚举列出所有窗口
    time.sleep(5)


def open_uibot():
    time.sleep(1)
    install_dir1 = os.path.join(os.environ.get("LOCALAPPDATA"), 'UiBot Creator Community')
    install_dir2 = os.path.join(os.environ.get("LOCALAPPDATA"), 'UiBotCreator')

    install_dir3 = os.path.join(os.environ.get("PROGRAMFILES(X86)"), 'UiBot Creator Community')
    install_dir4 = os.path.join(os.environ.get("PROGRAMFILES(X86)"), 'UiBotCreator')

    if os.path.exists(install_dir1):
        win32api.ShellExecute(0, 'open', os.path.join(install_dir1, 'Creator'), '', '', 1)
    if os.path.exists(install_dir2):
        win32api.ShellExecute(0, 'open', os.path.join(install_dir2, 'Creator'), '', '', 1)
    if os.path.exists(install_dir3):
        win32api.ShellExecute(0, 'open', os.path.join(install_dir3, 'Creator'), '', '', 1)
    if os.path.exists(install_dir4):
        win32api.ShellExecute(0, 'open', os.path.join(install_dir4, 'Creator'), '', '', 1)

    time.sleep(8)
    win32api.SetCursorPos([1000, 420])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(2)


def main():
    # consumer
    logger.info("kafka server is {},topic is [{}]".format(SERVER, TOPIC))
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=SERVER,
        group_id='rpa-worker',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        consumer_timeout_ms=3 * 1000,
    )

    STATUS = False  # 控制日志提示信息

    logger.info("rpa worker started!")
    while True:
        if os.path.exists("lock.txt"):
            if not STATUS:
                logger.info("worker is running, suspended...")
                STATUS = True
            time.sleep(5)
            continue
        try:
            message = next(consumer)
            consumer.commit()
            message_str = message.value.decode("utf-8")
            logger.info("receive message: {}".format(message_str))
            message_dict = json.loads(message_str)
            handle_message(message_dict)
        except StopIteration as se:
            # logger.info("receive no message from kafka, continue pulling...")
            time.sleep(.1)
        except Exception as e:
            logger.error(e)
        finally:
            STATUS = False


def handle_message(message):
    sw_type_key = "sw_type"
    declare_id_key = "declareId"
    if not isinstance(message, dict):
        raise TypeError("message must be dict!")
    if sw_type_key not in message or declare_id_key not in message:
        raise TypeError("message must contain {} and {} ".format(sw_type_key, declare_id_key))
    sw_type = message.get(sw_type_key)
    declare_id = message.get(declare_id_key)
    url = SPECIAL_URL + declare_id
    try:
        response = requests.get(url).text
        if "username" not in response:
            raise TypeError("response key error from {}".format(url))
        logger.info('当前信息获取成功，报税公司id为{} ！！'.format(declare_id))
        with open("lock.txt", mode='w', encoding="utf-8") as f:
            f.write(declare_id)
        logger.info("create lock file success!")
        save_table(response, declare_id)
        logger.info("create local excel file success!")
        call_uibot()
        logger.info("call uibot success!")
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()
    # call_uibot()