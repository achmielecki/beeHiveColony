import datetime
from enum import Enum
import beehive.bee.Logic.goForFood as gff
import numpy as np
import math
from beehive.constVariables import *

dance_intensity_model = gff.GoForFood()

# https://en.wikipedia.org/wiki/Artificial_bee_colony_algorithm
class ArtificialBeeColonyBehaviour:
    def __init__(self, bee):
        self.is_dancing = False
        self.spotted_food = None
        self.overall_food_quality = None
        self.distance_to_hive = None
        self.speed = bee_min_speed + ((bee_max_speed - bee_min_speed) * np.random.rand())
        self.my_food_source = None
        self.bee = bee
        self.role = self.init_role()
        self.carried_nectar = 0
        self.max_carry = bee_nectar_max_carry
        self.scout_steps = 0
        self.current_direction = 1  # angle in radians
        self.acked_onlookers = 0
        self.dance_intensity = dance_intensity_model

    def init_role(self):
        if np.random.rand() < 0.8:
            return Role(4)
        else:
            return Role(2)

    def act(self):
        if self.is_too_old():
            self.die()
        match self.role:
            case Role.employed:
                self.harvest_your_food_source()
            case Role.onlooker:
                self.onlook()
            case Role.scout:
                self.scout()

    def is_too_old(self):
        return self.bee.get_age() > datetime.timedelta(days=36) - (0.5 - np.random.rand()) * datetime.timedelta(
            hours=48)

    def die(self):
        self.bee.hive.remove_dead_bee(self.bee)

    def onlook(self):
        self.stay_around_hive()
        if self.is_around_hive() and self.are_there_any_dances():
            self.get_employed_at_best_food_source()
        else:
            if self.should_become_scout():
                self.become_scout()

    def get_employed_at_best_food_source(self):
        self.my_food_source = self.choose_best_dance()
        self.role = Role.employed

    def should_become_scout(self):
        return np.random.rand() < self.chance_of_becoming_scout()

    def chance_of_becoming_scout(self):
        if self.bee.hive.current_scouts >= self.bee.hive.max_scouts:
            return 0
        if self.bee.hive.world.is_it_dark():
            return 0
        return chance_of_becoming_scout

    def become_scout(self):
        self.bee.hive.current_scouts += 1
        self.role = Role.scout

    def stay_around_hive(self):
        self.update_distance_to_hive()
        if self.is_around_hive():
            self.float_around_hive()
        else:
            self.go_to_hive()

    def is_around_hive(self):
        return self.distance_to_hive < 0.05

    def update_distance_to_hive(self):
        self.distance_to_hive = self.get_distance(self.bee.x, self.bee.y, self.bee.hive.x, self.bee.hive.y)

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

    def are_there_any_dances(self):
        return self.bee.hive.get_current_dances()

    def choose_best_dance(self):
        dances = self.bee.hive.get_current_dances()
        dance = list(sorted(dances, key=lambda it: it[2]))[-1]
        dance[0].ack_onlooker()
        return dance[1]

    def ack_onlooker(self):
        self.acked_onlookers += 1
        if self.acked_onlookers >= (self.spotted_food.current_amount / self.max_carry) - 1:
            self.role = Role.employed
            self.bee.hive.current_dances.remove((self, self.spotted_food, self.overall_food_quality))
            self.my_food_source = self.spotted_food
            self.spotted_food = None
            self.bee.hive.current_scouts -= 1
            self.acked_onlookers = 0
            self.is_dancing = False

    def harvest_your_food_source(self):
        if self.should_leave_nectar_in_hive():
            self.update_distance_to_hive()
            if not self.is_around_hive():
                self.go_to_hive()
            else:
                self.leave_food_in_hive()
            return
        if self.my_food_source is None:
            self.role = Role(2)
        else:
            if self.distance_to_your_food() > 0.05:
                self.go_to_your_food_source()
            else:
                self.harvest()
                if self.my_food_is_not_efficient_anymore():
                    self.abandon_my_food_source()

    def should_leave_nectar_in_hive(self):
        return self.carried_nectar > self.max_carry * 0.8 or (self.carried_nectar > 0 and self.my_food_source is None)

    def distance_to_your_food(self) -> float:
        return np.sqrt((self.my_food_source.x - self.bee.x) ** 2 + (self.my_food_source.y - self.bee.y) ** 2)

    def go_to_your_food_source(self):
        self.go_towards_object(self.my_food_source)

    def harvest(self):
        amount_that_can_be_harvested = min(self.max_carry / 4, self.max_carry - self.carried_nectar)
        self.carried_nectar = self.my_food_source.extract_food(amount_that_can_be_harvested)

    def my_food_is_not_efficient_anymore(self):
        return self.my_food_source.current_amount < self.max_carry

    def abandon_my_food_source(self):
        self.my_food_source = None

    def leave_food_in_hive(self):
        self.bee.hive.leave_nectar(self.carried_nectar)
        self.carried_nectar = 0

    def scout(self):
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

    def spot_food(self):
        foods = self.bee.hive.world.get_food_in_range(self.bee.x, self.bee.y, bee_sight_range)
        foods = list(filter(lambda it: it.current_amount > flower_max_nectar_carry and it.discovered is False, foods))
        if foods:
            foods[0].spot()
            return foods[0]
        return None

    def dance(self):
        self.is_dancing = True
        food_distance_from_hive = self.get_distance(self.bee.hive.x, self.spotted_food.x,
                                                    self.bee.hive.y, self.spotted_food.y)
        self.overall_food_quality = self.dance_intensity.set_dance_intensity(
            food_distance_from_hive, self.spotted_food.count_of_flowers)
        self.bee.hive.current_dances.append((self, self.spotted_food, self.overall_food_quality))

    def random_direction(self):
        self.current_direction = math.pi * 2 * np.random.rand()

    def go_towards_direction(self, direction, speed):
        self.bee.x += math.cos(direction) * speed
        self.bee.y += math.sin(direction) * speed

    def get_distance(self, x1, y1, x2, y2) -> float:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Role(Enum):
    employed = 1
    onlooker = 2
    scout = 3
    employed_in_hive = 4
