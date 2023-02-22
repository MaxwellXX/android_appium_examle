from time import sleep
from pages.basePage import BasePage
from appium.webdriver.common.mobileby import MobileBy as By
from appium import webdriver
import os

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # login
        self.uName=(By.ID, "com.test.test_android:id/loginUsername")
        self.uPwd=(By.ID, "com.test.test_android:id/loginPwd")
        self.loginBtn=(By.ID, "com.test.test_android:id/login_btn")
        # message
        self.msgTitle=(By.ID, "com.test.test_android:id/md_text_title")
        self.msgCont=(By.ID, "com.test.test_android:id/md_text_message")
        self.msgOK=(By.ID, 'com.test.test_android:id/md_button_positive')
        # login
        self.mapView=(By.ID, "com.test.test_android:id/mapView")
        self.left=(By.ID,"com.test.test_android:id/left_action")
        self.logoutIcon=(By.XPATH,"//[@resource-id='com.test.test_android:id/material_drawer_icon' and @text='Logout'] ")

    def get_uName(self):
        return self.find_element(*self.uName)

    def get_uPwd(self):
        return self.find_element(*self.uPwd)

    def get_loginBtn(self):
        return self.find_element(*self.loginBtn)

    def get_msgTitle(self):
        return self.find_element(*self.msgTitle)

    def get_msgCont(self):
        return self.find_element(*self.msgCont)

    def get_msgOK(self):
        return self.find_element(*self.msgOK)

    def get_mapView(self):
        return self.find_element(*self.mapView)

    def uName_fill(self, text):
        self.find_element(*self.uName).send_keys(text)

    def uPwd_fill(self, text):
        self.find_element(*self.uPwd).send_keys(text)

    def login_btn_click(self):
        self.find_element(*self.loginBtn).click()

    def msgOK_click(self):
        self.find_element(*self.msgOK).click()

    def left_click(self):
        self.find_element(*self.left).click()

    def logoutIcon_click(self):
        self.find_element(*self.logoutIcon).click()

    def login(self, user, pwd):
        #如果自动登录了，先登出
        autoLogin=None
        try:
            autoLogin=self.get_mapView().is_displayed()
        except Exception as e:
            print(e)

        if autoLogin:
            self.left_click()
            sleep(1)
            self.logoutIcon_click()
            sleep(1)

        if self.get_loginBtn().is_enabled():
            # 登录按钮可点击再进行操作
            if self.get_uName().get_attribute('text') != 'User ID':
                # 如果用户名已经有值了，清空再填
                self.get_uName().clear()
                sleep(1)
                self.uName_fill(user)
                sleep(1)
                self.get_uPwd().clear()
                sleep(1)
                self.uPwd_fill(pwd)
                sleep(1)
                self.login_btn_click()
                sleep(2)

if __name__ == '__main__':
    desire_cap = {
        # 默认是 Android
        "platformName": "android",
        # adb devices 的 sn 名称
        #"deviceName": "da342a8c",
        "deviceName": "192.168.3.118:5555",
        # 包名
        "appPackage": "com.test.test_android",
        # activity 名字
        "appActivity": ".MainActivity",
        #"noReset": "true",
        "unicodeKeyboard": False
    }
    # 运行 appium，前提是要打开 appium server
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desire_cap)
    driver.implicitly_wait(5)

    lp = LoginPage(driver)
    lp.login('anna@test.com', 'nikola')
    '''for i in range(1,5):
        print('zoom_out_map, ', i)
        lp.zoom_out_map(0.1)
    
    for i in range(1, 5):
        print('zoom_in_map, ', i)
        lp.zoom_in_map(0.1)
    
    for i in range(1, 5):
        lp.drag_map('UP', 0.1)
        print('up, ', i)
    for i in range(1, 5):
        lp.drag_map('DOWN', 0.1)
        print('DOWN, ', i)
    for i in range(1, 5):
        lp.drag_map('left', 0.1)
        print('left, ', i)
    for i in range(1, 5):
        lp.drag_map('RIGHT', 0.1)
        print('RIGHT, ', i)
    '''
    lp.global_search('测试地图点位名称')
    lp.click_on_global_search_result(search_result=(
        By.XPATH, "//*[@resource-id='com.test.test_android:id/body' and @text='测试地图点位名称'] "))
    lp.open_venue_layer()
    lp.open_store_layer()
    path_current_directory = os.path.dirname(os.path.dirname(__file__))
    screenshot_path = os.path.join(path_current_directory,'pics/xxx.png')
    lp.zoom_out_map(0.3)
    driver.get_screenshot_as_file(screenshot_path)