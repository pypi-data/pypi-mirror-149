# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



from ruamel import yaml
from common.basePath import _dir

def write_yaml_data(key, value, filename=_dir + 'config/data.yaml'):
    """
    yaml文件写入方法:适用于从前段页面拿到返回值写入Yaml文件解决用例关联  如cookie,token等
    :param key:
    :param value:
    :param filename:
    :return:
    """
    with open(filename, "r", encoding="utf-8") as f:
        doc = yaml.round_trip_load(f)  # 将类型转换成list
        # print(doc)
        doc[key] = value

        with open(filename, "w", encoding="utf-8") as f:
            yaml.round_trip_dump(doc, f)