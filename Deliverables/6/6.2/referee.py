from constants import *
from player import Player
from board import Board
import rule_checker as rc

class Referee():
    def __init__(self):
        self.is_black_registered = False
        self.is_white_registered = False
        self.time_to_determine_winner = False
        self.end_type = ""
        self.is_game_ended = False


        self.current_turn = BLACK
        self.black_player = Player()
        self.white_player = Player()
        self.board_history = [Board()]
        self.prev_move = ""

    def register_black_player(self, player_name):
        self.black_player.set_name(player_name)
        self.black_player.receive_stones(BLACK)
        self.is_black_registered = True
        return BLACK
    def register_white_player(self, player_name):
        self.white_player.name = player_name
        self.white_player.set_name(player_name)
        self.white_player.receive_stones(WHITE)
        self.is_white_registered = True
        return WHITE
    def register_player(self, player_name):
        if not self.is_black_registered:
            self.black_player.set_name(player_name)
            self.black_player.receive_stones(BLACK)
            self.is_black_registered = True
            return BLACK
        elif not self.is_white_registered:
            self.white_player.name = player_name
            self.white_player.set_name(player_name)
            self.white_player.receive_stones(WHITE)
            self.is_white_registered = True
            return WHITE

    def determine_winner(self, is_proper_end):
        # properly ended (two passes have been made)
        if is_proper_end:
            scores = rc.get_scores(self.board_history[0])
            if scores[BLACK] > scores[WHITE]:
                return [self.black_player.name]
            elif scores[WHITE] > scores[BLACK]:
                return [self.white_player.name]
            else:
                return sorted([self.black_player.name, self.white_player.name])
        # illegal move has been made
        else:
            if self.current_turn == BLACK:
                return [self.white_player.name]
            else:
                return [self.black_player.name]


    def update_board_history(self, new_board):
        if len(self.board_history) < 3:
            self.board_history.insert(0, new_board)
        else:
            self.board_history.pop()
            self.board_history.insert(0, new_board)


    def update_turn(self):
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE


    def update_prev_move(self, point_or_pass):
        self.prev_move = point_or_pass


    def play_point(self, point_or_pass):
        # both players need to be registered before playing point
        if not (self.is_black_registered and self.is_white_registered):
            return
        if point_or_pass == PASS:
            if self.prev_move == PASS:
                # proper end to the game
                self.is_game_ended = True
                return self.determine_winner(PROPER_END)
            else:
                self.update_board_history(self.board_history[0])
                self.update_turn()
                self.update_prev_move(point_or_pass)
                #return self.board_history[1]
                return self.board_history

        point = point_or_pass
        if rc.is_move_legal(self.current_turn,
                            (point, self.board_history)):
            curr_board = self.board_history[0]
            new_board = rc._get_board_if_valid_play(curr_board, self.current_turn, point)
            self.update_board_history(new_board)
            self.update_turn()
            self.update_prev_move(point_or_pass)
            #return curr_board
            return self.board_history
        else:
            #ILLEGAL_END
            self.is_game_ended = True
            return self.determine_winner(ILLEGAL_END)
