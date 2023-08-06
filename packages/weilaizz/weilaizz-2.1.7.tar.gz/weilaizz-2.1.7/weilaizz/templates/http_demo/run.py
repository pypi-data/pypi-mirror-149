# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------

import pytest

from config.runConfig import mainSetup as ms, mainTearDown as mt

if __name__ == '__main__':
    ms()        #测试前置
    pytest.main()
    mt()        #测试后置




