# Import nonlocal dependencies.
import json, os, sys, typing

# Import local dependencies.
import player, strategies, referee
from point import Point
from board import Board
from constants import *
from referee import Referee


def main():
    # Parse the text input into a list of JSON elements.
    txt = sys.stdin.read().rstrip()
    json_elements = txt2json(txt)

    rf = Referee()
    results = []
    for i, json_element in enumerate(json_elements):
        # If the move is a pass
        if i < 2:
            results.append(rf.register_player(json_element))
            continue
        elif i == 2:
            results.append(rf.board_history[0].to_json())
        if rf.is_game_ended:
            break
        else:
            if json_element == PASS:
                play_or_pass = PASS
            else:
                play_or_pass = Point.from_str(json_element)
            res = rf.play_point(play_or_pass)
            if isinstance(res, Board):
                results.append(res.to_json())
            else:
                results.append(res)

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
