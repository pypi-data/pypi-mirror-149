# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



from basePage import driver
from basePage.baseUtil import BaseUtil
from common.runTime import _runtime
from common.writeYaml import write_yaml_data

"""页面层两部分: 1.页面元素存放 2.页面动作执行"""
class LoginPage(BaseUtil):

    #页面元素:元组
    # 元素1 :()
    # 元素2 :()
    # 元素3 :()
    # 元素4 :()
    # 元素5 :()


    @_runtime
    def __init__(self):
        """
        初始化方法
        """
        driver.browserInit()
        super().__init__(driver)

    @_runtime
    def login(self):
        """
        页面业务流程
        :return:
        """
        pass

    @_runtime
    def write_yaml_token(self):
        """
        执行JS脚本获取token并写入yaml
        :return:
        """
        js = 'return window.localStorage.getItem("loginKey")'
        token = self.driver.execute_script(js)
        write_yaml_data('loginkey', token)
        print("token获取并写入成功")