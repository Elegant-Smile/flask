class DefalutConfig(object):
    DEBUG = True
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:adminadmin@localhost/tigereye'
    SQLALCHEMY_TRACK_MODIFICATIONS = False