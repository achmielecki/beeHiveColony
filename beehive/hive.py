import datetime

import numpy as np

from beehive.model_of_competition.model import ModelOfCompetition
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
        self.food_stored = 0
        self.world = world
        self.num_bees = num_bees
        self.x = x
        self.y = y
        self.area_size = area_size
        self.bees = []
        self.spawn_initial_bees(num_bees)
        self.nectar_stored = 0
        self.current_dances = []
        self.current_scouts = 0
        self.max_scouts = self.num_bees * 0.1
        self.nectar_goal = 0
        self.dead_bees = 0

    def spawn_initial_bees(self, num_bees):
        for i in range(num_bees):
            self.spawn_bee()

    def get_current_dances(self):
        return self.current_dances

    def spawn_bee(self):
        self.bees.append(
            Bee(
                self,
                self.x + np.random.rand() * self.area_size,
                self.y + np.random.rand() * self.area_size,
                self.world.get_time() - datetime.timedelta(seconds=(3110400 * np.random.rand()))
            )
        )

    def leave_nectar(self, count):
        self.nectar_stored += count

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

    def remove_dead_bee(self, bee):
        self.bees.remove(next((x for x in self.bees if x.id == bee.id), None))
        self.dead_bees += 1

    def simulate(self, is_new_day=False):
        if is_new_day:
            self.get_new_nectar_goal()
        for bee in self.bees:
            bee.act()

    def get_new_nectar_goal(self):
        model = ModelOfCompetition(
            [self.world.get_temp(), self.world.get_tommorow_temp()],
            [self.world.get_rainfall(), self.world.get_tomorrow_rainfall()],
            len(self.bees) * 10,
            1
        )
        model.simulation(False)
        self.nectar_goal = model.get_foraged_nectar()
