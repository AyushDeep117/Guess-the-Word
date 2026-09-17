from flask import Flask, session
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
            return """
                <h1>Guess The Word</h1>
                <a href="/login">Login</a>
                <br>
                <a href="/register">Register</a>
            """

        return f"""
            <h1>Guess The Word</h1>
            <p>Welcome, {session["username"]}!</p>
            <p>Role: {session["role"]}</p>
            <a href="/logout">Logout</a>
        """

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)