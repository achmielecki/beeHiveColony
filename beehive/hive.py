import numpy as np
import matplotlib.pyplot as plt
from beehive.bee import Bee
from beehive.foodSource import FoodSource


class Hive:
    def __init__(self, num_bees, num_food_sources, world_size):
        self.x = world_size/2
        self.y = world_size/2
        self.num_bees = num_bees
        self.num_food_sources = num_food_sources
        self.world_size = world_size
        self.bees = []
        for i in range(num_bees):
            bee = Bee(self, world_size)
            self.bees.append(bee)
        self.food_sources = []
        for i in range(num_food_sources):
            food_source = FoodSource()
            self.food_sources.append(food_source)

    def simulate(self, num_iterations):
        for i in range(num_iterations):
            for bee in self.bees:
                bee.act()
            self.plot()

    def plot(self):
        x_bees = []
        y_bees = []
        for bee in self.bees:
            x_bees.append(bee.x)
            y_bees.append(bee.y)
        x_food_sources = []
        y_food_sources = []
        for food_source in self.food_sources:
            x_food_sources.append(food_source.x)
            y_food_sources.append(food_source.y)
        plt.scatter(x_bees, y_bees, c='b', label='Bees')
        plt.scatter(x_food_sources, y_food_sources, c='g', label='Food Sources')
        plt.scatter(self.x, self.y, c='r', label="Hive")
        plt.legend()
        plt.show()
