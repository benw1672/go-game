# Import nonlocal dependencies.
import operator

# Import local dependencies.
from constants import *
from functools import total_ordering


def is_row_index_in_bounds(x: int):
    return 0 <= x < BOARD_ROW_LENGTH


def is_col_index_in_bounds(y: int):
    return 0 <= y < BOARD_COL_LENGTH


@total_ordering
class Point(tuple):
    def __new__(cls, x, y):
        if not is_row_index_in_bounds(x):
            raise ValueError("Point.x must be within the bounds of the board.")
        if not is_col_index_in_bounds(y):
            raise ValueError("Point.y must be within the bounds of the board.")
        return tuple.__new__(Point, (x, y))
    
    
    @property
    def x(self):
        return operator.itemgetter(0)(self)


    @property
    def y(self):
        return operator.itemgetter(1)(self)


    # Points in this version of Go are ordered ascending by 
    # column index, then row index.
    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        else:
            return self.x < other.x


    @classmethod
    def from_str(cls, str_point):
        # In the Japanese Go notation, the column number is listed before row number.
        y_one_indexed, x_one_indexed = str_point.split('-')
        return cls(int(x_one_indexed)-1, int(y_one_indexed)-1)


    def __str__(self):
        # In the Japanese Go notation, the column number is listed before row number,
        # and the point is 1-indexed rather than 0-indexed.
        return "%s-%s" % (self.y+1, self.x+1)


    def get_valid_neighbors(self):
        def is_in_bounds(pair):
            row_idx, col_idx = pair
            return is_row_index_in_bounds(row_idx) and is_col_index_in_bounds(col_idx)

        neighbors = [(self.x - 1, self.y),
                    (self.x, self.y - 1),
                    (self.x + 1, self.y),
                    (self.x, self.y + 1)]
        return [Point(*p) for p in neighbors if is_in_bounds(p)]