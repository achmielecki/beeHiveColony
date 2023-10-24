import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

bee_max_speed = 8.2  # m/s
bee_min_speed = 4.9  # m/s
bee_max_range_for_water = 3000  # m
bee_max_range_for_pollen = 6000  # m
bee_max_range_for_nectar = 12000  # m
max_life_time = 10  # days
min_life_time = 5  # days


class BeeFuzzyBehaviour:

    def __init__(self, bee):
        self.max_speed = 8.2
        self.movement_from_hive_radius = 12000
        self.bee = bee
        self.bee.vx = 0.0
        self.bee.vy = 0.0
        self.fuzzy_inputs = {
            'food_distance': None,
            'food_quantity': None,
            'bee_distance': None,
            'bee_alignment': None,
            'bee_cohesion': None
        }
        self.fuzzy_outputs = {
            'move_direction': None,
            'move_speed': None
        }
        # Food distance: Low, average, high
        self.food_distance = ctrl.Antecedent(np.arange(0, self.movement_from_hive_radius, 1), 'food_distance')
        self.food_distance.automf(5, variable_type='quant')
        # Food quantity: Low, average, high
        self.food_quantity = ctrl.Antecedent(np.arange(0, 10, 1), 'food_quantity')
        self.food_quantity.automf(3, variable_type='quant')
        # Bee distance: Close, medium, far
        # Bee alignment: Poor, good
        # Bee cohesion: Poor, good
        # Move direction: Towards, away
        # Move speed: stop, slow, fast
        self.move_speed = ctrl.Consequent(np.arange(0, self.max_speed, 1), 'move_speed')
        self.move_speed["stop"] = fuzz.trimf(self.move_speed.universe, [0, 0, self.max_speed * (4 / 9)])
        self.move_speed["slow"] = fuzz.trimf(self.move_speed.universe, [1, self.max_speed / 2, self.max_speed])
        self.move_speed["fast"] = fuzz.trimf(self.move_speed.universe,
                                             [self.max_speed * (2 / 3), self.max_speed, self.max_speed])
        # If food distance is close and food quantity is high, move towards the food source at a fast speed.
        self.rule1 = ctrl.Rule(self.food_distance['lower'], self.move_speed["stop"])
        self.rule2 = ctrl.Rule(self.food_distance['low'], self.move_speed["slow"])
        self.rule3 = ctrl.Rule(self.food_distance['average'] & self.food_quantity['high'], self.move_speed["slow"])
        # If food distance is high or food quantity is low, stop.
        self.rule4 = ctrl.Rule(self.food_distance['high'], self.move_speed["fast"])
        self.rule5 = ctrl.Rule(self.food_distance['higher'], self.move_speed["fast"])
        # self.rule3 = ctrl.Rule(self.food_distance['low'], self.move_speed["stop"])
        # If food distance is medium and food quantity is medium, move towards the food source at a medium speed.
        # If bee distance is close and bee alignment is good and bee cohesion is good, move towards the other bee at a slow speed.
        # If bee distance is close and bee alignment is poor and bee cohesion is poor is low, move away from the other bee at a fast speed.
        # If bee distance is medium, move randomly.
        self.move_speed_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3, self.rule4, self.rule5])
        self.move_speed_ctrl_sim = ctrl.ControlSystemSimulation(self.move_speed_ctrl)

        self.hive_distance = ctrl.Antecedent(np.arange(0, self.movement_from_hive_radius, 1), 'hive_distance')
        self.hive_distance.automf(5, variable_type='quant')
        self.back_rule1 = ctrl.Rule(self.hive_distance['lower'], self.move_speed["stop"])
        self.back_rule2 = ctrl.Rule(self.hive_distance['low'], self.move_speed["slow"])
        self.back_rule3 = ctrl.Rule(self.hive_distance['average'], self.move_speed["slow"])
        self.back_rule4 = ctrl.Rule(self.hive_distance['high'], self.move_speed["fast"])
        self.back_rule5 = ctrl.Rule(self.hive_distance['higher'], self.move_speed["fast"])
        self.back_move_speed_ctrl = ctrl.ControlSystem(
            [self.back_rule1, self.back_rule2, self.back_rule3, self.back_rule4, self.back_rule5])
        self.back_move_speed_ctrl_sim = ctrl.ControlSystemSimulation(self.back_move_speed_ctrl)

        self.nearest_food_distance = None
        self.nearest_food = None

        self.hive_distance_value = np.sqrt((self.bee.x - self.bee.hive.x) ** 2 + (self.bee.y - self.bee.hive.y) ** 2)

    def act(self):
        if self.bee.carried_food == 0:
            self.go_for_food()
        else:
            self.move_food_back_to_hive()
        pass

    def go_for_food(self):
        self.update_nearest_food()
        outputs = self.go_to_food()
        # Update the bee's position and velocity based on the fuzzy outputs
        self.update_position_and_velocity(self.nearest_food, outputs['move_speed'])
        if self.nearest_food_distance < 2:
            self.extract_food(self.nearest_food)

    def update_nearest_food(self):
        self.nearest_food_distance, self.nearest_food = self.get_nearest_food()

    def get_nearest_food(self):
        food_distances = [(np.sqrt((food.x - self.bee.x) ** 2 + (food.y - self.bee.y) ** 2), food) for food in
                          self.bee.hive.get_food_sources()]
        food_distances = [x for x in food_distances if x[1].get_amount() > 3]
        # todo what if no food
        return min(food_distances, key=lambda t: t[0])

    def go_to_food(self):
        self.update_food_searching_fuzzy_inputs(self.bee.x, self.bee.y, self.nearest_food_distance, self.nearest_food.current_amount)
        self.determine_food_searching_fuzzy_outputs()
        return self.fuzzy_outputs

    def move_food_back_to_hive(self):
        outputs = self.go_to_hive()
        self.update_position_and_velocity(self.bee.hive, outputs["move_speed"])
        if self.distance_to_hive() < 2:
            self.bee.leave_food_in_hive()

    def go_to_hive(self):
        self.update_hive_searching_fuzzy_inputs()
        self.determine_hive_searching_fuzzy_outputs()
        return self.fuzzy_outputs

    def update_hive_searching_fuzzy_inputs(self):
        self.fuzzy_inputs['hive_distance'] = self.bee.distance_to_hive()

    def determine_hive_searching_fuzzy_outputs(self):
        self.back_move_speed_ctrl_sim.input["hive_distance"] = self.fuzzy_inputs['hive_distance']
        self.back_move_speed_ctrl_sim.compute()

        self.fuzzy_outputs['move_direction'] = 1
        self.fuzzy_outputs['move_speed'] = self.back_move_speed_ctrl_sim.output["move_speed"]

    def update_food_searching_fuzzy_inputs(self, x, y, nearest_food_distance, nearest_food_amount):
        # Implement fuzzy input updates based on sensory inputs

        # Determine the distance to the nearest food source
        self.fuzzy_inputs['food_distance'] = nearest_food_distance

        # Determine the amount of the nearest food source
        self.fuzzy_inputs['food_quantity'] = nearest_food_amount

        # Get neighboring bees within sight radius
        neighboring_bees = []
        for bee in self.bee.hive.bees:
            if bee != self:
                distance_to_bee = np.sqrt((self.bee.x - bee.x) ** 2 + (self.bee.y - bee.y) ** 2)
                if distance_to_bee <= self.movement_from_hive_radius:
                    neighboring_bees.append(bee)

        # Calculate distance to each neighboring bee and update fuzzy input
        distances = [np.sqrt((self.bee.x - bee.x) ** 2 + (self.bee.y - bee.y) ** 2) for bee in neighboring_bees]
        self.fuzzy_inputs['bee_distance'] = np.mean(distances)

        # Calculate membership value in each fuzzy set for bee separation
        bee_distances = []
        for bee in self.bee.hive.bees:
            if bee != self:
                bee_distance = np.sqrt((self.bee.x - bee.x) ** 2 + (self.bee.y - bee.y) ** 2)
                bee_distances.append(bee_distance)
        # print(self.fuzzy_inputs)

    def determine_food_searching_fuzzy_outputs(self):
        # todo implement
        self.move_speed_ctrl_sim.input["food_distance"] = self.fuzzy_inputs['food_distance']
        self.move_speed_ctrl_sim.input["food_quantity"] = self.fuzzy_inputs['food_quantity']
        self.move_speed_ctrl_sim.compute()

        self.fuzzy_outputs['move_direction'] = 1
        self.fuzzy_outputs['move_speed'] = self.move_speed_ctrl_sim.output["move_speed"]

    def update_position_and_velocity(self, object, move_speed):
        fx, fy = object.get_pos()

        dx = self.bee.x - fx
        dy = self.bee.y - fy

        if dx < 0:
            xdir = 1
        else:
            xdir = -1

        if dy < 0:
            ydir = 1
        else:
            ydir = -1

        self.bee.x += xdir * move_speed
        self.bee.y += ydir * move_speed

        # Limit movement range to sight radius
        if self.hive_distance_value > self.movement_from_hive_radius:
            self.bee.x = self.bee.hive.x + self.movement_from_hive_radius * (self.bee.x - self.bee.hive.x) / self.hive_distance_value
            self.bee.y = self.bee.hive.y + self.movement_from_hive_radius * (self.bee.y - self.bee.hive.y) / self.hive_distance_value

        # Update velocity based on new position
        self.bee.vx = self.bee.x - self.bee.hive.x
        self.bee.vy = self.bee.y - self.bee.hive.y

        # Limit speed to max speed
        speed = np.sqrt(self.bee.vx ** 2 + self.bee.vy ** 2)
        if speed > self.max_speed:
            self.bee.vx *= self.max_speed / speed
            self.bee.vy *= self.max_speed / speed
            
    def distance_to_hive(self) -> float:
        return np.sqrt((self.bee.x - self.bee.hive.x) ** 2 + (self.bee.y - self.bee.hive.y) ** 2)
