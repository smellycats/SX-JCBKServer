# -*- coding: utf-8 -*-

class Config(object):
    # 密码 string
    SECRET_KEY = 'thefatboy'
    # 服务器名称 string
    HEADER_SERVER = 'SX-JCBKServer'
    # 加密次数 int
    ROUNDS = 123456
    # token生存周期，默认2小时 int
    EXPIRES = 7200
    # 数据库连接 string
    SQLALCHEMY_DATABASE_URI = 'mysql://kakou:123@127.0.0.1/jcbk'
    # 数据库连接 dict
    SQLALCHEMY_BINDS = {}
    # 连接池大小 int
    #SQLALCHEMY_POOL_SIZE = 20
    # 白名单启用 bool
    #WHITE_LIST_OPEN = False
    # 白名单列表 set
    #WHITE_LIST = set(['127.0.0.1'])
    JCBK_URL = 'http://123.123.123.123:8099/jcbkproxy/jcbktrans/services/hole?wsdl'
    JCBK_DICT = {}


class Develop(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False

