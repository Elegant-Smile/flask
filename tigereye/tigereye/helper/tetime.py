from datetime import datetime


def now():
    return datetime.now().strftime('%Y%m%d%H%M%S')
    #  strftime 接收以时间元组，并返回以可读字符串表示的当地时间
