# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
from player import handle_player, PlayerStateProxy, PlayerContractProxy, Player
import strategies
from board import Board
from constants import *


def main():
    # Parse the text input into a list of JSON elements.
    txt = sys.stdin.read().rstrip()
    json_elements = txt2json(txt)

    # Instantiate dependencies.
    player = Player(strategy=strategies.PrioritizeCaptureStrategy())
    player_with_contract_state = PlayerStateProxy(PlayerContractProxy(player))

    # Handle each input and collect the results.
    results = []
    for json_element in json_elements:
        res = handle_player(player_with_contract_state, json_element)
        if res:
            results.append(res)
        if res == GO_HAS_GONE_CRAZY:
            break
    json.dump(results, sys.stdout)


def txt2json(content: str) -> list:
    decoder = json.JSONDecoder()
    json_elements = []
    while content != '':
        content = content.strip()
        element, idx = decoder.raw_decode(content)
        json_elements.append(element)
        content = content[idx:]

    return json_elements


if __name__ == "__main__":
    main()
