class GameResult(object):
    def __init__(self, winner, loser, loser_was_cheating: bool):
        self.winner = winner
        self.loser = loser
        self.loser_was_cheating = loser_was_cheating