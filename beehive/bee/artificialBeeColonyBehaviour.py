from enum import Enum
import numpy as np
import math

bee_max_speed = 8.2  # m/s
bee_min_speed = 4.9  # m/s
max_life_time = 10  # days
min_life_time = 5  # days
bee_nectar_max_carry = 0.06  # grams https://ucanr.edu/blogs/blogcore/postdetail.cfm?postnum=43385
bee_sight_range = 5  # m
chance_of_becoming_scout = 0.001
flower_max_nectar_carry = 0.007
jiggle_effect_base_strength = 0.6


# https://en.wikipedia.org/wiki/Artificial_bee_colony_algorithm
class ArtificialBeeColonyBehaviour:
    def __init__(self, bee):
        self.is_dancing = False
        self.spotted_food = None
        self.distance_to_hive = None
        self.speed = bee_min_speed + ((bee_max_speed - bee_min_speed) * np.random.rand())
        self.my_food_source = None
        self.bee = bee
        self.role = self.init_role()
        self.carried_nectar = 0
        self.max_carry = bee_nectar_max_carry
        self.scout_steps = 0
        self.current_direction = 1 #angle in radians
        self.acked_onlookers = 0

    def init_role(self):
        if np.random.rand() < 0.8:
            return Role(4)
        else:
            return Role(2)

    def act(self):
        match self.role:
            case Role.employed:
                self.harvest_your_food_source()
            case Role.onlooker:
                self.onlook()
            case Role.scout:
                self.scout()
            case Role.employed_in_hive:
                pass

    def onlook(self):
        self.stay_around_hive()
        if self.is_around_hive() and self.are_there_any_dances():
            self.my_food_source = self.choose_best_dance()
            self.role = Role.employed
        else:
            if np.random.rand() < chance_of_becoming_scout:
                if self.bee.hive.current_scouts < self.bee.hive.max_scouts:
                    self.bee.hive.current_scouts += 1
                    self.role = Role.scout

    def stay_around_hive(self):
        self.update_distance_to_hive()
        if self.is_around_hive():
            self.float_around_hive()
        else:
            self.go_to_hive()

    def is_around_hive(self):
        return self.distance_to_hive < 0.5

    def update_distance_to_hive(self):
        self.distance_to_hive = self.calculate_distance_to_hive()

    def calculate_distance_to_hive(self) -> float:
        return np.sqrt((self.bee.x - self.bee.hive.x) ** 2 + (self.bee.y - self.bee.hive.y) ** 2)

    def go_to_hive(self):
        self.go_towards_object(self.bee.hive)

    def go_towards_object(self, object):
        fx, fy = object.get_pos()
        dx = fx - self.bee.x
        dy = fy - self.bee.y
        jiggle_effect_strength = np.random.rand() - 0.5
        angle_radians = math.atan2(dy, dx) + (jiggle_effect_base_strength * jiggle_effect_strength)
        distance = math.sqrt(dx*dx + dy*dy)
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
        dance = list(sorted(dances, key=lambda it: it[1].current_amount))[-1]
        dance[0].ack_onlooker()
        return dance[1]

    def ack_onlooker(self):
        self.acked_onlookers += 1
        if self.acked_onlookers >= self.spotted_food.count_of_flowers - 1:
            self.role = Role.employed
            self.bee.hive.current_dances.remove((self, self.spotted_food))
            self.my_food_source = self.spotted_food
            self.spotted_food = None
            self.bee.hive.current_scouts -= 1

    def harvest_your_food_source(self):
        if self.carried_nectar > 0:
            self.update_distance_to_hive()
            if self.distance_to_hive > 0.05:
                self.go_to_hive()
            else:
                self.leave_food_in_hive()
        if self.my_food_source is None:
            self.role = Role(2)
        else:
            if self.carried_nectar == 0:
                if self.distance_to_your_food() > 0.05:
                    self.go_to_your_food_source()
                else:
                    self.harvest()
                    if self.my_food_is_not_efficient_anymore():
                        self.abandon_my_food_source()

    def distance_to_your_food(self) -> float:
        return np.sqrt((self.my_food_source.x - self.bee.x) ** 2 + (self.my_food_source.y - self.bee.y) ** 2)

    def go_to_your_food_source(self):
        self.go_towards_object(self.my_food_source)

    def harvest(self):
        self.carried_nectar = self.my_food_source.extract_food(self.max_carry)

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
            if self.distance_to_hive < 0.05:
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
        foods = list(filter(lambda it: it.current_amount > flower_max_nectar_carry, foods))
        if foods:
            foods[0].spot()
            return foods[0]
        return None

    def dance(self):
        self.is_dancing = True
        self.bee.hive.current_dances.append((self, self.spotted_food))

    def random_direction(self):
        self.current_direction = math.pi * 2 * np.random.rand()

    def go_towards_direction(self, direction, speed):
        self.bee.x += math.cos(direction) * speed
        self.bee.y += math.sin(direction) * speed


class Role(Enum):
    employed = 1
    onlooker = 2
    scout = 3
    employed_in_hive = 4
