from playground.Player import Player


class AI(Player):
    def __init__(self, symbol, network):
        super().__init__(symbol)
        self.symbol = symbol
        self.network = network

    def play(self, board):
        # print('\tPlays AI')
        out = self.network.compute(board)
        playable_idxs = [i for i, x in enumerate(board) if x == 0]
        max = out[playable_idxs[0]]
        max_idx = playable_idxs[0]
        for idx in playable_idxs:
            if out[idx] > max:
                max = out[idx]
                max_idx = idx
        board[max_idx] = self.symbol
