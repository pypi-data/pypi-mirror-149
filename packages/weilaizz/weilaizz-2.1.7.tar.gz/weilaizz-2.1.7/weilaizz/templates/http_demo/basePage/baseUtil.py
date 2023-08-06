# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import time
import allure
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from loguru import logger
from common.basePath import _dir

from common.runTime import _runtime


class BaseUtil():

    #初始化需浏览器回参
    def __init__(self ,driver, page_name=''):

        self.driver=driver
        self.page = page_name

    def get(self, url):

        try:
            logger.info(f'打开:{url}')
            self.driver.get(url)
        except Exception:
            raise

    #等待元素匿名函数+显示等待,返回定位元素
    def _find_element(self, ele, timeout_=30, poll_=0.5,  msg=''):

        if not isinstance(ele, tuple):
            raise TypeError('loc参数类型错误，必须是元组；loc = ("id", "value1")')

        else:
            try:
                logger.info('定位{}页面元素：{}, 元素描述：{}'.format(self.page, ele, msg))
                start_time = time.time()
                _wait = WebDriverWait(self.driver, timeout=timeout_, poll_frequency=poll_)
                _location = _wait.until(lambda x: x.find_element(*ele))
                end_time = time.time()
            except Exception:
                logger.error('元素定位失败!')
                self._save_screenshot()
                raise
            else:
                logger.info('元素定位成功：耗时{}秒!'.format(round(end_time - start_time, 3)))
                return _location

    #截图
    @_runtime
    def _save_screenshot(self):

        name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        filepath = _dir + r'\img\{}.png'.format(name)
        try:
            self.driver.save_screenshot(filepath)
            logger.info("截屏成功,图片路径为{}".format(filepath))
            sleep(1)
            allure.attach.file(filepath, name, allure.attachment_type.PNG)
        except Exception:
            logger.error("截屏失败")

    #点击
    @_runtime
    def _click(self,loc):

        try:
            ele=self._find_element(loc)
            ele.click()
            logger.info("点击成功")
        except:
            self._save_screenshot()
            logger.error("点击失败")

    #输入
    def _input(self,loc,txt):

        try:
            ele=self._find_element(loc)
            ele.clear()
            ele.semd_keys(txt)
            logger.info("输入成功,输入内容:{}".format(txt))
        except:
            self._save_screenshot()
            logger.error("输入失败,输入内容:{}".format(txt))