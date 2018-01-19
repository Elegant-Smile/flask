from tigereye.configs.default import  DefalutConfig

class Testconfig(DefalutConfig):

    TESTING = True
    # 提速用的s
    JSON_SORT_KEYS = False
    SQLALCHEMY_ECHO = False
    # sqlite 不写地址,直接运行在内存,运行完就删除
    SQLALCHEMY_DATABASE_URI = 'sqlite://'