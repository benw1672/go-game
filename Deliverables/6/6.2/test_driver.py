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
    res_print = []
    for i, json_element in enumerate(json_elements):
        # If the move is a pass
        if i == 0:
            results.append(rf.register_black_player(json_element))
            #print(rf.register_black_player(json_element))
            continue
        elif i == 1:
            results.append(rf.register_white_player(json_element))
            #print(rf.register_white_player(json_element))
            continue
        elif i == 2:
            res = rf.board_history
            results.append(list(map(lambda board: board.to_json(), res)))
            #map(lambda board: board.pretty_print(), res)
            #print("[")
            #for b in res:
            #    b.pretty_print()
            #print("]")
        if rf.is_game_ended:
            break
        else:
            if json_element == PASS:
                play_or_pass = PASS
            else:
                play_or_pass = Point.from_str(json_element)
            res = rf.play_point(play_or_pass)
            if isinstance(res[0], Board):
                results.append(list(map(lambda board: board.to_json(), res)))
                #print("[")
                #for b in res:
                #    b.pretty_print()
                #print("]")
                #map(lambda board: board.pretty_print(), res)
            else:
                results.append(res)
                #print(res)

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
