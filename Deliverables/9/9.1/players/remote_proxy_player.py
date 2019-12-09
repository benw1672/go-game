# Nonlocal imports.
import json, sys, os, time

# Local imports.
sys.path.append(os.path.abspath('..'))
import utils
from point import Point
from constants import *
from .order_proxy_player import OrderProxyPlayer
from .history_check_proxy_player import HistoryCheckProxyPlayer

def make_player(connection):
    return OrderProxyPlayer(RemoteProxyPlayer(connection))

CONNECTION_ERRORS = (ConnectionResetError, OSError, json.decoder.JSONDecodeError)

class RemoteProxyPlayer(object):
    def __init__(self, socket):
        self.name = None
        self.stone = None
        self.socket = socket


    def register(self):
        command = ["register"]
        try:
            self.socket.send(utils.jsonify(command).encode())
            json_response = json.loads(self.socket.recv(2048).decode())
        except CONNECTION_ERRORS:
            raise RuntimeError("Connected dropped by the player")
        if not json_response or not isinstance(json_response, str):
            raise RuntimeError("register: Connection to client is broken.")
        self.name = json_response
        return self.name


    def receive_stones(self, stone):
        command = ["receive-stones", stone]
        try:
            self.socket.send(utils.jsonify(command).encode())
        except CONNECTION_ERRORS:
            raise RuntimeError("receive-stones: Connection to client is broken.")
        return


    def make_a_move(self, boards):
        # Use the socket to get a move over the wire.
        command = ["make-a-move", boards]
        try:
            self.socket.send(utils.jsonify(command).encode())
            json_response = json.loads(self.socket.recv(2048).decode())
        except CONNECTION_ERRORS:
            raise RuntimeError("Connected dropped by the player")
        if not json_response:
            raise RuntimeError("make_a_move: Connection to client is broken.")
        if json_response == PASS:
            return PASS
        if json_response == INVALID_HISTORY:
            return INVALID_HISTORY
        else:
            try:
                point = Point.from_str(json_response)
                return point
            except ValueError:
                raise RuntimeError("make_a_move: Client provided invalid input")


    def end_game(self):
        command = ["end-game"]
        try:
            self.socket.send(utils.jsonify(command).encode())
            json_response = json.loads(self.socket.recv(2048).decode())
        except CONNECTION_ERRORS:
            return "OK"
        if not json_response == "OK":
            raise RuntimeError("Connection to client is broken.")
        return "OK"