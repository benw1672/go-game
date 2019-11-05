import json.decoder
import sys

from board import Board
from point import Point

def main():
    '''
    test_driver.py Parses JSON from stdin, converting the JSON to a series of python objects 
    representing statements. Each of those statements is then executed, and the results are
    passed to stdout.
    '''
    input = sys.stdin.read().rstrip()
    json_elements = parse_input(input)
    results = []
    
    for board_json, statement_json in json_elements:
        board = Board(board_json)
        if statement_json[0] == "reachable?":
            point = Point.from_str(statement_json[1])
            stone = statement_json[2]
            results.append(board.is_reachable(point, stone))

    json.dump(results, sys.stdout)
    print()


def parse_input(input: str) -> list:
    json_elements = []
    decoder = json.JSONDecoder()
    position = 0

    while (position < len(input)):
        input = input[position:].lstrip()
        if input.isspace():
            break
        json_element, end_position = decoder.raw_decode(input)
        json_elements.append(json_element)
        position = end_position

    return json_elements


if __name__ == "__main__":
    main()