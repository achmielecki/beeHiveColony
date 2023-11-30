from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour
import numpy as np
import math
from beehive.constVariables import *


class Scout(ArtificialBeeColonyBehaviour):
    def __init__(self, bee):
        super().__init__(bee)
        self.bee = bee

    def act(self):
        if self.is_dancing:
            return
        if self.spotted_food:
            self.update_distance_to_hive()
            if self.is_around_hive():
                self.dance()
            else:
                self.go_to_hive()
            return
        spotted_food = self.spot_food()
        if spotted_food:
            self.spotted_food = spotted_food
            return
        if self.scout_steps * np.random.rand() > 10:
            self.random_direction()
            self.scout_steps = 0
        self.go_towards_direction(self.current_direction, self.speed)
        self.scout_steps += 1

    def dance(self):
        self.is_dancing = True
        food_distance_from_hive = self.get_distance(self.bee.hive.x, self.spotted_food.x,
                                                    self.bee.hive.y, self.spotted_food.y)
        self.overall_food_quality = self.dance_intensity.set_dance_intensity(
            food_distance_from_hive, self.spotted_food.count_of_flowers)
        self.bee.hive.current_dances.append((self, self.spotted_food, self.overall_food_quality))

    def spot_food(self):
        foods = self.bee.hive.world.get_food_in_range(self.bee.x, self.bee.y, bee_sight_range)
        foods = list(filter(lambda it: it.current_amount > flower_max_nectar_carry and it.discovered is False, foods))
        if foods:
            foods[0].spot()
            return foods[0]
        return None

    def random_direction(self):
        self.current_direction = math.pi * 2 * np.random.rand()
