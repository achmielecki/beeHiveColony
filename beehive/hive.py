import matplotlib.pyplot as plt
import numpy as np

from beehive.bee import Bee


class Hive:
    def __init__(self, num_bees, x, y, area_size=20):
        self.num_bees = num_bees
        self.x = x
        self.y = y
        self.area_size = area_size
        self.bees = []
        self.spawn_bees(num_bees)

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

    def simulate(self, num_iterations):
        for i in range(num_iterations):
            for bee in self.bees:
                bee.act()
