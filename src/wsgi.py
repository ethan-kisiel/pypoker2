from flask import Flask, render_template, redirect, jsonify, request, url_for
from threading import Thread
from websocket_server import SocketServer

from managers.room_manager import RoomManager

socket_server = SocketServer("127.0.0.1", 4201)


room_manager = RoomManager()


socket_thread = Thread(target=socket_server.run, args=(room_manager,))
socket_thread.daemon = True
socket_thread.start()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", rooms=room_manager.get_rooms())

@app.route("/create-room")
def create_room():
    """
    endpoint for creating a new room
    """
    room_id = room_manager.create_room()
    return redirect(url_for("index"))
    pass


@app.route("/room-browser")
def room_browser():
    """
        Browser for the different rooms
    """
    pass

@app.route("/join-room/<int:room_id>/<username>")
def join_room(room_id: int, username: str):
    """
    page with join screen
    allows user to enter username and roomid
    """

    pass

@app.route("/room/<int:room_id>/<username>")
def room(room_id: int, username: str):
    """
    endpoint for the game
    """

    return render_template("room.html", room_id=room_id, user=username)
