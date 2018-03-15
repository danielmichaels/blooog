import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    POSTS_PER_PAGE = 10


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardcoded_for_dev_only'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABSE_URI') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data-dev.sqlite')
    DEBUG = True


# class Staging(Config): # TODO: include this

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data.sqlite')
    # DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
