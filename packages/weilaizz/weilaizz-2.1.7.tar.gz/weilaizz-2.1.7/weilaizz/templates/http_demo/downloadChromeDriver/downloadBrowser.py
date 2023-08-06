# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------

import requests
import winreg
import zipfile
from selenium import webdriver
import os

url = 'https://registry.npmmirror.com/-/binary/chromedriver/'  # 谷歌浏览器下载LINK


def get_chrome_vs():
    """获取系统中chrome的版本"""
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    return version


def get_chromedriver_vs():
    """查询系统内的Chrome驱动版本"""
    outstd2 = os.popen('chromedriver --version').read()
    return outstd2.split(' ')[1]


def download_driver(download_url):
    """下载浏览器驱动"""
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:
        zip_file.write(file.content)
        print('下载成功')


def unzip_driver(path=None):
    '''解压Chromedriver压缩包到指定目录'''
    if not path:
        path = os.getcwd()
    try:
        with zipfile.ZipFile(os.path.join(path, "chromedriver.zip"), 'r') as f:
            for file in f.namelist():
                f.extract(file, path)
        return True
    except zipfile.error:
        return False


def check_update_chromedriver():
    chromeVersion = get_chrome_vs()
    driverVersion = get_chromedriver_vs()
    if driverVersion != chromeVersion:
        print("chromedriver版本与chrome浏览器不兼容，更新中>>>")
        download_url = f"{url}{chromeVersion}/chromedriver_win32.zip"
        download_driver(download_url=download_url)
        unzip_driver()

        if not unzip_driver():
            print("暂无法找到与chrome兼容的chromedriver版本，请在http://npm.taobao.org/mirrors/chromedriver/ 核实。")
        os.remove("chromedriver.zip")
        print('更新后的Chromedriver版本为：', get_chromedriver_vs())
        return True
    else:
        print("chromedriver版本与chrome浏览器相兼容，无需更新chromedriver版本！")
        return False


def get_chrome_driver(path=None):
    """返回一个chromedriver"""
    if not path:
        path = "../common"
    return webdriver.Chrome()


if __name__ == "__main__":
    # print(get_chrome_vs())
    # print(get_chromedriver_vs())
    # download_driver('https://registry.npmmirror.com/-/binary/chromedriver/95.0.4638.54/chromedriver_win32.zip')
    # unzip_driver()
    # # check_update_chromedriver()
    get_chrome_driver()
