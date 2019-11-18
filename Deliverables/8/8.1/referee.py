from constants import *
from game_state import GameStateContainer, BlackIllegalMove, WhiteIllegalMove, LegalEnd


def play_a_game(self, black_player, white_player):
    game_state_container = GameStateContainer(black_player, white_player)
    end_states = (BlackIllegalMove, WhiteIllegalMove, LegalEnd)
    while True:
        game_state_container.act()
        if isinstance(game_state_container.next_action, end_states):
            game_state_container.act()
            break

    return game_state_container.get_results()[-1]