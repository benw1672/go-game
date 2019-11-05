# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
import constants, player, strategies
from board import Board


def main():
    # Parse the text input into a list of JSON elements.
    txt = sys.stdin.read().rstrip()
    json_elements = txt2json(txt)

    # Instantiate dependencies.
    prioritize_capture_strategy = strategies.PrioritizeCaptureStrategy(constants.AI_MAX_SEARCH_DEPTH)
    player1 = player.Player(prioritize_capture_strategy)

    # Handle each input and collect the results.
    results = []
    for json_element in json_elements:
        if json_element[0] == "register":
            player1.name = "no name"
            results.append(player1.name)
        elif json_element[0] == "receive-stones":
            stone = json_element[1]
            player1.receive_stones(stone)
        elif json_element[0] == "make-a-move":
            json_boards = json_element[1]
            boards = [Board.from_json(json_board) for json_board in json_boards]
            results.append(player1.make_a_move(boards))
        else:
            raise ValueError("The given input is not valid.")
    
    json.dump(results, sys.stdout)
    print()


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