class Config(object):
    """
    Common configurations
    """

class DevelopmentConfig(Config):
    """
    Development config
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production config
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
