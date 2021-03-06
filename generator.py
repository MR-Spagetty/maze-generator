import sys
import os

import map_maker
import keyboard
from display_type_selector import get_player_tile


class player:
    directions_opposites = {
            'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'
        }

    def __init__(self, up, down, left, right, map_object=map_maker.map()):
        self.up_control = up
        self.down_control = down
        self.left_control = left
        self.right_control = right
        self.map = map_object
        self.type = self.map.maze_type
        self.x = self.map.spawn_x
        self.y = self.map.spawn_y
        self.tile = []
        self.map.generate_tile(self.x, self.y)
        self.update_view()

        self.key_detection = keyboard.on_press(self.move)

    def update_view(self):
        os.system("cls" if os.name == 'nt' else "clear")
        if self.map.tiles[self.y][self.x].tile_type == 'block':
            self.tile = get_player_tile(self.type, '4-way_intersection')
        else:
            self.tile = get_player_tile(self.type,
                                        self.map.tiles[
                                            self.y][self.x].tile_type)
        self.map.print(self)

    def move(self, key):
        key = str(key)[14:-6]

        self.map.tiles[self.y][self.x].recheck_borders()
        if key == self.up_control:
            move_direction = 'up'
        elif key == self.down_control:
            move_direction = 'down'
        elif key == self.left_control:
            move_direction = 'left'
        elif key == self.right_control:
            move_direction = 'right'
        else:
            move_direction = False

        if move_direction:
            can_move = False
            Δx, Δy = self.map.tile.directions_relative_coordinates[
                move_direction]
            if move_direction in self.map.tiles[self.y][
                    self.x].passable_borders:
                can_move = self.map.tiles[self.y][self.x].passable_borders[
                    move_direction]
            if can_move is True and self.directions_opposites[
                    move_direction] in self.map.tiles[self.y + Δy][
                        self.x + Δx].passable_borders:
                self.map.tiles[self.y + Δy][self.x + Δx].recheck_borders()
                can_move = self.map.tiles[self.y + Δy][
                    self.x + Δx].passable_borders[self.directions_opposites[
                        move_direction]]
            if can_move is True:
                self.x += Δx
                self.y += Δy
                self.update_view()


if __name__ == '__main__':
    test_game = player('w', 's', 'a', 'd')
    while True:
        continue
