from pygame import image, Color, Rect


class Tank:
    def __init__(self, capacity, pos):
        self.capacity = capacity
        self.pos = pos
        self.rect = Rect(pos, (64, 64))
        self.amount = capacity
        self.image = image.load("img/tank/4.png")
        self.empty = False
        self.over = False

    def render(self, disp, font):
        img_num = int(self.amount / self.capacity * 4)

        if self.over:
            img_num = 5

        self.image = image.load("img/tank/" + str(img_num) + ".png")
        disp.blit(self.image, self.rect)

        text_surface = font.render(str(self.amount), True, Color("#000000"))
        text_rect = text_surface.get_rect()
        text_rect.center = (self.rect.centerx - 12, self.rect.centery - 12)
        disp.blit(text_surface, text_rect)
