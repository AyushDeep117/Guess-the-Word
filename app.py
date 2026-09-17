from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Guess The Word - Application Running"


if __name__ == "__main__":
    app.run(debug=True)