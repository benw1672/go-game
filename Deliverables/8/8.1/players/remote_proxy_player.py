# Nonlocal imports.
import json, sys, os

# Local imports.
sys.path.append(os.path.abspath('..'))
import utils
from point import Point
from constants import *


class RemoteProxyPlayer():
    def __init__(self, socket):
        self.name = None
        self.stone = None
        self.socket = socket


    def register(self):
        command = ["register"]
        # Use the socket to get a move over the wire.
        self.socket.send(utils.jsonify(command).encode())
        json_response = json.loads(self.socket.recv(2048).decode())
        if not json_response:
            raise RuntimeError("Connection to client is broken.")
        self.name = json_response
        return self.name


    def receive_stones(self, stone):
        command = ["receive-stones", stone]
        self.socket.send(utils.jsonify(command).encode())
        json_response = json.loads(self.socket.recv(2048).decode())
        if not json_response == "OK":
            raise RuntimeError("Connection to client is broken.")
        return


    def make_a_move(self, boards):
        # Use the socket to get a move over the wire.
        command = ["make-a-move", boards]
        self.socket.send(utils.jsonify(command).encode())
        json_response = json.loads(self.socket.recv(2048).decode())
        if not json_response:
            raise RuntimeError("Connection to client is broken.")
        if json_response == PASS:
            return PASS
        if json_response == INVALID_HISTORY:
            return INVALID_HISTORY
        else:
            return Point.from_str(json_response)