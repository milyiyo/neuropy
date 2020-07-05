from playground.Player import Player


class Brutus(Player):
    def play(self, board):
        for i, place in enumerate(board):
            if place == 0:
                board[i] = self.symbol
                break
