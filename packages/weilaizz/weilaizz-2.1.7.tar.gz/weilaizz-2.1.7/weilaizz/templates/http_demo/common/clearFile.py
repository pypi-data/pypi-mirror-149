# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------


import os
import time

def clearFile(dir_path):
    """
    清除目录以及子目录下的文件
    :param dir_path: 路径
    :return: None
    """
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        # 获取目录下文件和文件夹列表
        ls = os.listdir(dir_path)
        # 删除目录下的所有文件及子目录下的所有文件
        for i in ls:
            c_path = os.path.join(dir_path, i) #将目录和文件名拼接
            if os.path.isdir(c_path):      #如果是目录继续调用清除函数
                clearFile(c_path)
            else:
                os.remove(c_path)

    else:
        raise NameError('路径不存在或者不是一个目录')


def clearLog(dir_path):
    """
    清空一天前生成的log
    :param dir_path: 目录路径
    :return: None
    """
    now_time = time.time() #获取现在时间戳
    if os.path.exists(dir_path) and os.path.isdir(dir_path): #判断路径是目录并且路径下有文件或者目录
        ls = os.listdir(dir_path)
        for i in ls:
            c_path = os.path.join(dir_path, i)  #将目录和文件名拼接
            if os.path.isdir(c_path):
                clearLog(c_path)
            else:
                cre_time = os.path.getmtime(c_path) #获取文件创建时间戳
                if cre_time < (now_time - 86400): #删除符合条件文件
                    os.remove(c_path)
    else:
        raise NameError('路径不存在或者不是一个目录')
