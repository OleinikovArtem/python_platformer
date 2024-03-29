import pygame
import sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from debug import debug
from settings import *
from menu import Menu


class Editor:
    def __init__(self):
        # main setup
        self.display_surface = pygame.display.get_surface()

        # navigation
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # support lines
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        # selection
        self.selection_index = 2

        # menu
        self.menu = Menu()

    # input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)

    def pan_input(self, event):
        # middle mouse button pressed / released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False

        # mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 25
            else:
                self.origin.x -= event.y * 25

        # panning update
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selection_index += 1
            if event.key == pygame.K_LEFT:
                self.selection_index -= 1

            self.selection_index = max(2, min(self.selection_index, 18))

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            self.selection_index = self.menu.click(mouse_pos(), mouse_buttons())

    # drawing
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        origin_offset = vector(
            x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE,
        )

        self.support_line_surf.fill('green')

        for col in range(cols + 2):
            x = origin_offset.x + TILE_SIZE * col
            pygame.draw.line(self.support_line_surf, LINE_COLOR, start_pos=(x, 0), end_pos=(x, WINDOW_HEIGHT))

        for row in range(rows + 2):
            y = origin_offset.y + TILE_SIZE * row
            pygame.draw.line(self.support_line_surf, LINE_COLOR, start_pos=(0, y), end_pos=(WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surf, (0, 0))
        # debug(f'origin offset: {origin_offset}')

    def run(self, dt):
        self.event_loop()

        # bg
        self.display_surface.fill('gray')
        self.draw_tile_lines()

        # test item
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)

        # menu
        self.menu.display(self.selection_index)
