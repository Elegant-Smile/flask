import os


class DefalutConfig(object):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    DEBUG = True
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adminadmin@localhost/tigereye'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_ECHO = False

    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    #print(LOG_DIR)
