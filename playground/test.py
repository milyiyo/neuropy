import random, math

import Neuroevolution as ne
from playground.AI import AI
from playground.Brutus import Brutus

def sample():
    nn = neuroevol.nextGeneration()
    [print(n.compute([2,2])) for n in nn]
    [neuroevol.networkScore(n, random.random()) for n in nn]
    neuroevol.nextGeneration()

    [print(n.compute([2,2])) for n in nn]
    [neuroevol.networkScore(n, random.random()) for n in nn]
    neuroevol.nextGeneration()

    [print(n.compute([2,2])) for n in nn]
    [neuroevol.networkScore(n, random.random()) for n in nn]
    neuroevol.nextGeneration()


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
    """
    Indicates if there is a winner already and if the players can continue playing
    :param board: Current board
    :return: (<winner>, <canContinuePlaying>)
    """
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
    'network': [9, [5], 9],
})

ITERATIONS = 1000+1
GAMES = 3
EMPTY_BOARD = [0, 0, 0, 0, 0, 0, 0, 0, 0]
SYMBOL_BRUTUS = 1
SYMBOL_AI = -1


def play_game():
    board = EMPTY_BOARD[:]
    players = [Brutus(SYMBOL_BRUTUS), AI(SYMBOL_AI, network)]
    plays_idx = 0
    win_player, allow_play = can_play(board)

    while (allow_play):
        players[plays_idx].play(board)
        plays_idx = (plays_idx + 1) % 2
        win_player, allow_play = can_play(board)
    return win_player


for i in range(ITERATIONS):
    nn = neuroevol.next_generation()

    count_win_brutus = 0
    count_win_ai = 0
    count_win_no_one = 0
    count_best_score = 0

    for network in nn:
        score = 0
        for games in range(GAMES):
            win_player = play_game()

            # print_board(board)

            if win_player == SYMBOL_AI:
                score += 1
                count_win_ai += 1
            elif win_player == SYMBOL_BRUTUS:
                score -= 1
                count_win_brutus += 1
            else:
                count_win_no_one += 1

            # print('---------------------')
        final_score = score / sum([count_win_brutus, count_win_ai, count_win_no_one])
        neuroevol.network_score(network, final_score)

        if final_score < count_best_score:
            count_best_score = final_score
        # count_best_score = max(count_best_score, final_score)

    if i % 10 == 0:
        # print('\niteration #', i)
        # print('AI:     ', count_win_ai)
        # print('Brutus: ', count_win_brutus)
        # print('None:   ', count_win_no_one)
        # print('% AI:   ', count_win_ai * 100 / sum([count_win_ai, count_win_brutus, count_win_no_one]))
        base_100 = math.floor(count_win_ai * 100 / sum([count_win_ai, count_win_brutus, count_win_no_one]))
        inv = 100 - base_100
        print(''.join(['*' for i in range(base_100)]) + ''.join(' ' for i in range(inv)) + '|', base_100)

        # print('Score:  ', round(abs(count_best_score) * 100), '%')
