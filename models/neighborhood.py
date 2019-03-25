from pygame import image, Rect, Color
from models.tank import Tank

from random import randint


class Neighborhood:
    def __init__(self, name):
        self.tank = None
        self.adjacencies = []
        self.rect = Rect(randint(30, 1192), randint(30, 652), 144, 86)
        self.image = image.load("img/neighborhood/neighborhood.png")
        self.name = name

    def set_pos(self, pos):
        self.rect = Rect(pos, (144, 86))

    def set_random_pos(self):
        self.rect = Rect(randint(30, 1192), randint(30, 652), 144, 86)

    def set_tank(self, capacity):
        self.tank = Tank(capacity, (self.rect.right - 32, self.rect.bottom - 32))

    def render(self, disp, font):
        disp.blit(self.image, self.rect)

        text_surface = font.render(self.name, True, Color("#FFFFFF"))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.rect.x - 12, self.rect.y - 12)
        disp.blit(text_surface, text_rect)

        if self.tank:
            self.tank.render(disp)
