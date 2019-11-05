# Import nonlocal dependencies.
import typing
from queue import Queue

# Import local dependencies.
from constants import *
from point import Point
from chain import Chain


class Board(object):
# Initialization
    def __init__(self, grid=[[EMPTY]*BOARD_COL_LENGTH for _ in range(BOARD_ROW_LENGTH)]):
        self._grid = grid


# Special methods
    def __iter__(self):
        for j in range(BOARD_COL_LENGTH):
            for i in range(BOARD_ROW_LENGTH):
                point = Point(i, j)
                yield point, self[point]


    def __getitem__(self, point):
        # Allows an item to be retrieved using the syntax: `a = board[point]`
        return self._grid[point.x][point.y]


    def __setitem__(self, point, maybe_stone):
        # Allows an assignment using the syntax: `board[point] = maybe_stone`
        self._grid[point.x][point.y] = maybe_stone


    def __eq__(self, other):
        # Allows comparison by value of two boards using the `==` operator: `board1 == board2`
        if other == None:
            return False
        for i in range(len(self._grid)):
            for j in range(len(self._grid[0])):
                if self._grid[i][j] != other._grid[i][j]:
                    return False
        return True


# Normal public methods
    def to_json(self) -> list:
        return self._grid


    def is_occupied(self, point):
        maybe_stone = self[point]
        return maybe_stone in STONES


    def occupies(self, stone, point):
        return stone == self[point]


    def place(self, stone, point):
        if self.is_occupied(point):
            return "This seat is taken!"
        else:
            self[point] = stone
            return self.to_json()


    def remove(self, stone_to_be_removed, point):
        if self.occupies(stone_to_be_removed, point):
            self[point] = EMPTY
            return self.to_json()
        else:
            return "I am just a board! I cannot remove what is not there!"


    def get_points(self, target_maybe_stone):
        result = []
        for point, maybe_stone in iter(self):
            if maybe_stone == target_maybe_stone:
                result.append(str(point))
        return sorted(result)


    def is_fully_empty(self):
        for _, maybe_stone in iter(self):
            if maybe_stone in STONES:
                return False
        return True


    def is_reachable(self, starting_point, target_maybe_stone):
        starting_maybe_stone = self[starting_point]
        stack = [starting_point]
        visited = set()
        while stack:
            curr_point = stack.pop()
            visited.add(curr_point)
            if self[curr_point] == target_maybe_stone:
                return True
            elif self[curr_point] == starting_maybe_stone:
                for valid_neighbor in curr_point.get_valid_neighbors():
                    if valid_neighbor not in visited:
                        stack.append(valid_neighbor)
        return False


    def get_chain(self, starting_point):
        starting_stone = self[starting_point]
        liberties, connected_points, visited = set(), set(), set([starting_point])
        q = Queue()
        q.put(starting_point)
        while not q.empty():
            curr_point = q.get()
            curr_stone = self[curr_point]
            if curr_stone == starting_stone:
                connected_points.add(curr_point)
                for neighbor in curr_point.get_valid_neighbors():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.put(neighbor)
            else:
                if curr_stone == EMPTY:
                    liberties.add(curr_point)
        return Chain(starting_stone, connected_points, liberties)


    def get_all_chains(self) -> list:
        chains = []
        visited = set()
        for point, maybe_stone in iter(self):
            if maybe_stone in STONES and point not in visited:
                chain = self.get_chain(point)
                visited |= chain.connected_points
                chains.append(chain)

        return chains
