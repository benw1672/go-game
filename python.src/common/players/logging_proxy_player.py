from common.players.player import Player

class LoggingProxyPlayer(Player):
    def __init__(self, real_player, logging=True):
        self.real_player = real_player
        self.logging = logging
        self.stone = None


    @property
    def name(self):
        return self.real_player.name


    def __str__(self):
        return "PLAYER: {}\nSTONE: {}".format(self.name, self.stone)


    def register(self):
        if self.logging:
            print("REGISTER")
            name = self.real_player.register()
            print("REGISTERED WITH NAME: {}".format(name))
            return name
        else:
            return self.real_player.register()


    def receive_stones(self, stone):
        self.stone = stone
        if self.logging:
            print(self)
            print("RECEIVE STONE {}".format(stone))
            print()
        return self.real_player.receive_stones(stone)


    def make_a_move(self, boards):
        if self.logging:
            print(self)
            print("MAKE A MOVE")
            print(boards[0])
            move = self.real_player.make_a_move(boards)
            print("MY MOVE: {}".format(move))
            print()
            return move
        else:
            return self.real_player.make_a_move(boards)


    def end_game(self):
        if self.logging:
            print(self)
            print("END GAME")
            print()
        return self.real_player.end_game()
