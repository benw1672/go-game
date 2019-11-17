class ActionContainer():
    def __init__(self):
        self.next_action = Register()

    def next(self, action):
        self.next_action = action

    def act(self, player, *args):
        self.next_action.act(player, *args)

class Register():
    def act(self, container, player, name):
        player.name = name
        container.next_action = ReceiveStones()
        return name

class ReceiveStones():
    def act(self, container, player, stone):
        player.stone = stone
        container.next_action = MakeAMove()

class MakeAMove():
    def act(self, container, player, board_history):
        move = player.make_a_move(board_history)
        container.next_action = MakeAMove()
        return move
