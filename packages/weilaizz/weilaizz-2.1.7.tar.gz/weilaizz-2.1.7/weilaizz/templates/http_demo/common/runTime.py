# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import random
import time
from functools import wraps

def _runtime(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("页面层业务方法[%s]运行时间为: %s seconds" %
              (function.__name__, str(t1 - t0))
              )

        return result

    return function_timer


@_runtime
def random_sort_(n):
  return sorted([random.random() for i in range(n)])

if __name__ == '__main__':
    random_sort_(300000)