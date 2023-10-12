import numpy as np
from beehive.bee.beeFuzzyBehaviour import BeeFuzzyBehaviour

bee_max_speed = 8.2  # m/s
bee_min_speed = 4.9  # m/s
bee_max_range_for_water = 3000  # m
bee_max_range_for_pollen = 6000  # m
bee_max_range_for_nectar = 12000  # m
max_life_time = 10  # days
min_life_time = 5  # days


class Bee:
    def __init__(
            self,
            hive,
            x,
            y
    ):
        self.hive = hive
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.carried_food = 0
        self.max_carry = 3
        self.behaviour = BeeFuzzyBehaviour(self)

    def act(self):
        self.behaviour.act()

    def extract_food(self, food):
        self.carried_food = food.extract_food(self.max_carry)

    def leave_food_in_hive(self):
        self.hive.leave_food(self.carried_food)
        self.carried_food = 0

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

