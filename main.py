from app.flask.app import create_app
from config.app import AppConfig

app = create_app()

if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT)
