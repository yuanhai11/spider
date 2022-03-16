# encoding=utf-8

# 对界面的要求比较高，很大几率识别不出来。但是基本可以实现UIBOT的效果
import time

import rpa as r
import win32con


def login():
    r.init(visual_automation=True,chrome_browser=False)
    r.run('E:\soft_isruning_position\WXWork\WXWork.exe')
    r.click("h.jpg")
    r.click("3.png")
    r.wait(1.5)

    is_true = r.exist("aa.png")
    print(is_true)
    if is_true:
        r.snap("step-6.png",filename_to_save=r"D:\projects\S_Git_proj\spider\Other\spider_all\Rpa-Python\image")
        print("截图")
        print("进行图片传输")
        r.wait(1.5)

        is_true = r.exist('step-1.png')
        if is_true:
            print("login success")
        else:
            print("login fail")


def add():
    r.init(visual_automation=True,chrome_browser=False)
    r.run('E:\soft_isruning_position\WXWork\WXWork.exe')
    pass

def logout():
    r.init(visual_automation=True,chrome_browser=False)
    r.run('C:\Servyou\EPPortal_DS3.0\EPEvenue_SH.exe')

    if r.exist("a.png"):

        r.click("a.png")
        r.click("b.png")
        r.click("c.png")
    # 13s
    pass

def check():
    a = r.init(visual_automation=True, chrome_browser=False)
    print(a)
    b = r.run(r'C:\Users\20945\AppData\Local\UB_Store\Store.exe')
    print(b)
    r.click(0, 0)
    r.rclick(0.0)

    pass

def test_win32api():
    import win32api
    # 日报软件启动
    win32api.ShellExecute(0, 'open', r'C:\Users\20945\AppData\Local\UB_Store\Store.exe', '', '', 1)
    from ctypes import windll
    time.sleep(5)
    # 鼠标点击，先移动鼠标到对应位置

    windll.user32.SetCursorPos(300,570)
    # 左键按下，0, 0(x, y)由于我是鼠标直接移动过去的，所以当前位置点击下去即可
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.05)
    # 左键抬起
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

if __name__ == '__main__':
    # check()
    # logout()
    test_win32api()