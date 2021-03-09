import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class SVC:

    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driverwait = WebDriverWait(self.driver, 20)
        self.email = 'EMAIL'
        self.password = 'PASSWORD'
        self.location = {}
        self.size = {'width': 260, 'height': 160}
        self.BORDER = 40

    def __del__(self):
        self.driver.close()

    def setAttribute(self, elementObj, attributeName, value):
        # 封装设置页面对象的属性值的方法
        # 调用JavaScript代码修改页面元素的属性值，arguments[0]－［2］分别会用后面的
        # element、attributeName和value参数值进行替换，并执行该JavaScript代码
        self.driver.execute_script("arguments[0].setAttribute (arguments[1],arguments[2])", elementObj, attributeName,
                                   value)

    def removeAttribute(self, elementObj, attributeName):
        # 封装删除页面元素属性的方法
        # 调用JavaScript代码删除页面元素的指定的属性，arguments[0]－［1］分别会用后面的
        # element、attributeName参数值进行替换，并执行该JavaScript代码
        self.driver.execute_script("arguments[0].removeAttribute(arguments[1])", elementObj, attributeName)

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        # button = self.driver.find_element_by_xpath('//*[@id="captcha"]/div/div[2]/div[1]/div[3]')
        button = self.driverwait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.driverwait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.driver.get(self.url)
        email = self.driver.find_element_by_xpath('//*[@id="email"]')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        # email = self.driverwait.until(EC.presence_of_element_located((By.ID, 'email')))
        # password = self.driverwait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_geetest_image(self, name):
        """
        获取验证码图片 captcha.png
        :return: 图片对象
        """
        left, top, right, bottom = (
        self.location['x'] + 177, self.location['y'] + 44, self.location['x'] + self.size['width'] + 235,
        self.location['y'] + self.size['height'] + 80)
        print('验证码位置', left, top, right, bottom)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def getImg(self):
        time.sleep(3)
        ele = self.driver.find_elements_by_tag_name('canvas')
        self.location = ele[0].location
        self.setAttribute(ele[1], 'style', 'display: none;')  # 移除小方框
        self.get_geetest_image('captcha_up.png')
        self.setAttribute(ele[0], 'style', 'display: none;')  # 移除上面图片
        self.removeAttribute(ele[2], 'style')  # 移除隐藏属性以显示地面图片
        self.get_geetest_image('captcha_down.png')
        self.removeAttribute(ele[0], 'style')
        time.sleep(0.5)
        self.removeAttribute(ele[1], 'style')
        time.sleep(0.5)
        self.setAttribute(ele[2], 'style', 'display: none;')

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 0
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:

            return True
        else:
            print(pixel1, pixel2)
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        list1 = []
        list2 = []
        list3 = []
        # 当前位移
        for i in range(round(distance / 4)):
            list1.append(1)
            list2.append(2)
            list2.append(1)
        return list1 + list2

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def start(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()

    def crack(self):
        self.getImg()
        Image2 = Image.open('captcha_down.png')
        Image1 = Image.open('captcha_up.png')
        gap = self.get_gap(Image1, Image2)
        print('缺口位置', gap)
        # 减去缺口位移
        if gap < 45:
            gap -= 5
        elif gap < 55:
            gap -= 15
        elif gap < 125:
            gap -= 25
        elif gap < 165:
            gap -= 35
        elif gap < 185:
            gap -= 40
        else:
            gap -= 45
        track = self.get_track(gap)
        print('滑动轨迹', track)
        slider = self.get_slider()
        self.move_to_gap(slider, track)
        time.sleep(1)
        success = False
        try:
            success = self.driverwait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        except:
            print('失败')
        # 失败后重试
        if not success:
            time.sleep(0.1)
            self.crack()
        else:
            print('成功')
            self.login()

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.driverwait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        print('登录成功')


if __name__ == '__main__':
    svc = SVC()
    svc.start()
    svc.crack()