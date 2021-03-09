import time
from io import BytesIO
from PIL import Image
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


class SVC:

    def __init__(self):

        self.url = 'https://beian.miit.gov.cn/#/Integrated/index'
        self.driver = webdriver.Chrome(executable_path=r'D:\wxt-new\chromedriver_win32\chromedriver.exe')
        self.driver.get(self.url)
        time.sleep(1)

        self.driver.maximize_window()
        self.driverwait = WebDriverWait(self.driver, 20)
        self.location = {}
        self.size = {'width': 260, 'height': 160}
        self.BORDER = 40

        self.driver.find_element_by_xpath('//input[@class="el-input__inner"]').send_keys('浙江中禄财务咨询有限公司')
        self.driver.find_element_by_xpath('//i[@class="el-icon-search"]').click()
        time.sleep(2)
        # data = self.driver.page_source
        # tree111 = etree.HTML(data)
        # bgImg = tree111.xpath('//img[@id="bgImg"]/@src')[0].split('base64,')[-1]

        # import base64
        # with open('bgImg.png', 'wb') as f:
        #     f.write(base64.b64decode(bgImg))
    def __del__(self):
        self.driver.close()

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
        slider = self.driverwait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'sildeblock')))
        return slider

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

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 0
        print(image1.size[0])
        print(image1.size[1])
        # exit()
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
        for i in range(round(distance / 40)):
            list1.append(10)
            list2.append(20)
            list2.append(10)
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
        print('over')

    def crack(self):
        Image2 = Image.open('a1.png')
        Image1 = Image.open('a.png')
        gap = self.get_gap(Image1, Image2)
        gap = 141
        print('缺口位置', gap)
        # exit()
        # # 减去缺口位移
        # if gap < 45:
        #     gap -= 5
        # elif gap < 55:
        #     gap -= 15
        # elif gap < 125:
        #     gap -= 25
        # elif gap < 165:
        #     gap -= 35
        # elif gap < 185:
        #     gap -= 40
        # else:
        #     gap -= 45
        track = self.get_track(gap)
        print('滑动轨迹', track)
        slider = self.get_slider()
        self.move_to_gap(slider, track)
        time.sleep(1)


if __name__ == '__main__':
    svc = SVC()
    svc.crack()