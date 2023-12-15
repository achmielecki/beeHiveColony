import datetime
from enum import Enum
import beehive.bee.Logic.leaveHive as lh
import beehive.bee.Logic.goForFood as gff
import numpy as np
import math
from beehive.constVariables import *


# go_out_model = lh.LeaveHive()


# https://en.wikipedia.org/wiki/Artificial_bee_colony_algorithm
class ArtificialBeeColonyBehaviour:
    def __init__(self, bee):
        self.speed = bee_min_speed + ((bee_max_speed - bee_min_speed) * np.random.rand())
        self.bee = bee
        self.max_carry = bee_nectar_max_carry

    def is_too_old(self):
        return self.bee.get_age() > datetime.timedelta(days=max_life_time) - (0.5 - np.random.rand()) * datetime.timedelta(
            hours=max_life_time_deviation)

    def die(self):
        self.bee.hive.remove_dead_bee(self.bee)

    def stay_around_hive(self):
        self.update_distance_to_hive()
        if self.is_around_hive():
            self.float_around_hive()
        else:
            self.go_to_hive()

    def is_around_hive(self):
        return self.bee.distance_to_hive < 0.05

    def update_distance_to_hive(self):
        self.bee.distance_to_hive = self.get_distance(self.bee.x, self.bee.y, self.bee.hive.x, self.bee.hive.y)

    def go_to_hive(self):
        self.go_towards_object(self.bee.hive)

    def go_towards_object(self, object):
        fx, fy = object.get_pos()
        dx = fx - self.bee.x
        dy = fy - self.bee.y
        jiggle_effect_strength = np.random.rand() - 0.5
        angle_radians = math.atan2(dy, dx) + (jiggle_effect_base_strength * jiggle_effect_strength)
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > self.speed:
            self.go_towards_direction(angle_radians, self.speed)
        else:
            self.go_towards_direction(angle_radians, distance)

    def float_around_hive(self):
        pass

    def distance_to_your_food(self) -> float:
        return self.get_distance(self.bee.my_food_source.x, self.bee.my_food_source.y, self.bee.x, self.bee.y)

    def go_towards_direction(self, direction, speed):
        self.bee.x += math.cos(direction) * speed
        self.bee.y += math.sin(direction) * speed

    @staticmethod
    def get_distance(x1, y1, x2, y2) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Role(Enum):
    employed = 1
    onlooker = 2
    scout = 3
    employed_in_hive = 4
