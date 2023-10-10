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
            y,
            max_speed=bee_max_speed,
            sight_radius=20
    ):
        self.hive = hive
        self.max_speed = max_speed
        self.sight_radius = sight_radius
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.carried_food = 0
        self.max_carry = 3
        self.nearest_food_distance = None
        self.nearest_food = None
        self.hive_distance_value = np.sqrt((self.x - self.hive.x) ** 2 + (self.y - self.hive.y) ** 2)
        self.behaviour = BeeFuzzyBehaviour(self)

    def act(self):
        if self.carried_food == 0:
            self.go_for_food()
        else:
            self.move_food_back_to_hive()
        pass

    def go_for_food(self):
        self.update_nearest_food()
        outputs = self.behaviour.go_for_food()
        # Update the bee's position and velocity based on the fuzzy outputs
        self.update_position_and_velocity(self.nearest_food, outputs['move_speed'])
        if self.nearest_food_distance < 2:
            self.extract_food(self.nearest_food)

    def update_nearest_food(self):
        self.nearest_food_distance, self.nearest_food = self.get_nearest_food()

    def get_nearest_food(self):
        food_distances = [(np.sqrt((food.x - self.x) ** 2 + (food.y - self.y) ** 2), food) for food in
                          self.hive.get_food_sources()]
        food_distances = [x for x in food_distances if x[1].get_amount() > 3]
        # todo what if no food
        return min(food_distances, key=lambda t: t[0])

    def update_position_and_velocity(self, object, move_speed):
        fx, fy = object.get_pos()

        dx = self.x - fx
        dy = self.y - fy

        if dx < 0:
            xdir = 1
        else:
            xdir = -1

        if dy < 0:
            ydir = 1
        else:
            ydir = -1

        self.x += xdir * move_speed
        self.y += ydir * move_speed

        # Limit movement range to sight radius
        if self.hive_distance_value > self.sight_radius:
            self.x = self.hive.x + self.sight_radius * (self.x - self.hive.x) / self.hive_distance_value
            self.y = self.hive.y + self.sight_radius * (self.y - self.hive.y) / self.hive_distance_value

        # Update velocity based on new position
        self.vx = self.x - self.hive.x
        self.vy = self.y - self.hive.y

        # Limit speed to max speed
        speed = np.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > self.max_speed:
            self.vx *= self.max_speed / speed
            self.vy *= self.max_speed / speed

    def extract_food(self, food):
        self.carried_food = food.extract_food(self.max_carry)

    def move_food_back_to_hive(self):
        outputs = self.behaviour.go_to_hive()
        self.update_position_and_velocity(self.hive, outputs["move_speed"])
        if self.hive_distance_value < 2:
            self.leave_food_in_hive()

    def leave_food_in_hive(self):
        self.hive.leave_food(self.carried_food)
        self.carried_food = 0

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def distance_to_hive(self) -> float:
        return np.sqrt((self.x - self.hive.x) ** 2 + (self.y - self.hive.y) ** 2)
