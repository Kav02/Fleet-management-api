import os

class Config:
    '''Configuration class for the fleet management API.'''

    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PGSQL_USER')}:{os.getenv('PGSQL_PASSWORD')}@{os.getenv('PGSQL_HOST')}/{os.getenv('PGSQL_DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/swagger'
    API_URL = 'http://localhost:5000/apidocs/swagger.json'



class DevelopmentConfig(Config):
    '''Configuration class for development environment.'''
    DEBUG = True


config = {
    'development': DevelopmentConfig
}
