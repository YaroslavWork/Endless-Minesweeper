import random

import pygame.draw

from scripts.game.chunk import Chunk


class Field:

    def __init__(self) -> None:
        self.chunks = {

        }

    def create_chunk(self, pos) -> None:
        if self.chunks.get(pos) is None:
            self.chunks[pos] = Chunk(pos, 0.1)
            self.chunks[pos].create_bomb()

            self.edge = {
                "left": None,
                "right": None,
                "top": None,
                "bottom": None,
                "top_left": None,
                "top_right": None,
                "bottom_left": None,
                "bottom_right": None
            }

            if self.chunks.get((pos[0] - 1, pos[1])) is not None:
                print(f"Copied left edge from {pos[0] - 1, pos[1]} to {pos}")
                self.edge["left"] = self.chunks[(pos[0] - 1, pos[1])].get_right_edge()
                self.chunks[pos].set_left_row(self.chunks[(pos[0] - 1, pos[1])].edges["right"])
            if self.chunks.get((pos[0] + 1, pos[1])) is not None:
                print(f"Copied right edge from {pos[0] + 1, pos[1]} to {pos}")
                self.edge["right"] = self.chunks[(pos[0] + 1, pos[1])].get_left_edge()
                self.chunks[pos].set_right_row(self.chunks[(pos[0] + 1, pos[1])].edges["left"])
            if self.chunks.get((pos[0], pos[1] - 1)) is not None:
                print(f"Copied top edge from {pos[0], pos[1] - 1} to {pos}")
                self.edge["top"] = self.chunks[(pos[0], pos[1] - 1)].get_bottom_edge()
                self.chunks[pos].set_top_row(self.chunks[(pos[0], pos[1] - 1)].edges["bottom"])
            if self.chunks.get((pos[0], pos[1] + 1)) is not None:
                print(f"Copied bottom edge from {pos[0], pos[1] + 1} to {pos}")
                self.edge["bottom"] = self.chunks[(pos[0], pos[1] + 1)].get_top_edge()
                self.chunks[pos].set_bottom_row(self.chunks[(pos[0], pos[1] + 1)].edges["top"])
            if self.chunks.get((pos[0] - 1, pos[1] - 1)) is not None:
                print(f"Copied top left edge from {pos[0] - 1, pos[1] - 1} to {pos}")
                self.edge["top_left"] = self.chunks[(pos[0] - 1, pos[1] - 1)].get_bottom_right_edge()
                #self.chunks[pos].set_top_left_row(self.chunks[(pos[0] - 1, pos[1] - 1)].edges["bottom_right"])
            if self.chunks.get((pos[0] + 1, pos[1] - 1)) is not None:
                print(f"Copied top right edge from {pos[0] + 1, pos[1] - 1} to {pos}")
                self.edge["top_right"] = self.chunks[(pos[0] + 1, pos[1] - 1)].get_bottom_left_edge()
                #self.chunks[pos].set_top_right_row(self.chunks[(pos[0] + 1, pos[1] - 1)].edges["bottom_left"])
            if self.chunks.get((pos[0] - 1, pos[1] + 1)) is not None:
                print(f"Copied bottom left edge from {pos[0] - 1, pos[1] + 1} to {pos}")
                self.edge["bottom_left"] = self.chunks[(pos[0] - 1, pos[1] + 1)].get_top_right_edge()
                #self.chunks[pos].set_bottom_left_row(self.chunks[(pos[0] - 1, pos[1] + 1)].edges["top_right"])
            if self.chunks.get((pos[0] + 1, pos[1] + 1)) is not None:
                print(f"Copied bottom right edge from {pos[0] + 1, pos[1] + 1} to {pos}")
                self.edge["bottom_right"] = self.chunks[(pos[0] + 1, pos[1] + 1)].get_top_left_edge()
                #self.chunks[pos].set_bottom_right_row(self.chunks[(pos[0] + 1, pos[1] + 1)].edges["top_left"])

            self.chunks[pos].create_edges(self.edge["left"], self.edge["right"], self.edge["top"], self.edge["bottom"],
                                       self.edge["top_left"], self.edge["top_right"], self.edge["bottom_left"],
                                       self.edge["bottom_right"])

            self.chunks[pos].update_numbers()

    def draw(self, screen, camera) -> None:
        for chunk in self.chunks.values():
            chunk.draw(screen, camera)