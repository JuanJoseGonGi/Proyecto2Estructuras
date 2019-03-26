import os
import color
import json
import pygame as pg
from models.button import Button
from models.city import City
from random import randint
from string import ascii_uppercase


class App:
    def load_inital_city(self):
        city = City()
        with open("json/ciudad.json") as json_file:
            data = json.load(json_file)
            for neighborhood in data:
                neighbor = city.add_neighborhood(neighborhood["name"])
                if neighborhood["tank"]:
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
        self.x = 0
        self.y = 0
        self.size = self.width, self.height

        # Font definitions
        self.smallFont = None
        self.mediumFont = None
        self.largeFont = None

        # Objects definition
        self.close_btn = None
        self.add_btn = None
        self.obstruction_btn = None
        self.change_dir_btn = None
        self.create_conduct_btn = None
        self.create_tank_btn = None
        self.city = self.load_inital_city()

        # Event flags
        self.is_obstructing = False
        self.is_changing_dir = False
        self.is_creating_tank = False
        self.to_create_conduct = None

        # Center the window
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i,%i" % (self.x, self.y)
        os.environ["SDL_VIDEO_CENTERED"] = "0"

    def stop(self):
        self._running = False

    def add(self):
        name = ""
        for letter in ascii_uppercase:
            neigh = list(filter(lambda n: n.name == letter, self.city.neighborhoods))
            if not len(neigh):
                name = letter

        neighbor = self.city.add_neighborhood(name)

        if not neighbor:
            return

        if randint(0, 1):
            neighbor.set_tank(randint(100, 500))

        if randint(0, 1) and neighbor.tank:
            n = len(self.city.neighborhoods) - 1

            pos = randint(0, n)

            while (
                self.city.neighborhoods[pos] == neighbor
                and not self.city.neighborhoods[pos].tank
            ):
                pos = randint(0, n)

            self.city.add_conduct(neighbor, self.city.neighborhoods[pos])
            return

        if randint(0, 1):
            n = len(self.city.neighborhoods) - 1

            pos = randint(0, n)

            while self.city.neighborhoods[pos] == neighbor:
                pos = randint(0, n)

            self.city.add_conduct(self.city.neighborhoods[pos], neighbor)

    def obstruct(self):
        self.is_obstructing = True
        self.obstruction_btn.disabled = True

    def change_dir(self):
        self.is_changing_dir = True
        self.change_dir_btn.disabled = True

    def conduct(self):
        self.to_create_conduct = []
        self.create_conduct_btn.disabled = True

    def tank(self):
        self.is_creating_tank = True
        self.create_tank_btn.disabled = True

    def button_events(self):
        if not self.close_btn.disabled and self.close_btn.is_hovered():
            self.close_btn.click()

        if not self.add_btn.disabled and self.add_btn.is_hovered():
            self.add_btn.click()

        if not self.obstruction_btn.disabled and self.obstruction_btn.is_hovered():
            self.obstruction_btn.click()

        if not self.change_dir_btn.disabled and self.change_dir_btn.is_hovered():
            self.change_dir_btn.click()

        if (
            not self.create_conduct_btn.disabled
            and self.create_conduct_btn.is_hovered()
        ):
            self.create_conduct_btn.click()

        if not self.create_tank_btn.disabled and self.create_tank_btn.is_hovered():
            self.create_tank_btn.click()

    def conduct_events(self):
        for conduct in self.city.conducts:
            for pipe in conduct.pipes:
                if pipe.is_hovered():
                    if self.is_obstructing:
                        conduct.close()
                        self.obstruction_btn.disabled = False
                        self.is_obstructing = False
                    if self.is_changing_dir:
                        conduct.change_dir()
                        self.change_dir_btn.disabled = False
                        self.is_changing_dir = False

    def neighbor_events(self):
        for neighbor in self.city.neighborhoods:
            if self.to_create_conduct is not None and neighbor.is_hovered():
                self.to_create_conduct.append(neighbor)
                neighbor.selected = True
                if len(self.to_create_conduct) != 2:
                    return

                self.city.add_conduct(
                    self.to_create_conduct[0], self.to_create_conduct[1]
                )
                self.to_create_conduct[0].selected = False
                self.to_create_conduct[1].selected = False

                self.create_conduct_btn.disabled = False
                self.to_create_conduct = None
                break

            if self.is_creating_tank and neighbor.is_hovered():
                if neighbor.tank:
                    return
                neighbor.set_tank(randint(100, 500))
                self.is_creating_tank = False
                self.create_tank_btn.disabled = False

    def without_filter(self, n):
        if n.tank:
            n.highlight = False
            return False

        for neigh in self.city.neighborhoods:
            if not neigh.tank:
                neigh.highlight = False
                continue

            if n in neigh.adjacencies:
                n.highlight = False
                return False

        return True

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
            text_color=color.RED,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.RED,
            click_fn=self.stop,
        )

        self.add_btn = Button(
            x=0,
            y=738,
            width=30,
            height=30,
            text="+",
            text_color=color.GREEN,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.GREEN,
            click_fn=self.add,
        )

        self.obstruction_btn = Button(
            x=30,
            y=738,
            width=200,
            height=30,
            text="Obstruction",
            text_color=color.ORANGE,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.ORANGE,
            click_fn=self.obstruct,
        )

        self.change_dir_btn = Button(
            x=230,
            y=738,
            width=260,
            height=30,
            text="Change direction",
            text_color=color.BLUE,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.BLUE,
            click_fn=self.change_dir,
        )

        self.create_conduct_btn = Button(
            x=490,
            y=738,
            width=260,
            height=30,
            text="Create conduct",
            text_color=color.PURPLE,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.PURPLE,
            click_fn=self.conduct,
        )

        self.create_tank_btn = Button(
            x=750,
            y=738,
            width=160,
            height=30,
            text="Add tank",
            text_color=color.YELLOW,
            text_accent_color=color.BLACK,
            bg_color=color.BLACK,
            bg_accent_color=color.YELLOW,
            click_fn=self.tank,
        )

        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.button_events()
            self.conduct_events()
            self.neighbor_events()

    def on_loop(self):
        without_tank = filter(lambda n: self.without_filter(n), self.city.neighborhoods)
        for neigh in without_tank:
            neigh.highlight = True

    def on_render(self):
        self._disp.fill(color.BLACK)

        self.close_btn.render(self._disp, self.smallFont)
        self.add_btn.render(self._disp, self.mediumFont)
        self.obstruction_btn.render(self._disp, self.mediumFont)
        self.change_dir_btn.render(self._disp, self.mediumFont)
        self.create_conduct_btn.render(self._disp, self.mediumFont)
        self.create_tank_btn.render(self._disp, self.mediumFont)

        self.city.render(self._disp, self.smallFont)

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
