from openpyxl import load_workbook
from common.basePath import _dir

def r_xlsx(_fname, _sname="Sheet1"):
    """
    解析读取excel表格中数据,返回元组
    :param _fname:读取的文件路径
    :param _sname: 读取的具体的页业务数据
    """
    excel = load_workbook(_fname)
    data = []
    for value in excel[_sname].values:
        # print(value)
        if value[0] > 1:
            data.append(value[1:])
    excel.close()
    return data

if __name__ == '__main__':
    data = r_xlsx(_dir+'data/测试.xlsx')

    print(data)