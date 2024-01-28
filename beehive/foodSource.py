import datetime

import numpy as np
from beehive.constVariables import *


class FoodSource:
    def __init__(
            self,
            x,
            y,
            spawn_rate=flower_nectar_respawn_rate
    ):
        self.count_of_flowers = max_count_of_flowers_in_one_place * np.random.rand()
        self.spawn_rate = spawn_rate
        self.x = x
        self.y = y
        self.max_amount = flower_max_nectar_carry * self.count_of_flowers
        self.current_amount = self.max_amount
        self.last_gathered = datetime.datetime.now()
        self.discovered = False

    def spot(self, current_time):
        self.discovered = True
        self.last_gathered = current_time

    def get_pos(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def simulate(self, current_time):
        self.respawn_nectar(current_time)

    def respawn_nectar(self, current_time):
        if self.discovered is True and current_time - self.last_gathered == datetime.timedelta(hours=forget_food_source_hours):
            self.discovered = False
        if self.current_amount < self.max_amount:
            self.current_amount += self.spawn_rate

    def has_nectar_for_at_least_two_bees(self):
        return self.current_amount > bee_nectar_max_carry * 2

    def extract_food(self, max):
        if self.current_amount > max:
            self.update_amount(max)
            return max
        else:
            self.update_amount(self.current_amount)
            return self.current_amount

    def get_amount(self):
        return self.current_amount

    def update_amount(self, amount):
        self.current_amount -= amount
        if self.current_amount < 0:
            self.current_amount = 0
