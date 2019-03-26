from pygame import mouse, draw
import color


class Button:
    def __init__(
        self,
        click_fn,
        x=0,
        y=0,
        width=50,
        height=50,
        text="",
        text_color=color.BLACK,
        text_accent_color=color.BLACK,
        bg_color=color.GREEN,
        bg_accent_color=color.GREEN,
        disabled=False,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text
        self.text_color = text_color
        self.text_accent_color = text_accent_color
        self.bg_color = bg_color
        self.bg_accent_color = bg_accent_color

        self.disabled = disabled

        self.click = click_fn

    def is_hovered(self):
        mouse_pos = mouse.get_pos()
        return (
            self.x <= mouse_pos[0] <= self.x + self.width
            and self.y <= mouse_pos[1] <= self.y + self.height
        )

    def render(self, disp, font):
        bg_color = self.bg_color
        text_color = self.text_color

        if self.is_hovered():
            bg_color = self.bg_accent_color
            text_color = self.text_accent_color

        if self.disabled:
            bg_color = color.GRAY
            text_color = color.BLACK

        draw.rect(disp, bg_color, (self.x, self.y, self.width, self.height))

        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        disp.blit(text_surface, text_rect)
