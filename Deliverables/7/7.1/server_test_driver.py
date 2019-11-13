# Import nonlocal dependencies.
import json, jsonpickle, sys, typing, socket, os
from functools import partial

# Import local dependencies.
import constants, utils
from player import RemoteProxyPlayer, StateProxyPlayer, command_player


def main():
    # Tokenize the text input into a list of JSON elements.
    input_iter = stream_to_json_gen(sys.stdin)

    # Create a referee and use inputs to play a game.
    script_dir = os.path.dirname(__file__)
    # Start up server, listening on the port specified in the config file.
    with open(os.path.join(script_dir, 'go.config')) as f:
        network_config = json.load(f)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((network_config["IP"], network_config["port"]))
    # Accept only one connection for now.
    serversocket.listen(1)
    conn, address = serversocket.accept()

    # Instantiate player and action container.
    remote_proxy_player = StateProxyPlayer(RemoteProxyPlayer(conn))

    results = []
    for json_element in input_iter:
        result = command_player(remote_proxy_player, json_element)
        if result:
            results.append(result)
        if result == constants.GO_HAS_GONE_CRAZY:
            break
    
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    serversocket.close()
    print(utils.jsonify(results))


def stream_to_json_gen(stream):
    decoder = json.JSONDecoder()
    buffer = ''
    buffersize=10
    for chunk in iter(partial(stream.read, buffersize), ''):
         buffer += chunk
         while buffer:
             try:
                 result, index = decoder.raw_decode(buffer.lstrip())
                 yield result
                 buffer = buffer.lstrip()[index:]
             except ValueError:
                 # Not enough data to decode, read more
                 break


if __name__ == "__main__":
    main()