from scripts.UI.text import Text
from scripts.settings import CHUNK_SIZE
import random
import pygame.draw

def generate_row(size, bomb_ratio) -> list:
    row = [0 for _ in range(size)]
    for i in range(size):
        if random.random() < bomb_ratio:
            row[i] = -1
    return row

def generate_tile(size, bomb_ratio) -> int:
    return -1 if random.random() < bomb_ratio else 0

class Chunk:

    def __init__(self, pos=None, bomb_ratio=0.1) -> None:
        if pos is None:
            pos = [0, 0]
        self.pos = pos

        self.size = CHUNK_SIZE
        self.tiles = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.is_open = [[True for _ in range(self.size)] for _ in range(self.size)]
        self.edges = {
            "left": None,
            "right": None,
            "top": None,
            "bottom": None,
            "top_left": None,
            "top_right": None,
            "bottom_left": None,
            "bottom_right": None
        }
        self.bomb_ratio = bomb_ratio
        # self.create_bomb()
        # self.create_edges()
        # self.update_numbers()

    def create_bomb(self):
        for x in range(self.size):
            for y in range(self.size):
                if random.random() < self.bomb_ratio:
                    self.tiles[x][y] = -1

    def create_edges(self, left=None, right=None, top=None, bottom=None, top_left=None, top_right=None,
                     bottom_left=None, bottom_right=None):
        self.edges["left"] = generate_row(self.size, self.bomb_ratio) if left is None else left
        self.edges["right"] = generate_row(self.size, self.bomb_ratio) if right is None else right
        self.edges["top"] = generate_row(self.size, self.bomb_ratio) if top is None else top
        self.edges["bottom"] = generate_row(self.size, self.bomb_ratio) if bottom is None else bottom
        self.edges["top_left"] = generate_tile(self.size, self.bomb_ratio) if top_left is None else top_left
        self.edges["top_right"] = generate_tile(self.size, self.bomb_ratio) if top_right is None else top_right
        self.edges["bottom_left"] = generate_tile(self.size, self.bomb_ratio) if bottom_left is None else bottom_left
        self.edges["bottom_right"] = generate_tile(self.size, self.bomb_ratio) if bottom_right is None else bottom_right

    def update_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.tiles[i][j] == -1:
                    continue
                self.tiles[i][j] = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if x == 0 and y == 0:
                            continue
                        if 0 <= i + x < self.size and 0 <= j + y < self.size:  # Check if the tile is in the chunk
                            if self.tiles[i + x][j + y] == -1:
                                self.tiles[i][j] += 1


        for i in range(self.size):
            # For up
            if self.tiles[i][0] != -1:
                for x in range(-1, 2):
                    if 0 <= i + x < self.size:
                        if self.edges["top"][i + x] == -1:
                            self.tiles[i][0] += 1

            # For down
            if self.tiles[i][self.size - 1] != -1:
                for x in range(-1, 2):
                    if 0 <= i + x < self.size:
                        if self.edges["bottom"][i + x] == -1:
                            self.tiles[i][self.size - 1] += 1

            # For left
            if self.tiles[0][i] != -1:
                for y in range(-1, 2):
                    if 0 <= i + y < self.size:
                        if self.edges["left"][i + y] == -1:
                            self.tiles[0][i] += 1

            # For right
            if self.tiles[self.size - 1][i] != -1:
                for y in range(-1, 2):
                    if 0 <= i + y < self.size:
                        if self.edges["right"][i + y] == -1:
                            self.tiles[self.size - 1][i] += 1

        if self.edges["top_left"] == -1 and self.tiles[0][0] != -1:
            self.tiles[0][0] += 1
        if self.edges["top_right"] == -1 and self.tiles[self.size - 1][0] != -1:
            self.tiles[self.size - 1][0] += 1
        if self.edges["bottom_left"] == -1 and self.tiles[0][self.size - 1] != -1:
            self.tiles[0][self.size - 1] += 1
        if self.edges["bottom_right"] == -1 and self.tiles[self.size - 1][self.size - 1] != -1:
            self.tiles[self.size - 1][self.size - 1] += 1

    def get_tile(self, x: int, y: int) -> int:
        return self.tiles[x][y]

    def get_left_edge(self) -> list:
        return [self.tiles[0][i] for i in range(self.size)]

    def get_right_edge(self) -> list:
        return [self.tiles[self.size - 1][i] for i in range(self.size)]

    def get_top_edge(self) -> list:
        return [self.tiles[i][0] for i in range(self.size)]

    def get_bottom_edge(self) -> list:
        return [self.tiles[i][self.size - 1] for i in range(self.size)]

    def get_top_left_edge(self) -> int:
        return self.tiles[0][0]

    def get_top_right_edge(self) -> int:
        return self.tiles[self.size - 1][0]

    def get_bottom_left_edge(self) -> int:
        return self.tiles[0][self.size - 1]

    def get_bottom_right_edge(self) -> int:
        return self.tiles[self.size - 1][self.size - 1]

    def set_left_row(self, row: list) -> None:
        for i in range(self.size):
            self.tiles[0][i] = row[i]

    def set_right_row(self, row: list) -> None:
        for i in range(self.size):
            self.tiles[self.size - 1][i] = row[i]

    def set_top_row(self, row: list) -> None:
        for i in range(self.size):
            self.tiles[i][0] = row[i]

    def set_bottom_row(self, row: list) -> None:
        for i in range(self.size):
            self.tiles[i][self.size - 1] = row[i]

    def set_top_left_row(self, value: int) -> None:
        self.tiles[0][0] = value

    def set_top_right_row(self, value: int) -> None:
        self.tiles[self.size - 1][0] = value

    def set_bottom_left_row(self, value: int) -> None:
        self.tiles[0][self.size - 1] = value

    def set_bottom_right_row(self, value: int) -> None:
        self.tiles[self.size - 1][self.size - 1] = value

    # --- Draw ---
    def draw(self, screen, camera):
        for i in range(self.size):
            for j in range(self.size):
                local_pos = camera.get_local_point(i + self.pos[0] * self.size, j + self.pos[1] * self.size)
                local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
                size = camera.get_local_radius(1)+1

                if self.is_open[i][j]:
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(screen, [255, 233, 175], [local_pos[0], local_pos[1], size, size])
                    else:
                        pygame.draw.rect(screen, [255, 223, 175], [local_pos[0], local_pos[1], size, size])

                    if self.tiles[i][j] == -1:
                        pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3)
                    else:
                        if self.tiles[i][j] > 0:
                            Text(str(self.tiles[i][j]), [0, 0, 0], int(size/1.65)).print(screen, (local_pos_center[0], local_pos_center[1]), True)
                else:
                    if (i + j) % 2 == 0:
                        pygame.draw.rect(screen, [128, 179, 255], [local_pos[0], local_pos[1], size, size])
                    else:
                        pygame.draw.rect(screen, [120, 171, 247], [local_pos[0], local_pos[1], size, size])

        # dra edges as a border line
        point1 = camera.get_local_point(self.pos[0] * self.size, self.pos[1] * self.size)
        point2 = camera.get_local_point(self.pos[0] * self.size + self.size, self.pos[1] * self.size)
        point3 = camera.get_local_point(self.pos[0] * self.size + self.size, self.pos[1] * self.size + self.size)
        point4 = camera.get_local_point(self.pos[0] * self.size, self.pos[1] * self.size + self.size)
        pygame.draw.line(screen, [0, 0, 0], point1, point2, 2)
        pygame.draw.line(screen, [0, 0, 0], point2, point3, 2)
        pygame.draw.line(screen, [0, 0, 0], point3, point4, 2)
        pygame.draw.line(screen, [0, 0, 0], point4, point1, 2)



        # # For the top
        # for i in range(self.size):
        #     local_pos = camera.get_local_point(i + self.pos[0] * self.size, self.pos[1] * self.size - 1)
        #     local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        #     size = camera.get_local_radius(1)+1
        #
        #     if self.edges["top"][i] == -1:
        #         pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3)
        #     else:
        #         Text(str(self.edges["top"][i]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the bottom
        # for i in range(self.size):
        #     local_pos = camera.get_local_point(i + self.pos[0] * self.size, self.pos[1] * self.size + self.size)
        #     local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        #     size = camera.get_local_radius(1)+1
        #
        #     if self.edges["bottom"][i] == -1:
        #         pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3)
        #     else:
        #         Text(str(self.edges["bottom"][i]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the left
        # for i in range(self.size):
        #     local_pos = camera.get_local_point(self.pos[0] * self.size - 1, i + self.pos[1] * self.size)
        #     local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        #     size = camera.get_local_radius(1)+1
        #
        #     if self.edges["left"][i] == -1:
        #         pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3)
        #     else:
        #         Text(str(self.edges["left"][i]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the right
        # for i in range(self.size):
        #     local_pos = camera.get_local_point(self.pos[0] * self.size + self.size, i + self.pos[1] * self.size)
        #     local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        #     size = camera.get_local_radius(1)+1
        #
        #     if self.edges["right"][i] == -1:
        #         pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3)
        #     else:
        #         Text(str(self.edges["right"][i]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the top left
        # local_pos = camera.get_local_point(self.pos[0] * self.size - 1, self.pos[1] * self.size - 1)
        # local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        # size = camera.get_local_radius(1)+1
        # pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3) if self.edges["top_left"] == -1 else Text(str(self.edges["top_left"]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the top right
        # local_pos = camera.get_local_point(self.pos[0] * self.size + self.size, self.pos[1] * self.size - 1)
        # local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        # size = camera.get_local_radius(1)+1
        # pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3) if self.edges["top_right"] == -1 else Text(str(self.edges["top_right"]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the bottom left
        # local_pos = camera.get_local_point(self.pos[0] * self.size - 1, self.pos[1] * self.size + self.size)
        # local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        # size = camera.get_local_radius(1)+1
        # pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3) if self.edges["bottom_left"] == -1 else Text(str(self.edges["bottom_left"]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)
        #
        # # For the bottom right
        # local_pos = camera.get_local_point(self.pos[0] * self.size + self.size, self.pos[1] * self.size + self.size)
        # local_pos_center = (local_pos[0] + camera.get_local_radius(1) // 2, local_pos[1] + camera.get_local_radius(1) // 2)
        # size = camera.get_local_radius(1)+1
        # pygame.draw.circle(screen, [255, 0, 0], (local_pos_center[0], local_pos_center[1]), size / 3) if self.edges["bottom_right"] == -1 else Text(str(self.edges["bottom_right"]), [0, 0, 0], 20).print(screen, (local_pos_center[0], local_pos_center[1]), True)