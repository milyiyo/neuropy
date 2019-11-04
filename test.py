import neuroevolution as ne
import random


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def play(self, board):
        pass


class Brutus(Player):
    def play(self, board):
        for i, place in enumerate(board):
            if place == 0:
                board[i] = self.symbol
                break


class AI(Player):
    def __init__(self, symbol, network):
        self.symbol = symbol
        self.network = network

    def play(self, board):
        out = network.compute(board)
        playable_idxs = [i for i, x in enumerate(board) if x == 0]
        max = out[playable_idxs[0]]
        max_idx = playable_idxs[0]
        for idx in playable_idxs:
            if out[idx] > max:
                max = out[idx]
                max_idx = idx
        board[max_idx] = self.symbol
        i = 0


# nn = neuroevol.nextGeneration()
# [print(n.compute([2,2])) for n in nn]
# [neuroevol.networkScore(n, random.random()) for n in nn]
# neuroevol.nextGeneration()

# [print(n.compute([2,2])) for n in nn]
# [neuroevol.networkScore(n, random.random()) for n in nn]
# neuroevol.nextGeneration()

# [print(n.compute([2,2])) for n in nn]
# [neuroevol.networkScore(n, random.random()) for n in nn]
# neuroevol.nextGeneration()


def player_ai(symbol):
    def play(board):
        for i, place in enumerate(board):
            if place == 0:
                board[i] = symbol
                break
    return play


def print_board(board):
    nb = [' ' if x == 0 else 'x' if x == 1 else 'o' for x in board]
    print('', *nb[0:3], '\n', *nb[3:6], '\n', *nb[6:9], '', sep=' | ')
    print()


def can_play(board):
    def equal_cells(c1, c2, c3):
        return board[c1] == board[c2] == board[c3] and board[c1] != 0

    if equal_cells(0, 1, 2):
        return (board[0], False)
    if equal_cells(3, 4, 5):
        return (board[3], False)
    if equal_cells(6, 7, 8):
        return (board[6], False)

    if equal_cells(0, 3, 6):
        return (board[0], False)
    if equal_cells(1, 4, 7):
        return (board[1], False)
    if equal_cells(2, 5, 8):
        return (board[2], False)

    if equal_cells(0, 4, 8):
        return (board[0], False)
    if equal_cells(2, 4, 6):
        return (board[2], False)

    res = any([True for x in board if x == 0])
    return (None, res)


neuroevol = ne.Neuroevolution({
    'network': [9, [2], 9],
})

for network in neuroevol.nextGeneration():
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    players = [Brutus(1), AI(-1, network)]
    plays_idx = 0
    win_player, allow_play = can_play(board)

    while(allow_play):
        # print_board(board)
        players[plays_idx].play(board)
        plays_idx = (plays_idx + 1) % 2
        win_player, allow_play = can_play(board)

    print_board(board)
    print('Winner: ', 'x' if win_player == 1 
        else 'o' if win_player == -1 
        else 'No one')

    print('---------------------')
