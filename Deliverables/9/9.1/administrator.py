# Import nonlocal dependencies.
import json, jsonpickle, sys, typing, socket, os
from functools import partial
from importlib import util

# Import local dependencies.
import constants, utils
from players.remote_proxy_player import RemoteProxyPlayer
from players.state_proxy_player import StateProxyPlayer
from players.strategies import PrioritizeCaptureStrategy
import referee


def main():
    # Get config.
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'go.config')) as fd:
        config = json.load(fd)

    # Instantiate a default player. Credits to team 44 for explaining how to do this.
    spec = util.spec_from_file_location('players.default_player', config["default-player"])
    default_player_mod = util.module_from_spec(spec)
    spec.loader.exec_module(default_player_mod)
    default_player = default_player_mod.make_player()

    # Start up server, listening on the port specified in the config file.
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((config["IP"], config["port"]))

    # Accept only one connection for now.
    serversocket.listen(1)
    clientsocket, _ = serversocket.accept()

    # Instantiate representative of the remote player.
    remote_player = StateProxyPlayer(RemoteProxyPlayer(clientsocket))
    
    # Play a game and send the result to stdout.
    results = referee.play_a_game(remote_player, default_player)
    print(utils.jsonify(results))

    # Graceful shutdown.
    try:
        clientsocket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    clientsocket.close()
    serversocket.close()


if __name__ == "__main__":
    main()