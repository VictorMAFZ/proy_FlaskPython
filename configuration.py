class BaseConfig():
    SECRET_KEY="123456"
    DEBUG = True
    TESTING = True

class DevConfig(BaseConfig):
    pass

class ProConfig(BaseConfig):
    DEBUG = False
    TESTING = False