class Chain(object):
    def __init__(self, stone_color: str,
                connected_points: set, liberties: set):
        self.stone_color = stone_color
        self.connected_points = connected_points
        self.liberties = liberties