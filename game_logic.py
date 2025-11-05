# game_logic.py

import random
from constants import BOARD_SIZE, PROB_2

def new_board():
    """Tạo một bàn cờ mới rỗng."""
    return [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def copy_board(b):
    """Tạo một bản sao của bàn cờ."""
    return [row[:] for row in b]

def board_to_tuple(b):
    """Chuyển bàn cờ sang dạng tuple để làm key trong cache."""
    return tuple(tuple(row) for row in b)

def get_empty_cells(b):
    """Lấy danh sách các ô trống trên bàn cờ."""
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if b[r][c] == 0]

def add_random_tile(b):
    """Thêm một ô ngẫu nhiên (2 hoặc 4) vào một vị trí trống."""
    empties = get_empty_cells(b)
    if not empties:
        return False
    r, c = random.choice(empties)
    b[r][c] = 2 if random.random() < PROB_2 else 4
    return True

def compress_line(line):
    """Trượt và hợp nhất một hàng/cột về bên trái."""
    new = [v for v in line if v != 0]
    score = 0
    moved = False
    out = []
    i = 0
    while i < len(new):
        if i + 1 < len(new) and new[i] == new[i+1]:
            out.append(new[i] * 2)
            score += new[i] * 2
            i += 2
            moved = True
        else:
            out.append(new[i])
            i += 1
    out += [0] * (BOARD_SIZE - len(out))
    if out != line:
        moved = True
    return out, score, moved

def move_left(b):
    new = copy_board(b)
    score = 0
    moved_any = False
    for r in range(BOARD_SIZE):
        line, s, moved = compress_line(new[r])
        new[r] = line
        score += s
        moved_any |= moved
    return new, score, moved_any

def move_right(b):
    rev = [list(reversed(row)) for row in b]
    out, score, moved = move_left(rev)
    out = [list(reversed(row)) for row in out]
    return out, score, moved

def transpose(b):
    return [list(row) for row in zip(*b)]

def move_up(b):
    t = transpose(b)
    out, score, moved = move_left(t)
    out = transpose(out)
    return out, score, moved

def move_down(b):
    t = transpose(b)
    out, score, moved = move_right(t)
    out = transpose(out)
    return out, score, moved

def get_available_moves(b):
    """Lấy danh sách các nước đi hợp lệ từ trạng thái bàn cờ hiện tại."""
    moves = []
    for name, fn in [('Up', move_up), ('Down', move_down), ('Left', move_left), ('Right', move_right)]:
        nb, sc, moved = fn(b)
        if moved:
            moves.append((name, nb))
    return moves

def is_game_over(b):
    """Kiểm tra xem trò chơi đã kết thúc chưa."""
    if get_empty_cells(b):
        return False
    for fn in [move_left, move_right, move_up, move_down]:
        _, _, moved = fn(b)
        if moved:
            return False
    return True