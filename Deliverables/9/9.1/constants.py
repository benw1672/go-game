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

# Config file.
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, 'go.config')) as fd:
    config = json.load(fd)
IP = config["IP"]
PORT = config["port"]

# Load default player.
spec = util.spec_from_file_location('players.default_player', config["default-player"])
DEFAULT_PLAYER_MODULE = util.module_from_spec(spec)