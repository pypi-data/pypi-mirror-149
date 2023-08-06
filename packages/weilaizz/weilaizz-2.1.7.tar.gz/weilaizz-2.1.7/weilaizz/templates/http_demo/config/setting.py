# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import os
from os.path import dirname, join



# 测试环境


# 预发布环境


# 生产环境


# 项目根目录
BASE_PATH = dirname(__file__).replace(r'\/'.replace(os.sep, ''), os.sep)

# 浏览器驱动文件地址
CHROME_DRIVER_PATH = join(BASE_PATH, 'drivers/chrome_driver.exe').replace(r'\/'.replace(os.sep, ''), os.sep)
EDGE_DRIVER_PATH = join(BASE_PATH, 'drivers/edge_driver.exe').replace(r'\/'.replace(os.sep, ''), os.sep)
FIREFOX_DRIVER_PATH = join(BASE_PATH, 'drivers/gecko_driver.exe').replace(r'\/'.replace(os.sep, ''), os.sep)
IE_DRIVER_PATH = join(BASE_PATH, 'drivers/IEDriverServer.exe').replace(r'\/'.replace(os.sep, ''), os.sep)
OPERA_DRIVER_PATH = join(BASE_PATH, 'drivers/opera_driver.exe').replace(r'\/'.replace(os.sep, ''), os.sep)


# 无头化
HEADLESS = False

# 隐式等待时间
IMPLICITLY_WAIT_TIME = 20

# 页面加载超时时间
PAGE_LOAD_TIME = 20

# JS异步执行超时时间
SCRIPT_TIMEOUT = 20

# 浏览器启动尺寸
WINDOWS_SIZE = (1920, 1024)

# chrome浏览器操作开关
CHROME_METHOD_MARK = True

# chrome启动参数开关
CHROME_OPTION_MARK = True

# chrome实验性质启动参数
CHROME_EXPERIMENTAL = {
        # 'mobileEmulation': {'deviceName': 'iPhone 6'},
        'excludeSwitches': ['enable-automation']
    }

# chrome窗口大小启动参数
CHROME_WINDOW_SIZE = ''

# chrome启动最大化参数
CHROME_START_MAXIMIZED = '--start-maximized'

# chrome隐式等待时间
CHROME_IMPLICITLY_WAIT_TIME = 30

