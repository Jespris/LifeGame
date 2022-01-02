"""
Responsible for gamestate
"""

import pygame as p


class Gamestate:
    def __init__(self, width, height, sq_size):
        self.width = width
        self.height = height
        self.sq_size = sq_size

        self.nr_rows = self.height // sq_size
        self.nr_cols = self.width // sq_size
        self.alive_color = p.Color("green")
        self.dead_color = p.Color("grey")

        self.world = []
        self.create_world()
        # self.add_test_block()

        self.generation = 0
        self.time_until_next_gen = 0
        self.generation_time = 0.5
        self.is_paused = True

    def change_tile_with_mousepos(self, pos):
        row, col = self.get_tile(pos)
        self.world[row][col] = not self.world[row][col]

    def get_tile(self, pos):
        return pos[1] // self.sq_size, pos[0] // self.sq_size

    def update(self, clock):
        if not self.is_paused:
            self.time_until_next_gen -= clock.get_time() / 1000
            if self.time_until_next_gen <= 0:
                print("Next gen!")
                self.do_generation()
                self.generation += 1
                self.time_until_next_gen = self.generation_time

    def create_world(self):
        world = []
        for i in range(self.nr_rows):
            row = []
            for k in range(self.nr_cols):
                row.append(False)
            world.append(row)
        self.world = world

    def do_generation(self):
        new_world = []
        for row in range(self.nr_rows):
            new_row = []
            for col in range(self.nr_cols):
                neighbours = self.check_neighbours(row, col)
                if self.world[row][col]:
                    if neighbours <= 1 or neighbours >= 4:
                        alive = False
                    else:
                        alive = True
                else:
                    if neighbours == 3:
                        alive = True
                    else:
                        alive = False
                new_row.append(alive)
            new_world.append(new_row)
        self.world = new_world

    def check_neighbours(self, row, col):
        cardinals = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1))
        neighbours = 0
        for direction in cardinals:
            new_row = row + direction[0]
            new_col = col + direction[1]
            if self.inside_map(new_row, new_col):
                tile = self.world[new_row][new_col]
                neighbours += 1 if tile else 0
        return neighbours

    def inside_map(self, row, col):
        return 0 <= row < self.nr_rows and 0 <= col < self.nr_cols

    def add_test_block(self):
        self.world[self.nr_rows // 2][self.nr_cols // 2] = True
        self.world[self.nr_rows // 2 + 1][self.nr_cols // 2] = True
        self.world[self.nr_rows // 2 + 2][self.nr_cols // 2] = True
        self.world[self.nr_rows // 2 + 2][self.nr_cols // 2 - 1] = True
        self.world[self.nr_rows // 2 + 1][self.nr_cols // 2 - 2] = True

