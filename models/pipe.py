from pygame import image, Rect, transform, mouse


class Pipe:
    def __init__(self):
        self.rect = Rect((0, 0), (64, 40))
        self.state = 0
        self.angle = 0
        self.is_curve = False
        self.flip_horizontal = False
        self.flip_vertical = False
        self.image = image.load("img/pipe/0.png")
        self.was_animated = False
        self.hide = False
        self.empty = False

    def set_pos(self, pos):
        self.rect = Rect(pos, (64, 40))

    def increase_state(self, amount=1):
        self.state += amount
        if self.state > 8:
            self.state = 0

    def decrease_state(self, amount=1):
        self.state -= amount
        if self.state < 0:
            self.state = 4

    def is_hovered(self):
        mouse_pos = mouse.get_pos()
        return (
            self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.width
            and self.rect.y <= mouse_pos[1] <= self.rect.y + self.rect.height
        )

    def render(self, disp):
        if self.hide:
            return

        curve = ""
        if self.is_curve:
            curve = "curve/"
        path = curve + str(self.state) + ".png"

        if self.empty:
            path = curve + "0.png"

        self.image = transform.rotate(image.load("img/pipe/" + path), self.angle)

        self.image = transform.flip(
            self.image, self.flip_vertical, self.flip_horizontal
        )

        disp.blit(self.image, self.rect)
