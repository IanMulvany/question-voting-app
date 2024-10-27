from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ideas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    votes = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "votes": self.votes,
        }


@app.route("/")
def home():
    ideas = Idea.query.all()
    return render_template("index.html", ideas=ideas)


@app.route("/vote")
def vote():
    ideas = Idea.query.all()
    return render_template("vote.html", ideas=ideas)


@app.route("/questions")
def questions():
    ideas = Idea.query.all()
    return render_template("questions.html", ideas=ideas)


@app.route("/submit-question")
def submit_question():
    return render_template("submit_question.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@socketio.on("connect")
def on_connect():
    ideas = Idea.query.all()
    emit("init", [i.serialize() for i in ideas])


@socketio.on("submit_idea")
def on_submit_idea(data):
    idea = Idea(title=data["title"], description=data.get("description"))
    db.session.add(idea)
    db.session.commit()
    emit("idea", idea.serialize(), broadcast=True)


@socketio.on("vote")
def on_vote(data):
    idea = db.session.get(Idea, data["id"])
    if idea:
        idea.votes += data["change"]
        db.session.commit()
        emit("update_vote", idea.serialize(), broadcast=True)


@socketio.on("clear_board")
def on_clear_board():
    Idea.query.delete()
    db.session.commit()
    emit("clear_board", broadcast=True)


# Entry point for the application
if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
