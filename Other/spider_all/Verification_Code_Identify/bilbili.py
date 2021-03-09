from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from io import BytesIO
import time, random


class Bilibili(object):

    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path=r'D:\wxt-new\chromedriver_win32\chromedriver.exe')

        # 隐式等待
        self.driver.implicitly_wait(3)
        self.url = 'https://beian.miit.gov.cn/#/Integrated/index'
        # 用户名
        self.user = '146wda'
        # 密码
        self.pwd = '123465'

    def close(self):
        '''
        关闭浏览器
        '''
        self.driver.quit()

    def input_user_pwd(self):
        '''
           输入用户名和密码
        '''
        # 进入登陆页面
        self.driver.get(self.url)
        time.sleep(3)
        # 文本框输入用户名

        self.driver.find_element_by_xpath('//input[@class="el-input__inner"]').send_keys('浙江中禄财务咨询有限公司')
        self.driver.find_element_by_xpath('//i[@class="el-icon-search"]').click()

        # tb_user.send_keys(self.user)
        # 文本框输入密码
        # tb_pwd = self.driver.find_element_by_id('login-passwd')
        # tb_pwd.send_keys(self.pwd)

    # 6.有阴影拼图的验证码图片&获取验证码图片
    def get_screenshot(self):
        '''
        获取屏幕截图
        '''
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))

        return screenshot


    def update_style(self):
        '''
            修改图片的style属性，显示无缺口的图片
        '''
        js = 'document.querySelectorAll("canvas")[3].style="display:block"'
        self.driver.execute_script(js)
        time.sleep(2)


    def get_position(self):
        '''
            获取截取验证码时的四条边
        '''
        # 定位到登陆按钮
        bt_login = self.driver.find_element_by_xpath('//a[@class="btn btn-login"]')
        # 模拟点击
        bt_login.click()
        time.sleep(2)
        # 获取验证码图片对象
        code_img = self.driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')
        time.sleep(2)

        location = code_img.location
        size = code_img.size

        # screenshot = self.get_screenshot()
        # print(screenshot.size)

        # 计算图片截取区域(左，上，右，下，的坐标值)
        left, top, right, buttom = location['x'], location['y'], location['x'] + size['width'], location['y'] + size[
            'height']
        return left, top, right, buttom


    def get_image(self):
        '''
            截取验证码图片
        '''
        # 获取验证码位置
        position = self.get_position()
        # 从屏幕截图中抠出有缺口的验证码图片
        captcha1 = self.get_screenshot().crop(position)
        # 修改style属性，显示无缺口的验证码图片
        self.update_style()
        # 从屏幕截图中抠出无缺口的验证码图片
        captcha2 = self.get_screenshot().crop(position)

        with open('captcha1.png', 'wb') as f1, open('captcha2.png', 'wb') as f2:
            captcha1.save(f1)
            captcha2.save(f2)

        return captcha1, captcha2

        # 7. 比较两个验证码图片获取验证码滑块的偏移量


    def is_pixel_equal(self, img1, img2, x, y):
        '''
            判断两张图片的同一像素点的RGB值是否相等
        '''
        pixel1, pixel2 = img1.load()[x, y], img2.load()[x, y]
        # print(pixel1,pixel2)
        # 设定一个比较基准
        sub_index = 60

        # 比较
        if abs(pixel1[0] - pixel2[0]) < sub_index and abs(pixel1[1] - pixel2[1]) < sub_index and abs(
                pixel1[2] - pixel2[2]) < sub_index:
            return True
        else:
            return False


    def get_gap_offset(self, img1, img2):
        '''
            获取缺口的偏移量
        '''
        x = int(img1.size[0] / 4.2)
        for i in range(x, img1.size[0]):
            for j in range(img1.size[1]):
                # 两张图片对比,(i,j)像素点的RGB差距，过大则该x为偏移值
                if not self.is_pixel_equal(img1, img2, i, j):
                    x = i
                    return x
        return x


        # 8.使用偏移值计算移动操作（轨迹）


    def get_track(self, offset):
        '''
           模拟人为拖动验证码滑块
        '''
        track = []
        # 滑块起始x坐标
        current = 5
        # 变速临界值

        border_point = int(offset * 3 / 5)
        # 设置时间间隔
        t = 0.2
        # 设置初速度
        offset += 4
        v = 0
        # 循环直到滑动到偏移值时退出
        while current < offset:
            # 根据是否临界点改变运动状态
            if current < border_point:
                # 加速度
                a = 1
            else:
                a = -0.5
            v0 = v
            v = v0 + a * t

            move = v0 * t + 0.5 * a * t * t

            current += move

            track.append(round(move))

        return track

        # 9.操作滑块按钮，模拟拖动滑块做验证登录


    def shake_mouse(self):
        """
        模拟人手释放鼠标抖动
        :return: None
        """
        ActionChains(self.driver).move_by_offset(xoffset=-2, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=2, yoffset=0).perform()


    def operate_slider(self, track):
        '''
           拖动滑块
        '''
        # 获取拖动按钮
        back_tracks = [-1, -1, -2, -1]
        slider_bt = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')

        # 点击拖动验证码的按钮不放
        ActionChains(self.driver).click_and_hold(slider_bt).perform()

        # 按正向轨迹移动
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
            # 先加速后减速效果也不是很好。
            # 每移动一次随机停顿0-1/100秒之间骗过了极验，通过率很高
            time.sleep(random.random() / 100)
        time.sleep(random.random())
        # 按逆向轨迹移动
        for i in back_tracks:
            time.sleep(random.random() / 100)
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
        # 模拟人手抖动
        self.shake_mouse()
        time.sleep(random.random())
        # 松开滑块按钮
        ActionChains(self.driver).release().perform()


    def do_captcha(self):
        '''
            实现处理验证码
        '''
        # 有缺口，无缺口图片
        img1, img2 = self.get_image()
        # 比较两个验证码图片获取验证码滑块的偏移量
        offset = self.get_gap_offset(img1, img2)
        print(offset)

        # 使用偏移值计算移动操作
        track = self.get_track(offset)

        # 操作滑块按钮，模拟拖动滑块做验证登录
        self.operate_slider(track)


    def login(self):
        '''
        实现主要的登陆逻辑
        '''
        # 来到登陆界面并输入账号密码
        self.input_user_pwd()
        # 处理验证码
        self.do_captcha()

        # 关闭浏览器
        self.close()


    def run(self):
        self.login()


if __name__ == '__main__':
    bili = Bilibili()
    bili.run()