from pygame import draw, transform
from models.pipe import Pipe
import color


class Conduct:
    def create_intersection(self, neigh_from, neigh_to):
        pos_x = neigh_to.rect.centerx - 20
        pos_y = neigh_from.rect.centery - 20

        pipe = Pipe()

        pipe.is_curve = True

        distance_x = neigh_to.rect.centerx - neigh_from.rect.centerx
        distance_y = neigh_to.rect.centery - neigh_from.rect.centery

        pipe.flip_vertical = distance_x < 0
        pipe.flip_horizontal = distance_y > 0

        pipe.set_pos((pos_x, pos_y))

        return pipe

    def create_horizontal_pipes(self, pipes, neigh_from, neigh_to, intersection):
        distance_x = neigh_to.rect.centerx - neigh_from.rect.centerx

        base_x = intersection.rect.x - 64
        base_y = intersection.rect.y

        direction = -1

        if distance_x < 0:
            base_x = intersection.rect.right - 24
            direction = 1

        pipe_amount = int(abs(distance_x) / 64)

        for n in range(pipe_amount):
            pipe = Pipe()

            pos_x = base_x + pipe.rect.width * n * direction

            pipe.set_pos((pos_x, base_y))

            if direction == 1:
                pipe.angle = 180

            pipes.insert(0, pipe)

    def create_vertical_pipes(self, neigh_from, neigh_to, intersection):
        pipes = []
        distance_y = neigh_to.rect.centery - neigh_from.rect.centery

        base_x = intersection.rect.x
        base_y = intersection.rect.y - 64

        direction = -1

        if distance_y > 0:
            base_y = intersection.rect.bottom
            direction = 1

        pipe_amount = int(abs(distance_y) / 64)

        for n in range(pipe_amount):
            pipe = Pipe()

            pos_y = base_y + pipe.rect.width * n * direction

            pipe.set_pos((base_x, pos_y))

            pipe.angle = -direction * 90

            pipes.append(pipe)

        return pipes

    def create_pipes(self, neigh_from, neigh_to):
        pipes = []

        intersection = self.create_intersection(neigh_from, neigh_to)
        self.create_horizontal_pipes(pipes, neigh_from, neigh_to, intersection)
        pipes.append(intersection)
        pipes = pipes + self.create_vertical_pipes(neigh_from, neigh_to, intersection)

        return pipes

    def __init__(self, neigh_from, neigh_to, weight):
        self.neighs = [neigh_from, neigh_to]
        self.weight = weight
        self.closed = False
        self.pipes = self.create_pipes(neigh_from, neigh_to)
        self.frame = 0

    def move_water(self):
        self.frame += 1
        if self.frame % 4 != 0:
            return

        non_filled = list(filter(lambda p: p.state != 4, self.pipes))

        if len(non_filled) == 0:
            return

        non_filled[0].increase_state()

    def render(self, disp):
        self.move_water()
        for pipe in self.pipes:
            pipe.render(disp)
