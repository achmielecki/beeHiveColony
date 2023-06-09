import numpy as np
import matplotlib.pyplot as plt
from beehive.foodSource import FoodSource
from beehive.hive import Hive


class World:
    def __init__(self, num_hives, num_bees_per_hive, num_food_sources, world_size=50, hives_area=20):
        self.num_hives = num_hives
        self.num_bees_per_hive = num_bees_per_hive
        self.num_food_sources = num_food_sources
        self.world_size = world_size
        self.hives_area = hives_area
        self.hives = []
        self.food_sources = []
        self.spawn_hives(num_bees_per_hive)
        self.spawn_food(num_food_sources, world_size)

    def spawn_food(self, num_food_sources, world_size):
        for i in range(num_food_sources):
            self.food_sources.append(
                FoodSource(
                    np.random.rand() * world_size,
                    np.random.rand() * world_size
                )
            )

    def spawn_hives(self, num_bees):
        for i in range(num_bees):
            self.spawn_hive()

    def spawn_hive(self):
        assert self.world_size > self.hives_area
        self.hives.append(
            Hive(
                self.num_bees_per_hive,
                self.hives_area + np.random.rand() * (self.world_size - self.hives_area),
                self.hives_area + np.random.rand() * (self.world_size - self.hives_area),
                area_size=self.hives_area
            )
        )

    def simulate(self, num_iterations):
        for i in range(num_iterations):
            for hive in self.hives:
                hive.simulate()
            self.plot()

    def plot(self):
        x_hives = []
        y_hives = []
        x_food_sources = []
        y_food_sources = []
        x_bees = []
        y_bees = []
        for hive in self.hives:
            x_hives.append(hive.x)
            x_bees = hive.get_bees_x_positions()
            y_hives.append(hive.y)
            y_bees = hive.get_bees_y_positions()
        for food_source in self.food_sources:
            x_food_sources.append(food_source.x)
            y_food_sources.append(food_source.y)
        plt.scatter(x_bees, y_bees, c='b', label='Bees')
        plt.scatter(x_food_sources, y_food_sources, c='g', label='Food Sources')
        plt.scatter(x_hives, y_hives, c='r', label="Hive")
        plt.legend()
        plt.show()
        pass
