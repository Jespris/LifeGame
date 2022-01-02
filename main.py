# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pygame as p
from win32api import GetSystemMetrics
from Engine import Gamestate

# GLOBALS
SCREENSIZE = 1  # change this for different window sizes
WIDTH = int(GetSystemMetrics(0) * SCREENSIZE)
HEIGHT = int(GetSystemMetrics(1) * SCREENSIZE)
SQ_SIZE = WIDTH // 32
MAX_FPS = 30


def main():
    p.init()
    print("Click on squares to toggle them,\npress space to toggle paused, \npress 'r' while paused to reset")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    screen.fill(p.Color("black"))
    clock = p.time.Clock()
    gamestate = Gamestate(WIDTH, HEIGHT, SQ_SIZE)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                elif e.key == p.K_SPACE:
                    gamestate.is_paused = not gamestate.is_paused
                elif e.key == p.K_LEFT:
                    gamestate.generation_time += 0.2
                elif e.key == p.K_RIGHT:
                    gamestate.generation_time -= 0.2
                elif e.key == p.K_r and gamestate.is_paused:
                    gamestate.create_world()

            # mouse handler
            if e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if gamestate.is_paused:
                    gamestate.change_tile_with_mousepos(pos)

        gamestate.update(clock)
        Display_Game(gamestate, screen)

        p.display.flip()
        clock.tick(MAX_FPS)


def Display_Game(gamestate, screen):
    gap = 2
    for row in range(gamestate.nr_rows):
        for col in range(gamestate.nr_cols):
            tile = gamestate.world[row][col]
            color = gamestate.dead_color if not tile else gamestate.alive_color
            p.draw.rect(screen, color,
                        p.Rect((col * SQ_SIZE + gap, row * SQ_SIZE + gap), (SQ_SIZE - 2 * gap, SQ_SIZE - 2 * gap)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
