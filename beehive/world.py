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
        self.time = datetime.datetime(2000, 5, 1)

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
                self.world_size / 2 + (self.world_size / 2 * (np.random.rand() - 0.5)),
                self.world_size / 2 + (self.world_size / 2 * (np.random.rand() - 0.5)),
                area_size=self.hives_area
            )
        )

    def simulate(self, num_iterations=1):
        if self.is_it_dark():
            self.time_goes_forward(600)
            return
        for i in range(num_iterations):
            for hive in self.hives:
                if self.is_it_beginning_of_the_day():
                    hive.simulate(True)
                else:
                    hive.simulate()
            for food in self.food_sources:
                food.simulate()
        self.time_goes_forward()

    def time_goes_forward(self, seconds=1):
        self.time += datetime.timedelta(seconds=seconds)
        if self.time.second == 0:
            self.print_stuff()

    def print_stuff(self):
        print("===================")
        print(self.time)
        for hive in self.hives:
            print("food: " + str(hive.nectar_stored))
            print("today prognosed food: " + str(hive.nectar_goal))
            print("difference: " + str(hive.nectar_stored - hive.nectar_goal))

    def get_temp(self):
        return 20

    def get_tommorow_temp(self):
        return 20

    def get_rainfall(self):
        return 0

    def get_tomorrow_rainfall(self):
        return 0

    def is_it_beginning_of_the_day(self):
        return self.time.second == 0 and self.time.hour == 5 and self.time.minute == 0

    def is_it_dark(self):
        return self.time.hour < 5 or self.time.hour > 20
