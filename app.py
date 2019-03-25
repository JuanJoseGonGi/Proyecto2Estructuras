import os
import color
import json
import pygame as pg
from models.button import Button
from models.city import City


class App:
    def load_inital_city(self):
        city = City()
        with open("json/ciudad.json") as json_file:
            data = json.load(json_file)
            for neighborhood in data:
                neighbor = city.add_neighborhood(neighborhood["name"])
                neighbor.set_tank(neighborhood["tank"]["capacity"])

            for neighborhood in data:
                for adj in neighborhood["adjacencies"]:
                    neighbor_from = city.find_neighborhood(neighborhood["name"])
                    neighbor_to = city.find_neighborhood(adj)

                    if neighbor_from is None or neighbor_to is None:
                        continue

                    city.add_conduct(neighbor_from, neighbor_to)

        return city

    def __init__(self):
        # Pygame stuff
        self._clock = pg.time.Clock()
        self._running = True
        self._disp = None

        # Window size and pos
        self.width = 1366
        self.height = 768
        self.x = 183
        self.y = 206
        self.size = self.width, self.height

        # Font definitions
        self.smallFont = None
        self.mediumFont = None
        self.largeFont = None

        # Objects definition
        self.close_btn = None
        self.city = self.load_inital_city()

        # Center the window
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i,%i" % (self.x, self.y)
        os.environ["SDL_VIDEO_CENTERED"] = "0"

    def stop(self):
        self._running = False

    def on_init(self):
        pg.init()

        pg.display.set_caption("Pipes")
        self._disp = pg.display.set_mode(
            self.size, pg.HWSURFACE | pg.DOUBLEBUF | pg.NOFRAME
        )

        self.smallFont = pg.font.Font("fonts/Montserrat-Regular.ttf", 15)
        self.mediumFont = pg.font.Font("fonts/Montserrat-Regular.ttf", 25)
        self.largeFont = pg.font.Font("fonts/Montserrat-Regular.ttf", 40)

        self.close_btn = Button(
            x=1336,
            y=0,
            width=30,
            height=30,
            text="X",
            text_color=color.WHITE,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.RED,
            click_fn=self.stop,
        )

        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._disp.fill(color.BLACK)

        self.close_btn.render(self._disp, self.smallFont)

        self.city.render(self._disp)

        pg.display.update()

    def on_cleanup(self):
        pg.quit()

    def on_execute(self):
        self.on_init()

        while self._running:
            for event in pg.event.get():
                self.on_event(event)

            self.on_loop()

            self.on_render()

            # Limit to 60 fps
            self._clock.tick(60)

        self.on_cleanup()
