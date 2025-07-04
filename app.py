from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os
from random import choice

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}
waiting_list = []

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/mindfulness")
def mindfulness():
    return render_template("mindfullness.html")  # note the spelling with double 'l'

@app.route("/kindness")
def kindness():
    return render_template("kindness.html")
@app.route("/connect")
def connect_user():
    return render_template("connect.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

@socketio.on("new-user-joined")
def handle_new_user(name):
    users[request.sid] = {"name": name}
    if waiting_list:
        other_sid = waiting_list.pop(0)
        users[request.sid]["partner"] = other_sid
        users[other_sid]["partner"] = request.sid

        emit("connect-user", users[other_sid]["name"], to=request.sid)
        emit("connect-user", name, to=other_sid)
    else:
        waiting_list.append(request.sid)
        emit("waiting", "Waiting for someone to connect...", to=request.sid)

@socketio.on("send")
def handle_send(message):
    sender = request.sid
    if sender in users and "partner" in users[sender]:
        partner_sid = users[sender]["partner"]
        emit("receive", {"name": users[sender]["name"], "message": message}, to=partner_sid)
@socketio.on("typing")
def handle_typing(name):
    sender = request.sid
    if sender in users and "partner" in users[sender]:
        partner_sid = users[sender]["partner"]
        emit("typing", {"name": name}, to=partner_sid)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    user = users.pop(sid, None)
    if sid in waiting_list:
        waiting_list.remove(sid)
    if user and "partner" in user:
        partner_sid = user["partner"]
        if partner_sid in users:
            users[partner_sid].pop("partner", None)
            emit("user-disconnected", f"{user['name']} has left the chat.", to=partner_sid)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
