"""Module for map generation
"""
import random
from display_type_selector import select_type
import display_system


class map_system:
    def __init__(self, seed=random.getrandbits(200), width=-1, height=-1,
                 has_end=False, maze_type='hedge', view_distance=2):
        """constructor of the map object

        Args:
            seed (int, optional): the seed of wich the map will generate from.
            Defaults to a random int of a 200 bit length.

            width (int, optional): the width of the map -1 being infinite.
            Defaults to -1.

            height (int, optional): the height of the map -1 being infinite.
            Defaults to -1.

            has_end (bool, optional): whaether or not the map has an end point.
            Defaults to False.

            maze_type (str, optional): the type of tiles that will be used.
            Defaults to 'hedge'.

            view_distance (int, optional): how far the player can see.
            Defaults to 2.
        """
        # setting up atributes
        self.random = random
        self.random.seed(seed)

        self.display = display_system.display(view_distance, maze_type)

        self.maze_type = maze_type

        self.width = width
        self.height = height
        self.has_end = has_end
        self.tiles = {0: {}}
        self.tile_displays = select_type(maze_type)
        self.view_distance = view_distance

        # setting max x, max y, spawn x, and spawn y coordinates
        self.spawn_x = 0
        if width == -1:
            self.minimum_x = False
            self.maximum_x = False
        else:
            self.minimum_x = 0
            self.maximum_x = width - 1

        self.spawn_y = 0
        if height == -1:
            self.minimum_y = False
            self.maximum_y = False
        else:
            self.minimum_y = 0
            self.maximum_y = height - 1
        self.tiles[0][0] = self.tile(self, 0, 0, '4-way_intersection')

    def generate_from_player(self, player):
        poss_directions = self.tile.possible_directions_by_type[
            self.tiles[player.y][player.x].tile_type]

        oppo_needed_directions = [
            self.tile.directions_opposites[direction]
            for direction in poss_directions
        ]

        possible_tiles_by_direction = {}
        connected_tiles_by_direction = {}
        for oppo_direction in oppo_needed_directions:
            possible_tiles_by_direction[oppo_direction] = []
            for tile, directions in self.tile.possible_directions_by_type.\
                    items():
                for direction in directions:
                    if direction == oppo_direction:
                        possible_tiles_by_direction[oppo_direction].append(
                            tile)
            connected_tiles_by_direction[oppo_direction] = self.random.choice(
                possible_tiles_by_direction[oppo_direction])

        for direction in poss_directions:
            Δx, Δy = self.tile.directions_relative_coordinates[direction]
            x = player.x + Δx
            y = player.y + Δy

            if y not in self.tiles:
                self.tiles[y] = {}
            if x not in self.tiles[y]:
                self.tiles[y][x] = self.tile(self, x, y,
                                             connected_tiles_by_direction[
                                                self.tile.directions_opposites[
                                                    direction]])
        self.tiles[y][x].recheck_borders()

    def print(self, player):
        for y in range(player.y + self.view_distance,
                       player.y - self.view_distance - 1, -1):
            if y not in self.tiles:
                self.tiles[y] = {}
        self.display.print(self.tiles, player.x, player.y, player.tile)

    class tile:
        possible_types = [
            'straight_vertical', 'straight_horizontal', '4-way_intersection',
            'intersection_no_left', 'intersection_no_right',
            'intersection_no_up', 'intersection_no_down', 'end_up', 'end_down',
            'end_left', 'end_right'
        ]

        possible_directions_by_type = {
            'straight_vertical': ['up', 'down'],
            'straight_horizontal': ['left', 'right'],
            '4-way_intersection': ['up', 'down', 'left', 'right'],
            'intersection_no_left': ['up', 'down', 'right'],
            'intersection_no_right': ['up', 'down', 'left'],
            'intersection_no_up': ['down', 'left', 'right'],
            'intersection_no_down': ['up', 'left', 'right'],
            'end_up': ['up'], 'end_down': ['down'], 'end_left': ['left'],
            'end_right': ['right'], 'block': []
        }

        directions_relative_coordinates = {
            'up': (0, 1), 'down': (0, -1), 'left': (-1, 0), 'right': (1, 0)
        }

        directions_opposites = {
            'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'
        }

        def __init__(self, parent_map, x, y, tile_type=None):
            """constructor of a tile object

            Args:
                parent_map (maze map object): the parent map object

                x (int): the x coordinate of the tile

                y (int): the y coordinate of the tile

                tile_type (str, optional): determines what kind of tile the
                tile will be e.g. straight_verticle if not specified the type
                will be determined by the map's seed. Defaults to None.
            """
            self.parent = parent_map
            self.x = x
            self.y = y
            if tile_type is not None:
                self.tile_type = tile_type
            else:
                self.tile_type = self.parent.random.choice(self.possible_types)
            self.passable_borders = {}
            for border in self.possible_directions_by_type[self.tile_type]:
                self.check_border(border)
            self.display = self.parent.tile_displays[self.tile_type]

        def check_border(self, border_to_check):
            """function for checking wheather or not a border of a tile is
            passable

            Args:
                border_to_check (str): the name of the border to check
            """
            change_in_x, change_in_y = self.directions_relative_coordinates[
                border_to_check]
            x_to_check = self.x + change_in_x
            y_to_check = self.y + change_in_y
            if y_to_check in self.parent.tiles:
                if x_to_check in self.parent.tiles[y_to_check]:
                    passable = self.directions_opposites[border_to_check] in\
                        self.possible_directions_by_type[self.parent.tiles[
                            y_to_check][x_to_check].tile_type]
                else:
                    passable = '?'
            else:
                passable = '?'
            if passable:
                self.passable_borders[border_to_check] = passable
            elif border_to_check in self.passable_borders:
                del self.passable_borders[border_to_check]

        def recheck_borders(self):
            if '?' in self.passable_borders.values():
                passable_borders = self.passable_borders.copy()
                for border, value in passable_borders.items():
                    if value == '?':
                        self.check_border(
                            border)
