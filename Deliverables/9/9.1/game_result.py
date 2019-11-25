class GameResult(object):
    def __init__(self, winner, loser, game_was_draw: bool, loser_was_cheating: bool):
        self.winner = winner
        self.loser = loser
        self.game_was_draw = game_was_draw
        self.loser_was_cheating = loser_was_cheating