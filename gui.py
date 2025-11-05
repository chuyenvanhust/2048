# gui.py

import pygame
import time
from constants import *
from game_logic import *
from ai_agent import AIAgent

class GameGUI:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('2048 - Modularized')
        self.clock = pygame.time.Clock()
        self.restart()

    def restart(self):
        self.board = new_board()
        add_random_tile(self.board)
        add_random_tile(self.board)
        self.score = 0
        self.ai_on = False
        self.ai_agent = AIAgent()
        self.last_ai_think = None

    def step_move(self, direction):
        move_map = {'Left': move_left, 'Right': move_right, 'Up': move_up, 'Down': move_down}
        if direction in move_map:
            nb, sc, moved = move_map[direction](self.board)
            if moved:
                self.board = nb
                self.score += sc
                add_random_tile(self.board)
            return moved
        return False

    def update_ai(self):
        if not self.ai_on or is_game_over(self.board):
            return
        
        self.ai_agent.nodes = 0
        self.ai_agent.reset()
        t0 = time.time()
        name, val = self.ai_agent.best_move(self.board)
        t1 = time.time()
        self.last_ai_think = (t1 - t0, self.ai_agent.nodes, val)
        if name:
            self.step_move(name)

    def draw_board(self):
        self.screen.fill(COL_BG)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.board[r][c]
                rect = pygame.Rect(MARGIN + c * (TILE_SIZE + 10), MARGIN + r * (TILE_SIZE + 10), TILE_SIZE, TILE_SIZE)
                col = TILE_COLORS.get(val, (60, 58, 50))
                pygame.draw.rect(self.screen, col, rect, border_radius=8)
                if val != 0:
                    text_col = COL_TEXT_DARK if val <= 4 else COL_TEXT_LIGHT
                    text = self.big_font.render(str(val), True, text_col)
                    tw, th = text.get_size()
                    self.screen.blit(text, (rect.centerx - tw // 2, rect.centery - th // 2))

    def draw_hud(self):
        hud_y = BOARD_SIZE * (TILE_SIZE + 10) + MARGIN
        info = f'Score: {self.score}   Mode: {"AI" if self.ai_on else "Manual"}   Depth: {self.ai_agent.depth}'
        self.screen.blit(self.font.render(info, True, COL_TEXT_DARK), (MARGIN, hud_y))
        hint = 'Space: toggle AI   R: restart   +/-: depth'
        self.screen.blit(self.font.render(hint, True, COL_TEXT_DARK), (MARGIN, hud_y + 30))
        if self.last_ai_think:
            t, nodes, val = self.last_ai_think
            stat = f'AI think: {t:.2f}s nodes={nodes} val={val:.2f}'
            self.screen.blit(self.font.render(stat, True, COL_TEXT_DARK), (MARGIN, hud_y + 60))
        if is_game_over(self.board):
            over_surf = self.big_font.render('GAME OVER', True, (200, 30, 30))
            self.screen.blit(over_surf, (WINDOW_SIZE // 2 - over_surf.get_width() // 2, WINDOW_SIZE // 2 - over_surf.get_height() // 2))

    def run(self):
        running = True
        ai_tick_counter = 0
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ai_on = not self.ai_on
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                        self.ai_agent.depth = min(8, self.ai_agent.depth + 1)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.ai_agent.depth = max(1, self.ai_agent.depth - 1)
                    elif not self.ai_on:
                        key_map = {
                            pygame.K_LEFT: 'Left', pygame.K_RIGHT: 'Right',
                            pygame.K_UP: 'Up', pygame.K_DOWN: 'Down'
                        }
                        if event.key in key_map:
                            self.step_move(key_map[event.key])

            if self.ai_on and not is_game_over(self.board):
                if ai_tick_counter % 10 == 0:
                    self.update_ai()
            
            self.draw_board()
            self.draw_hud()
            pygame.display.flip()
            ai_tick_counter += 1

        pygame.quit()