from time import sleep
from pages.loginPage import LoginPage
from appium.webdriver.common.mobileby import MobileBy as By
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from util.finditem import find_layer1_in_map
from util.finditem import find_layer2_in_map
import random
import os


class LayerPage(LoginPage):
    def __init__(self, driver, source='layer1_in_map'):
        super().__init__(driver)
        self.source = source


    def get_item_coord(self, source, screen_shot_path):
        if source == 'layer1_in_map':
            coord = find_layer1_in_map(screen_shot_path, visualized=False)
        elif source == 'layer2_in_map':
            coord = find_layer2_in_map(screen_shot_path, visualized=False)
        if coord:
            return coord
        else:
            raise ValueError('Cannot find any item in current region!')

    def click_item_with_count(self, source, screen_shot_path, count, interval):
        coord = self.get_item_coord(source, screen_shot_path)
        index = [random.randint(0, len(coord)-1) for _ in range(count if count<len(coord) else len(coord))]
        print(len(index), index)
        for i, j in enumerate(index):
            self.click_map(positions=[coord[j]])
            print('clicked {} times'.format(i))
            sleep(float(interval))

    def click_item_and_open_detail_with_count(self, source, screen_shot_path, count, interval):
        coord = self.get_item_coord(source, screen_shot_path)
        index = [random.randint(0, len(coord)) for _ in range(count if count<len(coord) else len(coord))]
        print(len(index), index)
        for i, j in enumerate(index):
            print('try to click the {} time'.format(i))
            if self.click_item_and_open_close_detail(positions=[coord[j]]) == 'restart':
                break
            sleep(float(interval))

    def click_item_and_open_close_detail(self, positions):
        self.click_map(positions)
        print('clicked map, position: {}'.format(positions))
        sleep(1)
        self.open_detail_page()
        if self.close_detail_page() == 'back':
            return 'restart'
        return 'continue'

    def open_detail_page(self):
        try:
            self.find_element(By.ID, "com.test.test_android:id/detail_title")
            action1 = TouchAction(self.driver)
            action1.press(x=545, y=1939).wait(1000).move_to(x=545, y=1600).release().perform()
            print('swipe up detail to open page')
        except NoSuchElementException:
            print('not finding a detail title, might be layer2_in_map list cluster? checking ')
            try:
                self.find_element(By.ID, "com.test.test_android:id/main_title").click()
                print('clicked layer2_in_map list')
            except NoSuchElementException:
                print('no bottom detail or layer2_in_maplist opened, nothing to open!')

    def close_detail_page(self):
        try:
            self.find_element(By.XPATH, "//android.widget.TextView[@resource-id='com.test.test_android:id/formElementTitle']")
            action1 = TouchAction(self.driver)
            action1.press(x=545, y=1000).wait(1000).move_to(x=545, y=1600).release().perform()
            print('swipe down to close detail')
        except NoSuchElementException:
           print('no item detail opened, try to find layer2_in_map list')
           self.close_layer2_in_map_list_page()

    def close_layer2_in_map_list_page(self):
        try:
            self.find_element(By.XPATH, "//android.widget.TextView[@resource-id='com.test.test_android:id/layer2_in_map_list_section_title']")
            self.driver.back()
            print('driver go back to close layer2_in_map list ')
            return 'back'
        except NoSuchElementException:
            print('no detail page opened, nothing to close!')
            return 'ok'


if __name__ == '__main__':

    desire_cap = {
        # 默认是 Android
        "platformName": "android",
        # adb devices 的 sn 名称
        # "deviceName": "da342a8c",
        "deviceName": "192.168.3.118:5555",
        # 包名
        "appPackage": "com.test.test_android",
        # activity 名字
        "appActivity": ".MainActivity",
        # "noReset": "true",
        "unicodeKeyboard": False
    }
    # 运行 appium，前提是要打开 appium server
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desire_cap)
    driver.implicitly_wait(5)

    lp = LayerPage(driver,source='layer2_in_map')
    lp.login('xxx@test.com', 'nikola')

    lp.global_search('测试地图点位名称')
    lp.click_on_global_search_result(search_result=(
        By.XPATH, "//*[@resource-id='com.test.test_android:id/body' and @text='测试地图点位名称'] "))
    lp.open_layer1_in_map_layer()
    lp.open_layer2_in_map_layer()

    path_current_directory = os.path.dirname(os.path.dirname(__file__))
    screenshot_path = os.path.join(path_current_directory, 'pics/layer1_in_map_layer2_in_map_1.png')
    lp.zoom_out_map(0.3)
    sleep(5)
    driver.get_screenshot_as_file(screenshot_path)

    #lp.click_item_with_count(source='layer2_in_map',screen_shot_path=screenshot_path, count=200, interval=2)
    lp.click_item_and_open_detail_with_count(source='layer2_in_map', screen_shot_path=screenshot_path, count=200, interval=2)
    sleep(1)
    #lp.open_detail_page()
    #lp.close_detail_page()