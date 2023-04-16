import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz


class Bee:
    def __init__(self, hive,
                 world_size,
                 max_speed=3,
                 sight_radius=20):
        self.hive = hive
        self.max_speed = max_speed
        self.world_size = world_size
        self.sight_radius = sight_radius
        self.x = np.random.rand() * world_size
        self.y = np.random.rand() * world_size
        self.vx = 0.0
        self.vy = 0.0
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
        self.food_distance = ctrl.Antecedent(np.arange(0, 25, 1), 'food_distance')
        self.food_distance.automf(3, variable_type='quant')
        # Food quantity: Low, average, high
        self.food_quantity = ctrl.Antecedent(np.arange(0, 10, 1), 'food_quantity')
        self.food_quantity.automf(3, variable_type='quant')
        # Bee distance: Close, medium, far
        # Bee alignment: Poor, good
        # Bee cohesion: Poor, good
        # Move direction: Towards, away
        # Move speed: stop, slow, fast
        self.move_speed = ctrl.Consequent(np.arange(0, 4, 1), 'move_speed')
        self.move_speed["stop"] = fuzz.trimf(self.move_speed.universe, [0, 0, 1])
        self.move_speed["slow"] = fuzz.trimf(self.move_speed.universe, [1, 2, 3])
        self.move_speed["fast"] = fuzz.trimf(self.move_speed.universe, [2, 3, 3])
        # If food distance is close and food quantity is high, move towards the food source at a fast speed.
        self.rule1 = ctrl.Rule(self.food_distance['low'] & self.food_quantity['high'], self.move_speed["fast"])
        # If food distance is high or food quantity is low, stop.
        self.rule2 = ctrl.Rule(self.food_distance['high'] | self.food_quantity['low'], self.move_speed["stop"])
        # If food distance is medium and food quantity is medium, move towards the food source at a medium speed.
        # If bee distance is close and bee alignment is good and bee cohesion is good, move towards the other bee at a slow speed.
        # If bee distance is close and bee alignment is poor and bee cohesion is poor is low, move away from the other bee at a fast speed.
        # If bee distance is medium, move randomly.
        self.move_speed_ctrl = ctrl.ControlSystem([self.rule1, self.rule2])
        self.move_speed_ctrl_sim = ctrl.ControlSystemSimulation(self.move_speed_ctrl)

    def act(self):
        # Update the fuzzy inputs
        self.update_fuzzy_inputs()

        # Determine the fuzzy outputs
        self.determine_fuzzy_outputs()

        # Update the bee's position and velocity based on the fuzzy outputs
        self.update_position_and_velocity()
        pass

    def update_fuzzy_inputs(self):
        # Implement fuzzy input updates based on sensory inputs

        # Determine the distance to the nearest food source
        nearest_food_distance, nearest_food = self.get_nearest_food()
        self.fuzzy_inputs['food_distance'] = nearest_food_distance

        # Determine the amount of the nearest food source
        self.fuzzy_inputs['food_quantity'] = nearest_food.get_amount()

        # Fuzzify bee alignment
        bee_angles = np.arctan2(self.y - np.array([bee.y for bee in self.hive.bees]),
                                self.x - np.array([bee.x for bee in self.hive.bees]))
        avg_bee_angle = np.arctan2(np.mean(np.sin(bee_angles)), np.mean(np.cos(bee_angles)))
        self.fuzzy_inputs['bee_alignment'] = avg_bee_angle

        # Fuzzify bee cohesion
        mean_x = np.mean([bee.x for bee in self.hive.bees])
        mean_y = np.mean([bee.y for bee in self.hive.bees])
        self.fuzzy_inputs['bee_cohesion'] = np.arctan2(mean_y - self.y, mean_x - self.x)

        # Get neighboring bees within sight radius
        neighboring_bees = []
        for bee in self.hive.bees:
            if bee != self:
                distance_to_bee = np.sqrt((self.x - bee.x) ** 2 + (self.y - bee.y) ** 2)
                if distance_to_bee <= self.sight_radius:
                    neighboring_bees.append(bee)

        # Calculate distance to each neighboring bee and update fuzzy input
        distances = [np.sqrt((self.x - bee.x) ** 2 + (self.y - bee.y) ** 2) for bee in neighboring_bees]
        self.fuzzy_inputs['bee_distance'] = np.mean(distances)

        # Calculate membership value in each fuzzy set for bee separation
        bee_distances = []
        for bee in self.hive.bees:
            if bee != self:
                bee_distance = np.sqrt((self.x - bee.x) ** 2 + (self.y - bee.y) ** 2)
                bee_distances.append(bee_distance)

        #print(self.fuzzy_inputs)

    def get_nearest_food(self):
        food_distances = [(np.sqrt((food.x - self.x) ** 2 + (food.y - self.y) ** 2), food) for food in
                          self.hive.food_sources]
        return min(food_distances, key=lambda t: t[0])

    def determine_fuzzy_outputs(self):
        # todo implement
        self.move_speed_ctrl_sim.input["food_distance"] = self.fuzzy_inputs['food_distance']
        self.move_speed_ctrl_sim.input["food_quantity"] = self.fuzzy_inputs['food_quantity']
        self.move_speed_ctrl_sim.compute()

        self.fuzzy_outputs['move_direction'] = 1
        self.fuzzy_outputs['move_speed'] = self.move_speed_ctrl_sim.output["move_speed"]

    def update_position_and_velocity(self):
        nearest_food_distance, nearest_food = self.get_nearest_food()

        fx, fy = nearest_food.get_pos()

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

        self.x += xdir * self.fuzzy_outputs['move_speed']
        self.y += ydir * self.fuzzy_outputs['move_speed']

        # Limit movement range to sight radius
        distance_to_hive = np.sqrt((self.x - self.hive.x) ** 2 + (self.y - self.hive.y) ** 2)
        if distance_to_hive > self.sight_radius:
            self.x = self.hive.x + self.sight_radius * (self.x - self.hive.x) / distance_to_hive
            self.y = self.hive.y + self.sight_radius * (self.y - self.hive.y) / distance_to_hive

        # Update velocity based on new position
        self.vx = self.x - self.hive.x
        self.vy = self.y - self.hive.y

        # Limit speed to max speed
        speed = np.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > self.max_speed:
            self.vx *= self.max_speed / speed
            self.vy *= self.max_speed / speed
