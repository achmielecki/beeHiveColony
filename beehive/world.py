import matplotlib.pyplot as plt
import numpy as np
import datetime

from beehive.foodSource import FoodSource
from beehive.hive import Hive


def check_range(food, x, y, range):
    if x + range > food.x > x - range:
        if y + range > food.y > y - range:
            return True
    return False


class World:
    def __init__(
            self,
            num_hives,
            num_bees_per_hive,
            num_food_sources,
            world_size=2000,
            hives_area=15
    ):
        self.num_hives = num_hives
        self.num_bees_per_hive = num_bees_per_hive
        self.num_food_sources = num_food_sources
        self.world_size = world_size
        self.hives_area = hives_area
        self.hives = []
        self.food_sources = []
        self.spawn_hives(num_hives)
        self.spawn_food(num_food_sources, world_size)
        self.time = datetime.datetime(2000, 1, 1)

    def spawn_food(self, num_food_sources, world_size):
        for i in range(num_food_sources):
            x = np.random.rand() * world_size
            y = np.random.rand() * world_size
            while not self.distance_to_hives_is_ok(x, y):
                x = np.random.rand() * world_size
                y = np.random.rand() * world_size
            self.food_sources.append(FoodSource(x, y))

    def distance_to_hives_is_ok(self, x, y) -> float:
        for hive in self.hives:
            if np.sqrt((hive.x - hive.x) ** 2 + (x - y) ** 2) < 1:
                return False
        return True

    def get_food_sources(self):
        return self.food_sources

    def get_hives(self):
        return self.hives

    def get_size(self):
        return self.world_size

    def get_food_in_range(self, x, y, range):
        return list(filter(lambda it: check_range(it, x, y, range), self.food_sources))

    def spawn_hives(self, num_hives):
        for i in range(num_hives):
            self.spawn_hive()

    def spawn_hive(self):
        assert self.world_size > self.hives_area * 2
        self.hives.append(
            Hive(
                self,
                self.num_bees_per_hive,
                self.hives_area + np.random.rand() * (self.world_size - (self.hives_area * 2)),
                self.hives_area + np.random.rand() * (self.world_size - (self.hives_area * 2)),
                area_size=self.hives_area
            )
        )

    def simulate(self, num_iterations=1):
        for i in range(num_iterations):
            for hive in self.hives:
                hive.simulate()
            for food in self.food_sources:
                food.simulate()
        self.time_goes_forward()

    def time_goes_forward(self):
        self.time += datetime.timedelta(seconds=1)
        if self.time.second == 0:
            print(self.time)

    def get_temp(self):
        return 20

    def get_tommorow_temp(self):
        return 20

    def get_rainfall(self):
        return 0

    def get_tomorrow_rainfall(self):
        return 0

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
