from pygame import image, Rect, Color, mouse, gfxdraw
from models.tank import Tank

import color

from random import randint


class Neighborhood:
    def __init__(self, name):
        self.tank = None
        self.adjacencies = []
        self.rect = Rect(randint(30, 1192), randint(30, 652), 144, 86)
        self.image = image.load("img/neighborhood/neighborhood.png")
        self.name = name
        self.selected = False

    def set_pos(self, pos):
        self.rect = Rect(pos, (144, 86))

    def set_random_pos(self):
        self.rect = Rect(randint(30, 1192), randint(30, 652), 144, 86)

    def set_tank(self, capacity):
        self.tank = Tank(capacity, (self.rect.right - 32, self.rect.bottom - 32))
        self.water = capacity

    def is_hovered(self):
        mouse_pos = mouse.get_pos()
        return (
            self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.width
            and self.rect.y <= mouse_pos[1] <= self.rect.y + self.rect.height
        )

    def decrease(self, amount):
        if self.tank:
            self.tank.amount -= amount
            if self.tank.amount < 0:
                self.tank.amount = 0

    def increase(self, amount):
        if self.tank:
            self.tank.amount += amount
            if self.tank.amount > 500:
                self.tank.amount = 500
                self.over = True
            else:
                self.over = False

    def render(self, disp, font):
        disp.blit(self.image, self.rect)

        if self.selected:
            gfxdraw.filled_circle(disp, self.rect.right, self.rect.y, 14, color.RED)
            gfxdraw.aacircle(disp, self.rect.right, self.rect.y, 14, color.RED)

        if self.tank:
            self.tank.render(disp, font)
