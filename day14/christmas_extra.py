import random
from typing import Tuple, List

from PIL import Image

Coords = Tuple[int, int]

PATTERN_PATH = "/Users/andreisitaev/sources/sennder/aoc2024/day14/pattern_small.png"


class Robot:
    def __init__(self, p: Coords):
        self.p = p
        while True:
            self.v = (random.randint(-11, 11), random.randint(-11, 11))
            sm = sum(map(abs, self.v))
            if sm > 10:
                break


class PatternBuilder:
    def build_pattern(self, output_path: str) -> None:
        w, h = 101, 103
        white_pixels = self.get_white_pixel_coordinates(PATTERN_PATH)
        robots = [Robot(p) for p in white_pixels]

        moves = 404
        for i in range(moves):
            for r in robots:
                x, y = r.p
                dx, dy = r.v
                x += dx
                y += dy
                r.p = (x, y)

        # store robots at output_path as lines "p=67,43 v=80,86"
        random.shuffle(robots)
        with open(output_path, "w") as f:
            for r in robots:
                # normalize coords
                x, y = r.p
                while x < 0 or x >= w:
                    x = x + w if x < 0 else x - w
                while y < 0 or y >= h:
                    y = y + h if y < 0 else y - h

                f.write(f"p={x},{y} v={-r.v[0]},{-r.v[1]}\n")


    @classmethod
    def get_white_pixel_coordinates(cls, file_path: str) -> List[Tuple[int, int]]:
        with Image.open(file_path) as img:
            img = img.convert("1")
            pixels = img.load()
            width, height = img.size
            white_pixels = [
                (x, y)
                for y in range(height)
                for x in range(width)
                if pixels[x, y] == 255
            ]

        return white_pixels


if __name__ == "__main__":
    pb = PatternBuilder()
    pb.build_pattern("/Users/andreisitaev/sources/sennder/aoc2024/day14/input_x.txt")
