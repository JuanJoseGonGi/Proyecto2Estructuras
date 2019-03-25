from pygame import Rect
from models.neighborhood import Neighborhood
from models.conduct import Conduct


class City:
    def __init__(self):
        self.conducts = []
        self.neighborhoods = []

    def has_intersection(self, neigh1, neigh2):
        rect1 = Rect(
            neigh1.rect.x - 72,
            neigh1.rect.y - 43,
            neigh1.rect.width + 72,
            neigh1.rect.height + 43,
        )
        rect2 = Rect(
            neigh2.rect.x - 72,
            neigh2.rect.y - 43,
            neigh2.rect.width + 72,
            neigh2.rect.height + 43,
        )
        return rect1.colliderect(rect2)

    def set_neighbor_pos(self, neighbor):
        n = len(self.neighborhoods) - 1
        tries = 0
        while n >= 0:
            while self.has_intersection(neighbor, self.neighborhoods[n]):
                if tries > 5000:
                    return False
                neighbor.set_random_pos()
                tries += 1
                n = len(self.neighborhoods) - 1
            n -= 1

        return True

    def add_conduct(self, n_from, n_to):
        for condu in self.conducts:
            if n_from in condu.neighs and n_to in condu.neighs:
                return

        conduct = Conduct(n_from, n_to, 0)
        n_from.adjacencies.append(n_to)
        self.conducts.append(conduct)

    def add_neighborhood(self, name):
        for neighbor in self.neighborhoods:
            if neighbor.name == name:
                return

        neighbor = Neighborhood(name)
        can = self.set_neighbor_pos(neighbor)

        if not can:
            print("No more space")
            return None

        self.neighborhoods.append(neighbor)
        return neighbor

    def find_neighborhood(self, name):
        for neighbor in self.neighborhoods:
            if neighbor.name == name:
                return neighbor

    def render(self, disp, font):
        for conduct in self.conducts:
            conduct.render(disp)

        for neighbor in self.neighborhoods:
            neighbor.render(disp, font)
