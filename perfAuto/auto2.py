from pages.layerPage import LayerPage
from appium.webdriver.common.mobileby import MobileBy as By
from appium import webdriver
from time import sleep

def auto_test(interval, speed, count):
    """

    :param interval: 间隔，单位是秒
    :param speed: 缩放、拖拽长度相对于整屏的比例，只能为0-1里的小数，越高越快
    :param count: 缩放、拖拽多少次
    :return:
    """
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

    lp = LayerPage(driver)
    lp.login('xxx@test.com', 'nikola')

    lp.global_search('测试地图点位名称')
    lp.click_on_global_search_result(search_result=(
        By.XPATH, "//*[@resource-id='com.test.test_android:id/body' and @text='测试地图点位名称'] "))
    lp.open_venue_layer()
    lp.open_store_layer()

    for i in range(1, count):
        print('zoom_out_map, ', i)
        lp.zoom_out_map(speed)
        sleep(float(interval))

    for i in range(1, count):
        print('zoom_in_map, ', i)
        lp.zoom_in_map(speed)
        sleep(float(interval))

    for i in range(1, count/2):
        print('zoom_out_map again, ', i)
        lp.zoom_out_map(speed)
        sleep(float(interval))

    for i in range(1, count):
        lp.drag_map('UP', speed)
        print('up, ', i)
    for i in range(1, count):
        lp.drag_map('DOWN', speed)
        print('DOWN, ', i)
    for i in range(1, count):
        lp.drag_map('left', speed)
        print('left, ', i)
    for i in range(1, count):
        lp.drag_map('RIGHT', speed)
        print('RIGHT, ', i)


if __name__ == '__main__':
    auto_test(3, 0.1, 11)



