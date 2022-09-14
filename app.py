from config import Config
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_object(Config)


@app.route("/")
def index():
    title = "Flask App"
    return render_template("index.html", title=title)


if __name__ == "__main__":
    app.run(debug=True)
