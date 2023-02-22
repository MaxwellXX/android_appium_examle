from appium.webdriver.common.mobileby import MobileBy as By
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from time import sleep
from util.adbs import ADB


class BasePage(object):
    def __init__(self,driver):
        self.driver=driver
        self.adb = ADB('192.168.3.118:5555')

    def find_element(self,*args):
        return self.driver.find_element(*args)

    def find_elements(self,*args):
        return self.driver.find_elements(*args)

    def element_displayed(self, element):
        return element.is_displayed()

    def click_map(self, positions):
        self.driver.tap(positions=positions)

    def zoom_in_map(self, speed=0.2):
        """
        放大地图
        速率可调， 默认0.2
        :return:
        """
        driver = self.driver
        zoom_action = MultiAction(driver)
        action1 = TouchAction(driver)
        action2 = TouchAction(driver)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        # print("x,y :", x, y) x,y : 1080 2034
        # 两个点在屏幕的位置，一个是0.4， 一个是0.6
        point_from = [0.4, 0.6]
        point_to = [point_from[0] - speed, point_from[1] + speed]
        # 当speed = 0.2时，从屏幕0.4滑到到0.2，放大
        action1.press(x=x * point_from[0], y=y * point_from[0]).wait(1000).move_to(x=x * point_to[0], y=y * point_to[0]).release()
        # 当speed = 0.2时，从屏幕0.6滑到到0.8，放大
        action2.press(x=x * point_from[1], y=y * point_from[1]).wait(1000).move_to(x=x * point_to[1], y=y * point_to[1]).release()

        zoom_action.add(action1, action2)
        zoom_action.perform()

    def zoom_out_map(self, speed=0.2):
        """
        缩小地图
        速率可调， 默认0.2
        :return:
        """
        driver = self.driver
        zoom_action = MultiAction(driver)
        action1 = TouchAction(driver)
        action2 = TouchAction(driver)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        # print("x,y :", x, y) x,y : 1080 2034
        # 两个点在屏幕的位置，一个是0.4， 一个是0.6
        point_to = [0.4, 0.6]
        point_from = [point_to[0] - speed, point_to[1] + speed]

        # 当speed = 0.2时，从屏幕0.4滑到到0.2，放大
        action1.press(x=x * point_from[0], y=y * point_from[0]).wait(1000).move_to(x=x * point_to[0],
                                                                                   y=y * point_to[0]).release()
        # 当speed = 0.2时，从屏幕0.6滑到到0.8，放大
        action2.press(x=x * point_from[1], y=y * point_from[1]).wait(1000).move_to(x=x * point_to[1],
                                                                                   y=y * point_to[1]).release()
        '''
        # 当speed = 0.2时，从屏幕0.2滑到到0.4，缩小
        action1.press(x=x * 0.2, y=y * 0.2).wait(1000).move_to(x=x * 0.4, y=y * 0.4).wait(1000).release()
        # 当speed = 0.2时，从屏幕0.8滑到到0.6，缩小
        action2.press(x=x * 0.8, y=y * 0.8).wait(1000).move_to(x=x * 0.6, y=y * 0.6).wait(1000).release()
        '''
        zoom_action.add(action1, action2)
        zoom_action.perform()

    def drag_map(self, direction, speed = 0.2):
        """
        拖拽地图
        方向上下左右
        速率可调， 默认0.2
        :return:
        """
        driver = self.driver
        action1 = TouchAction(driver)
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        # print("x,y :", x, y) # x,y : 1080 2034
        direction = direction.upper()
        if direction == 'UP':
            action1.press(x=x * 0.5, y=y * 0.5).wait(1000).move_to(x=x * 0.5, y=y * (0.5-speed)).release().perform()
        elif direction == 'DOWN':
            action1.press(x=x * 0.5, y=y * 0.5).wait(1000).move_to(x=x * 0.5, y=y * (0.5 + speed)).release().perform()
        elif direction == 'LEFT':
            action1.press(x=x * 0.5, y=y * 0.5).wait(1000).move_to(x=x * (0.5 - speed), y=y * 0.5).release().perform()
        elif direction == 'RIGHT':
            action1.press(x=x * 0.5, y=y * 0.5).wait(1000).move_to(x=x * (0.5 + speed), y=y * 0.5).release().perform()
        else:
            raise ValueError('Invalid direction value!')

    def open_venue_layer(self):
        venue = (By.XPATH, "(//android.widget.ImageButton)[1]")
        self.find_element(*venue).click()
        sleep(1)

    def open_store_layer(self):
        store = (By.XPATH, "(//android.widget.ImageButton)[2]")
        self.find_element(*store).click()
        sleep(1)

    def global_search(self, text):
        search_bar = (By.ID, "com.test.test_android:id/search_bar_text")
        self.find_element(*search_bar).click()
        self.find_element(*search_bar).send_keys(text)
        # self.adb.sendText("GagChXinTD-v-CHN-1")
        # self.find_element(*self.search_bar).send_keys("GagChXinTD-v-CHN-1")
        sleep(1)
        #self.adb.changeInputToYj() #不启用uni键盘无需该改输入法
        #print('change keyboard to Yijia')

    def click_on_global_search_result(self, search_result=(
        By.XPATH, "(//*[@resource-id='com.test.test_android:id/body')[0]")):
        
        self.find_element(*search_result).click()
        sleep(2)
        self.adb.input_enter()
        

if __name__ == '__main__':
    pass