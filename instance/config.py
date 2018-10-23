import os




# Base configuration
class Config(object):
    DEBUG = False
    SECRET = os.getenv('STOREMANAGER_SECRET', 'KeepYourSecretsToYourself')



# Dev configuration
class DevConfig(Config):
    DEBUG = True


# Test configuration
class TestConfig(Config):
    TESTING = True
    DEBUG = True


# Staging configuration
class StagingConfig(Config):
    DEBUG = True


# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'production': ProductionConfig 
}