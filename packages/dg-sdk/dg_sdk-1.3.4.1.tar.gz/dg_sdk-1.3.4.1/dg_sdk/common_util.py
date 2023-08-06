import random
import time
import datetime
import functools
from fishbase import logger as fishbase_logger


def generate_mer_order_id():
    """
    生成请求order_no，根据时间戳+6位随机数
    :return:
    """
    timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    return "" + timestamp + str(random.randint(100000, 9999999))


def generate_req_date():
    """
    获取当前日期，格式%Y%m%d
    :return: 日期
    """
    return datetime.datetime.now().strftime('%Y%m%d')


def time_func(func):
    """
    计算方法耗时
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        data = 'func.__name__={}, func.inputs_args={}, \n' \
               'func.inputs_kwargs={}, \n' \
               'elapsed={} \n'.format(func.__name__, args, kwargs, end - start)
        fishbase_logger.info(data)
        return r

    return wrapper
