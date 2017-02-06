#coding=utf-8
'''
Created on 2016年12月27日

@author: huangning
'''
class Config(object):
    """Base config class."""
    SECRET_KEY = 'this is my secretkey'

class ProdConfig(Config):
    """Production config class."""
    pass

class DevConfig(Config):
    """Development config class."""
    DEBUG = True
    # MySQL connection
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@192.168.1.237/ricardonhuang'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
config = {
'development': DevConfig,
'production': ProdConfig,
'default': DevConfig
}