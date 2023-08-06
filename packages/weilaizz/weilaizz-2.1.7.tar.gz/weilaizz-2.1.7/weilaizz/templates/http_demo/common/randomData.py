# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------

import random
import base64
import time
from faker import Faker


def createUserPassword():
    """
    随机生成用户名和密码
    :return: 用户名和密码，元组类型
    """
    usableName_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"  # 可作为用户名的字符
    usablePassword_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"  # 可作为密码的字符，根据所需可适当增减
    usableName_char1 = '1234567890'
    e_userName = []
    e2_userName = []
    e_userPassword = []

    for i in range(random.randint(1, 6)):
        e_userName.append(random.choice(usableName_char))
        e2_userName.append(random.choice(usableName_char1))
    for j in range(6):
        e_userPassword.append(random.choice(usablePassword_char))
    e_userName = e_userName + ['_'] + e2_userName
    userName = ''.join(e_userName)
    userPassword = ''.join(e_userPassword)

    return userName, userPassword


# fake 假数据构造

fk = Faker(locale='zh_CN')


def random_mobile():
    """随机生成手机号"""
    return fk.phone_number()


def random_name():
    """随机生成中文名字"""
    return fk.name()


def random_ssn():
    """随机生成一个省份证号"""
    return fk.ssn()


def random_addr():
    """随机生成一个地址"""
    return fk.address()


def random_city():
    """随机生成一个城市名"""
    return fk.city()


def random_company():
    """随机生成一个公司名"""
    return fk.company()


def random_postcode():
    """随机生成一个邮编"""
    return fk.postcode()


def random_email():
    """随机生成一个邮箱号"""
    return fk.email()


def random_date():
    """随机生成一个日期"""
    return fk.date()


def radom_date_time():
    """随机生成一个时间"""
    return fk.date_time()


def random_ipv4():
    """随机生成一个ipv4的地址"""
    return fk.ipv4()


def get_timestamp():
    """生成当前时间戳"""
    return time.time()


def base64_encode(data: str):
    """base64编码"""
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')


def md5_encrypt(data: str):
    """md5加密"""
    from hashlib import md5
    new_md5 = md5()
    new_md5.update(data.encode('utf-8'))
    return new_md5.hexdigest()