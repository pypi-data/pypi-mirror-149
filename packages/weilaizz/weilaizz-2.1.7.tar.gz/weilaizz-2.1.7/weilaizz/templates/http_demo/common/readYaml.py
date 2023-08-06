# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import yaml
import os
from common.basePath import _dir
from loguru import logger

def read_yaml(key, filename=_dir + 'config/data.yaml'):
    """读取yaml文件并return文件"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        keys = key.split(".")
        for k in keys:
            data = data[k]
        return data


def load_yaml(file_path):
    """读取yaml并return"""
    logger.info("加载 {} 文件......".format(file_path))
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def load(file_name, path=_dir):
    """在项目内读取指定文件"""
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            data = load(file_name, c_path)
            if data is not None:
                return data
        elif file_name == i:
            data = load_yaml(c_path)
            return data







if __name__ == '__main__':
    print(read_yaml('url.dev'))