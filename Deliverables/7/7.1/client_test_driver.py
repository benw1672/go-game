# Import nonlocal dependencies.
import json, os, sys, typing, socket
import jsonpickle, time

# Import local dependencies.
from player import StateProxyPlayer, AIPlayer, command_player
from strategies import PrioritizeCaptureStrategy
from board import Board
from constants import *
import utils


def main():
    script_dir = os.path.dirname(__file__)
    # Setup the player.
    with open(os.path.join(script_dir, 'go-player.config')) as f:
        player_config = json.load(f)
    player = StateProxyPlayer(AIPlayer(PrioritizeCaptureStrategy(max_search_depth=player_config["depth"])))

    # Connect to server.
    with open(os.path.join(script_dir, 'go.config')) as f:
        network_config = json.load(f)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            time.sleep(1)
            clientsocket.connect((network_config["IP"], network_config["port"]))
            break
        except OSError:
            continue

    while True:
        # Get commands from server and relay to player.
        data = clientsocket.recv(8192).decode()
        if not data:
            break
        json_input = json.loads(data)
        result = command_player(player, json_input)
        if result:
            clientsocket.send(utils.jsonify(result).encode())

    clientsocket.close()


if __name__ == "__main__":
    main()