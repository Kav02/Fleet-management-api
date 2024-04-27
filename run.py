from src.app import create_app
from src.config import config

app = create_app('development')

if __name__ == '__main__':
    app.config.from_object(config['development'])

    app.run()
