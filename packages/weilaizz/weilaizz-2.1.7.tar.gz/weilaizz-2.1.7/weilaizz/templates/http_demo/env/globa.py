# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



def _init():
    """全局变量初始化,此方法在项目中只可运行一次
    """
    global _global_dict
    _global_dict = {}


def set_val(name, val):
    """设置全局变量"""
    _global_dict[name] = val


def get_val(name):
    """获取全局变量"""
    try:
        return _global_dict[name]
    except KeyError:
        return None
