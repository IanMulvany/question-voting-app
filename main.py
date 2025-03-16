from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
import os
import csv
from io import StringIO
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///ideas_prod.db"
)
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
    sort_by = request.args.get('sort', 'date')
    
    if sort_by == 'votes':
        ideas = Idea.query.order_by(Idea.votes.desc()).all()
    else:  # Default sort by date (ID)
        ideas = Idea.query.order_by(Idea.id.desc()).all()
        
    return render_template("questions.html", ideas=ideas, sort_by=sort_by)


@app.route("/submit-question")
def submit_question():
    return render_template("submit_question.html")


@app.route("/admin")
def admin():
    ideas = Idea.query.all()
    return render_template("admin.html", ideas=ideas)


@app.route("/admin/export-csv")
def export_csv():
    ideas = Idea.query.all()
    
    # Create a CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Title', 'Description', 'Votes'])
    
    # Write data
    for idea in ideas:
        writer.writerow([idea.id, idea.title, idea.description, idea.votes])
    
    # Prepare response
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"questions-{timestamp}.csv"
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )


@app.route("/admin/clear-questions", methods=["POST"])
def clear_questions():
    Idea.query.delete()
    db.session.commit()
    return jsonify({"status": "success", "message": "All questions have been cleared"})


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
