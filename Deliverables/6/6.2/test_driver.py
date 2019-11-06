# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
import player, strategies
from board import Board
from constants import *


def main():
    # Parse the text input into a list of JSON elements.
    txt = sys.stdin.read().rstrip()
    json_elements = txt2json(txt)

    # Instantiate dependencies.
    player1 = player.Player(strategy=strategies.SimpleStrategy())

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
            boards = [Board(json_board) for json_board in json_boards]
            move = player1.make_a_move(boards)
            if move == PASS:
                move_str = PASS
            else:
                move_str = str(move[0])
            results.append(move_str)
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