from flask import Flask, url_for, request, session, redirect, render_template
from flask_socketio import SocketIO, send, join_room, leave_room
import random
from string import ascii_uppercase


app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
socketio = SocketIO(app)

db = {}

def generate_room_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in db:
            break
    return code


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        room = request.form.get("room")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not username:
            return render_template("login.html", error="Username is required", username=username, room=room)
        
        if join != False and not room:
            return render_template("login.html", error="Room is required to join", username=username, room=room)
        
        if create != False:
            room = generate_room_code(4)
            db[room] = {"members": 0, "users": [], "messages": []}
        elif room not in db:
            return render_template("login.html", error="Room does not exist", username=username, room=room)

        session["username"] = username
        session["room"] = room
        return redirect(url_for("room"))
    
    else:
        return render_template("login.html")


@app.route("/room", methods=["GET", "POST"])
def room():
    if "username" not in session or "room" not in session:
        return redirect(url_for("login"))
    return render_template("room.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    socketio.run(app, debug=True)