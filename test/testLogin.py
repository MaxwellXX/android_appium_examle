import pytest
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy as By
from pages.loginPage import LoginPage

class TestLogin():
    # 设置 caps 的值
    def setup(self):
        self.desire_cap= {
            #默认是 Android
            "platformName":"android",
            #adb devices 的 sn 名称
            "deviceName":"da342a8c",
            #包名
            "appPackage":"com.test.test_android",
            #activity 名字
            "appActivity":".MainActivity",
            "noReset":"true",
            "unicodeKeyboard":True
        }
        #运行 appium，前提是要打开 appium server
        self.driver=webdriver.Remote("http://127.0.0.1:4723/wd/hub",self.desire_cap)
        self.driver.implicitly_wait(5)

    def test_login_invalid_user(self):
        sleep(5)
        lp = LoginPage(self.driver)
        lp.login('xxx@test.com', 'xxx')

        if lp.get_msgTitle().is_displayed():
            assert lp.get_msgTitle().get_attribute('text') == '温馨提示'
            assert lp.get_msgCont().get_attribute(
                'text') == 'Failed to login, error:请求失败，请稍后再试'
            assert lp.get_msgOK().is_enabled() is True
        lp.msgOK_click()
        msgAgain=None

        try:
            msgAgain=lp.get_msgTitle()
        except Exception as e:
            print(e)

        msgGone=False if msgAgain else True
        assert msgGone is True

    def test_login_valid_user(self):
        sleep(5)
        lp=LoginPage(self.driver)
        lp.login('xxx@test.com','nikola')
        sleep(2)
        assert  lp.get_mapView().is_displayed() is True

    def tearDown(self):
        self.driver.quit()
