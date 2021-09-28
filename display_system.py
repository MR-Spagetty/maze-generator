from display_type_selector import select_type


class display:
    def __init__(self, view_distance, type):
        self.type = type
        self.view_distance = view_distance
        self.fill_tile = select_type(type)['block']

    def print(self, tiles, x, y, player_tile):
        """Prints the currently visable tiles

        Args:
            tiles (2D dict): the dictionary containing the tile objects

            x (int): the x coordinate of the player

            y (int): the y coordinate of the player

            player_tile (list): the display of the player's current tile
        """
        print(x, y)
        matrix = {}
        for dis_y in range(y + self.view_distance, y - self.view_distance - 1, -1):
            matrix[dis_y] = [
                [],
                [],
                [],
                [],
                []
            ]
            for dis_x in range(x - self.view_distance, x +
                               self.view_distance + 1):
                if (dis_x, dis_y) != (x, y):
                    for line_id, line_tile in zip(range(len(matrix[dis_y])),
                                                  tiles[dis_y][dis_x].display):
                        matrix[dis_y][line_id] += line_tile
                else:
                    for line_id, line_tile in zip(range(len(matrix[dis_y])),
                                                  player_tile):
                        matrix[dis_y][line_id] += line_tile
                matrix_y = []
            for line in matrix[dis_y]:
                matrix_y.append(''.join(line))
            matrix[dis_y] = '\n'.join(matrix_y)
        print('\n'.join(matrix.values()))
