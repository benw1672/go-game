# Import nonlocal dependencies.
import json, jsonpickle, os, sys, typing, socket, time

# Import local dependencies.
from players.state_proxy_player import StateProxyPlayer
from players.ai_player import AIPlayer
from players.strategies import PrioritizeCaptureStrategy, SimpleStrategy
from players.random_any_player import RandomAnyPlayer
from players.human_player import HumanPlayer
from board import Board
from constants import *
import utils


def main():
    script_dir = os.path.dirname(__file__)
    # Set up the player.
    player = StateProxyPlayer(HumanPlayer())

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

    # Get commands from server and relay to player.
    while True:
        data = clientsocket.recv(8192).decode()
        if not data:
            break
        json_input = json.loads(data)
        result = command_player(player, json_input)
        if result:
            clientsocket.send(utils.jsonify(result).encode())

    clientsocket.close()


def command_player(player, json_element):
    try:
        command_name, *args = utils.jsoncommand2internal(json_element)
    except ValueError:
        return GO_HAS_GONE_CRAZY
    if command_name == "register":
        return player.register()
    elif command_name == "receive-stones":
        return player.receive_stones(*args)
    elif command_name == "make-a-move":
        return player.make_a_move(*args)
    elif command_name == "end-game":
        return player.end_game(*args)


if __name__ == "__main__":
    main()