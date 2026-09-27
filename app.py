from flask import Flask, session, redirect, url_for
from routes.admin_routes import admin_bp
from config import Config
from routes.auth_routes import auth_bp
from routes.game_routes import game_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(admin_bp)
    app.config.from_object(Config)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        if session["role"] == "ADMIN":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("auth.dashboard"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)