# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import pytest
import allure
from common.readYaml import load, read_yaml
from loguru import logger





@allure.epic('UI测试')
@allure.severity(allure.severity_level.NORMAL)
@allure.feature('登录模块')
class TestLogin:
    udata = load('loginData.yaml')
    url = read_yaml('url.test')

    def setup_class(self):
        logger.info(f'开始执行{TestLogin.__name__}模块测试')

    def teardown_class(self):
        logger.info(f'{TestLogin.__name__}模块测试完成')

    # @pytest.mark.xfail
    @allure.story('用户登录')
    @allure.title('测试数据：用户名：{user},密码：{password}')
    @pytest.mark.parametrize('user,password', udata)
    def testcase_01(self, browser, user, password):
        with allure.step('打开网页，点击登录'):
           #页面层业务流程
            pass
        with allure.step('输入用户名密码，点击确认'):
            #页面层业务流程
            pass
        with allure.step('断言'):
            try:
                pass
            except:
                pass
            else:
                pass

