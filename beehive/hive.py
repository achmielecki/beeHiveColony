import numpy as np

from beehive.bee.bee import Bee


class Hive:
    def __init__(
            self,
            world,
            num_bees,
            x,
            y,
            area_size=40
    ):
        self.world = world
        self.num_bees = num_bees
        self.x = x
        self.y = y
        self.area_size = area_size
        self.bees = []
        self.spawn_bees(num_bees)
        self.food_stored = 0

    def spawn_bees(self, num_bees):
        for i in range(num_bees):
            self.spawn_bee()

    def spawn_bee(self):
        self.bees.append(
            Bee(
                self,
                self.x + np.random.rand() * self.area_size,
                self.y + np.random.rand() * self.area_size
            )
        )

    def leave_food(self, count):
        self.food_stored += count

    def get_food_sources(self):
        return self.world.get_food_sources()

    def get_bees_x_positions(self):
        x_bees = []
        for bee in self.bees:
            x_bees.append(bee.x)
        return x_bees

    def get_bees_y_positions(self):
        y_bees = []
        for bee in self.bees:
            y_bees.append(bee.y)
        return y_bees

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_pos(self):
        return self.x, self.y

    def get_bees(self):
        return self.bees

    def simulate(self):
        for bee in self.bees:
            bee.act()
