'''
This module defines any package-global constants.
'''
# Board dimensions.
BOARD_COL_LENGTH = 19
BOARD_ROW_LENGTH = 19

# Stones and MaybeStones.
BLACK = "B"
WHITE = "W"
EMPTY = " "
STONES = [BLACK, WHITE]
MAYBE_STONES = [BLACK, WHITE, EMPTY]

# Types of turns.
PASS = "pass"
TURN_TYPES = [PASS] + STONES

# Player AI.
AI_MAX_SEARCH_DEPTH = 1

# Types of end
PROPER_END = True
ILLEGAL_END = False
