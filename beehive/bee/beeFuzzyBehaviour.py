import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class BeeFuzzyBehaviour:

    def __init__(self, bee):
        self.bee = bee
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
        self.food_distance = ctrl.Antecedent(np.arange(0, self.bee.sight_radius, 1), 'food_distance')
        self.food_distance.automf(5, variable_type='quant')
        # Food quantity: Low, average, high
        self.food_quantity = ctrl.Antecedent(np.arange(0, 10, 1), 'food_quantity')
        self.food_quantity.automf(3, variable_type='quant')
        # Bee distance: Close, medium, far
        # Bee alignment: Poor, good
        # Bee cohesion: Poor, good
        # Move direction: Towards, away
        # Move speed: stop, slow, fast
        self.move_speed = ctrl.Consequent(np.arange(0, self.bee.max_speed, 1), 'move_speed')
        self.move_speed["stop"] = fuzz.trimf(self.move_speed.universe, [0, 0, self.bee.max_speed * (4 / 9)])
        self.move_speed["slow"] = fuzz.trimf(self.move_speed.universe, [1, self.bee.max_speed / 2, self.bee.max_speed])
        self.move_speed["fast"] = fuzz.trimf(self.move_speed.universe, [self.bee.max_speed * (2 / 3), self.bee.max_speed, self.bee.max_speed])
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

        self.hive_distance = ctrl.Antecedent(np.arange(0, self.bee.sight_radius, 1), 'hive_distance')
        self.hive_distance.automf(5, variable_type='quant')
        self.back_rule1 = ctrl.Rule(self.hive_distance['lower'], self.move_speed["stop"])
        self.back_rule2 = ctrl.Rule(self.hive_distance['low'], self.move_speed["slow"])
        self.back_rule3 = ctrl.Rule(self.hive_distance['average'], self.move_speed["slow"])
        self.back_rule4 = ctrl.Rule(self.hive_distance['high'], self.move_speed["fast"])
        self.back_rule5 = ctrl.Rule(self.hive_distance['higher'], self.move_speed["fast"])
        self.back_move_speed_ctrl = ctrl.ControlSystem(
            [self.back_rule1, self.back_rule2, self.back_rule3, self.back_rule4, self.back_rule5])
        self.back_move_speed_ctrl_sim = ctrl.ControlSystemSimulation(self.back_move_speed_ctrl)

    def go_for_food(self):
        self.update_food_searching_fuzzy_inputs()
        self.determine_food_searching_fuzzy_outputs()
        return self.fuzzy_outputs

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

    def update_food_searching_fuzzy_inputs(self):
        # Implement fuzzy input updates based on sensory inputs

        # Determine the distance to the nearest food source
        self.fuzzy_inputs['food_distance'] = self.bee.nearest_food_distance

        # Determine the amount of the nearest food source
        self.fuzzy_inputs['food_quantity'] = self.bee.nearest_food.get_amount()

        # Fuzzify bee alignment
        bee_angles = np.arctan2(self.bee.y - np.array([bee.y for bee in self.bee.hive.bees]),
                                self.bee.x - np.array([bee.x for bee in self.bee.hive.bees]))
        avg_bee_angle = np.arctan2(np.mean(np.sin(bee_angles)), np.mean(np.cos(bee_angles)))
        self.fuzzy_inputs['bee_alignment'] = avg_bee_angle

        # Fuzzify bee cohesion
        mean_x = np.mean([bee.x for bee in self.bee.hive.bees])
        mean_y = np.mean([bee.y for bee in self.bee.hive.bees])
        self.fuzzy_inputs['bee_cohesion'] = np.arctan2(mean_y - self.bee.y, mean_x - self.bee.x)

        # Get neighboring bees within sight radius
        neighboring_bees = []
        for bee in self.bee.hive.bees:
            if bee != self:
                distance_to_bee = np.sqrt((self.bee.x - bee.x) ** 2 + (self.bee.y - bee.y) ** 2)
                if distance_to_bee <= self.bee.sight_radius:
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
        #todo implement
        self.move_speed_ctrl_sim.input["food_distance"] = self.fuzzy_inputs['food_distance']
        self.move_speed_ctrl_sim.input["food_quantity"] = self.fuzzy_inputs['food_quantity']
        self.move_speed_ctrl_sim.compute()

        self.fuzzy_outputs['move_direction'] = 1
        self.fuzzy_outputs['move_speed'] = self.move_speed_ctrl_sim.output["move_speed"]
