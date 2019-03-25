from pygame import image


class Tank:
    def __init__(self, capacity, pos):
        self.capacity = capacity
        self.pos = pos
        self.rect = (pos, (64, 64))
        self.amount = capacity
        self.image = image.load("img/tank/4.png")

    def render(self, disp):
        img = int(self.amount / self.capacity * 4)

        self.image = image.load("img/tank/" + str(img) + ".png")
        disp.blit(self.image, self.rect)
