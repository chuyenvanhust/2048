# constants.py

# Kích thước và giao diện
WINDOW_SIZE = 520
BOARD_SIZE = 4
TILE_SIZE = 100
MARGIN = 20
FPS = 30

# Cấu hình AI
AI_DEFAULT_DEPTH = 3
SAMPLE_CELLS = 6 
PROB_2 = 0.9
PROB_4 = 0.1

# Màu sắc
COL_BG = (187, 173, 160)
COL_EMPTY = (205, 193, 180)
COL_TEXT_LIGHT = (249, 246, 242)
COL_TEXT_DARK = (119, 110, 101)
TILE_COLORS = {
    0: COL_EMPTY,
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}