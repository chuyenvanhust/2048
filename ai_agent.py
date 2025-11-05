# ai_agent.py

import random
import math
from constants import AI_DEFAULT_DEPTH, SAMPLE_CELLS, PROB_2, PROB_4, BOARD_SIZE
from game_logic import get_available_moves, get_empty_cells, is_game_over, copy_board, board_to_tuple

def count_empty(b):
    return len(get_empty_cells(b))

def get_max_tile(b):
    return max(max(row) for row in b)

def calc_smoothness(b):
    smooth = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 1):
            a, d = b[r][c], b[r][c + 1]
            if a and d:
                smooth -= abs(math.log2(a) - math.log2(d))
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE - 1):
            a, d = b[r][c], b[r + 1][c]
            if a and d:
                smooth -= abs(math.log2(a) - math.log2(d))
    return smooth

def calc_monotonicity(b):
    totals = [0, 0, 0, 0]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 1):
            a, d = b[r][c], b[r][c + 1]
            if a > d:
                totals[0] += math.log2(a + 1) - math.log2(d + 1)
            else:
                totals[1] += math.log2(d + 1) - math.log2(a + 1)
    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE - 1):
            a, d = b[r][c], b[r + 1][c]
            if a > d:
                totals[2] += math.log2(a + 1) - math.log2(d + 1)
            else:
                totals[3] += math.log2(d + 1) - math.log2(a + 1)
    return -min(totals[0], totals[1]) - min(totals[2], totals[3])

def evaluate(b):
    """Hàm đánh giá điểm cho một trạng thái bàn cờ."""
    empty = count_empty(b)
    max_tile = get_max_tile(b)
    smooth = calc_smoothness(b)
    mono = calc_monotonicity(b)
    return 3.0 * empty + 1.0 * smooth + 1.5 * mono + 0.1 * math.log2(max_tile + 1)

class AIAgent:
    def __init__(self, depth=AI_DEFAULT_DEPTH, sample_cells=SAMPLE_CELLS):
        self.depth = depth
        self.sample_cells = sample_cells
        self.cache = {}
        self.nodes = 0

    def reset(self):
        self.cache.clear()

    def best_move(self, board):
        best = None
        best_val = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        moves = get_available_moves(board)
        sorted_moves = sorted(moves, key=lambda move: evaluate(move[1]), reverse=True)

        for name, nb in sorted_moves:
            val = self._hybrid_search(nb, self.depth - 1, alpha, beta, False)
            if val > best_val:
                best_val = val
                best = name
            alpha = max(alpha, val)
        return best, best_val

    def _hybrid_search(self, board, depth, alpha, beta, is_max_turn):
        self.nodes += 1
        key = (board_to_tuple(board), depth, is_max_turn)
        if key in self.cache:
            return self.cache[key]
        if depth == 0 or is_game_over(board):
            return self.cache.setdefault(key, evaluate(board))

        if is_max_turn:
            value = float('-inf')
            moves = get_available_moves(board)
            sorted_moves = sorted(moves, key=lambda move: evaluate(move[1]), reverse=True)
            for _, nb in sorted_moves:
                value = max(value, self._hybrid_search(nb, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return self.cache.setdefault(key, value)
        else:
            empties = get_empty_cells(board)
            if not empties:
                return self.cache.setdefault(key, evaluate(board))
            
            sample = random.sample(empties, min(len(empties), self.sample_cells))
            expected = 0.0
            for r, c in sample:
                for tile, prob in [(2, PROB_2), (4, PROB_4)]:
                    nb = copy_board(board)
                    nb[r][c] = tile
                    expected += prob * self._hybrid_search(nb, depth - 1, alpha, beta, True)
            return self.cache.setdefault(key, expected / len(sample))