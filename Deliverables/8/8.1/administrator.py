# Import nonlocal dependencies.
import json, jsonpickle, sys, typing, socket, os
from functools import partial

# Import local dependencies.
import constants, utils
from players.remote_proxy_player import RemoteProxyPlayer
from players.state_proxy_player import StateProxyPlayer
import referee


def main():
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'go.config')) as fd:
        config = json.load(fd)

    # Instantiate a default player.
    # default_player_impl_abs_path = os.path.join(script_dir, config["default-player"])
    # print(default_player_impl_abs_path)
    default_player_mod = __import__("players.default_player")
    default_player = default_player_mod.Player()

    # Start up server, listening on the port specified in the config file.
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((config["IP"], config["port"]))

    # Accept only one connection for now.
    serversocket.listen(1)
    clientsocket, address = serversocket.accept()

    # Instantiate representative of the remote player.
    remote_player = StateProxyPlayer(RemoteProxyPlayer(clientsocket))
    
    results = referee.play_a_game(remote_player, default_player)
    print(utils.jsonify(results))

    clientsocket.shutdown(socket.SHUT_RDWR)
    clientsocket.close()
    serversocket.close()


if __name__ == "__main__":
    main()