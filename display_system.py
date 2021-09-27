from display_type_selector import select_type


class display:
    def __init__(self, view_distance, type):
        self.type = type
        self.view_distance = view_distance
        self.fill_tile = select_type(type)['block']

    def print(self, tiles, x, y, player_tile):
        matrix = {}
        for dis_y in range(y + self.view_distance, y - self.view_distance - 1):
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
                    for line_id, line_tile in range(len(matrix[dis_y])), tiles[
                            dis_y][dis_x]:
                        matrix[dis_y][line_id] += line_tile
                else:
                    for line_id, line_tile in range(len(matrix[dis_y])),\
                            player_tile:
                        matrix[dis_y][line_id] += line_tile
            matrix[y] = '\n'.join(matrix)[y]
        print('\n'.join())
