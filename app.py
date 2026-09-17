from flask import Flask

from config import Config
from routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return "Guess The Word - Application Running"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)