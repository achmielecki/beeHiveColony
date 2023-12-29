from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour
import numpy as np
import math
from beehive.constVariables import *


class Scout(ArtificialBeeColonyBehaviour):
    def __init__(self, bee):
        super().__init__(bee)
        self.bee = bee

    def act(self):
        if self.bee.is_dancing:
            return
        if self.bee.spotted_food:
            self.update_distance_to_hive()
            if self.is_around_hive():
                self.dance()
            else:
                self.go_to_hive()
            return
        spotted_food = self.spot_food()
        if spotted_food:
            self.bee.spotted_food = spotted_food
            return
        if self.bee.scout_steps * np.random.rand() > 10:
            self.random_direction()
            self.bee.scout_steps = 0
        self.go_towards_direction(self.bee.current_direction, self.speed)
        self.bee.scout_steps += 1

    def dance(self):
        self.bee.is_dancing = True
        food_distance_from_hive = self.get_distance(self.bee.hive.x, self.bee.spotted_food.x,
                                                    self.bee.hive.y, self.bee.spotted_food.y)
        self.bee.overall_food_quality = self.bee.dance_intensity.set_dance_intensity(
            food_distance_from_hive, self.bee.spotted_food.count_of_flowers)
        self.bee.hive.current_dances.append((self, self.bee.spotted_food, self.bee.overall_food_quality))

    def spot_food(self):
        foods = self.bee.hive.world.get_food_in_range(self.bee.x, self.bee.y, bee_sight_range)
        foods = list(filter(lambda it: it.current_amount > flower_max_nectar_carry and it.discovered is False, foods))
        if foods:
            foods[0].spot()
            return foods[0]
        return None

    def random_direction(self):
        self.bee.current_direction = math.pi * 2 * np.random.rand()

    def ack_onlooker(self):
        self.bee.acked_onlookers += 1
        if self.bee.acked_onlookers >= (self.bee.spotted_food.current_amount / self.max_carry) - 1:
            self.bee.become_employed()
            self.bee.hive.current_dances.remove((self, self.bee.spotted_food, self.bee.overall_food_quality))
            self.bee.my_food_source = self.bee.spotted_food
            self.bee.spotted_food = None
            self.bee.hive.current_scouts -= 1
            self.bee.acked_onlookers = 0
            self.bee.is_dancing = False
