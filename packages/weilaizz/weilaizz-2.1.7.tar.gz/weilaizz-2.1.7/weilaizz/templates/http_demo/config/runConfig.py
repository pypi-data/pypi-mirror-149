# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import os
import platform
from env import globa
from basePath import _dir
from common.clearFile import clearLog as cl, clearFile as cf
from shutil import copyfile
from wenv import write_env


def mainSetup():
    """测试前置"""
    # 设置全局变量，用于命名log文件
    globa._init()
    globa.set_val('name', 'web')
    # 清空一天前的log
    logdir = _dir + r'\log'
    cl(logdir)
    # 获取系统信息并写入environment.properties
    file = _dir + r'\env\environment.properties'
    sys_info = platform.uname().system
    w = write_env.parse(file)
    w.put('OS', sys_info)
    # 清空imgs
    imgdir = _dir + r'\imgs'
    cf(imgdir)


def mainTearDown():
    """测试后置"""
    # 复制环境变量文件到xml
    source = _dir + r'\report\environment.properties'
    target = _dir + r'\report\xml\environment.properties'
    copyfile(source, target)
    # 生成allure报告
    os.system('allure generate --clean ./report/xml -o ./report/html')  # --clean 清空上次报告

