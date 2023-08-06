# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------

import argparse
import os
import time
import weilaizz
from shutil import copytree

from weilaizz.core.logger import print_waring, print_error, print_info


def run(args):
    """创建项目"""
    if hasattr(args, "name"):
        name = args.name
        template_path = os.path.join(os.path.dirname(os.path.abspath(weilaizz.__file__)), 'templates')
        api_templates = os.path.join(template_path, 'http_demo')
        print_waring("""----------------------------------------
正在创建UI自动化脚手架项目:{}""".format(name))
        print_waring("创建进度25%")
        print_waring("创建进度50%")
        print_waring("创建进度100%")
        print_waring("----------------------------------------")

        try:
            copytree(api_templates, os.path.join(".", name))
        except Exception as e:
            time.sleep(1)
            print_error("--------------------------------------------------------------------")
            print_error("项目创建失败！:{}".format(e))
            print_error("--------------------------------------------------------------------")
        else:
            time.sleep(1)
            print_info("""----------------------------------------
项目创建成功！
祝大家,前程似锦

                        魏来Vx:14922227
----------------------------------------
                    """)


def create_parser():
    parser = argparse.ArgumentParser(prog='apin', description='ApiTest使用命令介绍')
    # 添加版本号
    parser.add_argument('-V', '--version', action='version', version='weilaizz 2.1.1')
    subparsers = parser.add_subparsers(title='Command', metavar="命令")
    # 创建项目命令
    create_cmd = subparsers.add_parser('run', help='create test project ', aliases=['C'])
    create_cmd.add_argument('name', metavar='project_name', help="project name")
    create_cmd.set_defaults(func=run)

    return parser


def main(params: list = None):
    """
    程序入口
    :param params: list
    :return:
    """
    parser = create_parser()
    # 获取参数
    if params:
        args = parser.parse_args(params)
    else:
        args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()



if __name__ == '__main__':
    main(['run', 'test'])
