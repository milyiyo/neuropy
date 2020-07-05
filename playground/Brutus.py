from playground.Player import Player


class Brutus(Player):
    def play(self, board):
        # print('\tPlays Brutus')
        for i, place in enumerate(board):
            if place == 0:
                board[i] = self.symbol
                break
