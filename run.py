from src.app import create_app

app = create_app('development')

if __name__ == '__main__':
    # app.config.from_object(config['development'])

    app.run()
