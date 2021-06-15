'''
This module defines any package-global constants.
'''
import os, json
from importlib import util

# Board dimensions.
BOARD_COL_LENGTH = 9
BOARD_ROW_LENGTH = 9

# Stones and MaybeStones.
BLACK = "B"
WHITE = "W"
EMPTY = " "
STONES = [BLACK, WHITE]
MAYBE_STONES = [BLACK, WHITE, EMPTY]

# Types of turns.
PASS = "pass"
TURN_TYPES = [PASS] + STONES

# Special messages.
INVALID_HISTORY = "This history makes no sense!"
GO_HAS_GONE_CRAZY = "GO has gone crazy!"

# Player AI.
AI_MAX_SEARCH_DEPTH = 1

# Tournament modes.
LEAGUE = 500
CUP = 600

# Tournament
WIN = 1
LOSE = 0