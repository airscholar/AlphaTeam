import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Debug': DebugConfig
}
