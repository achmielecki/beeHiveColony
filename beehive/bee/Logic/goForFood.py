import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from beehive.constVariables import *


class GoForFood:
    def __init__(self):
        self.fuzzy_inputs = {
            'food_distance': None,
            'food_quantity': None,
        }
        self.fuzzy_outputs = {
            'dance_intensity': None
        }

        # Food quantity: low, average, high
        self.food_distance = ctrl.Antecedent(np.arange(0, world_size, 1), 'food_distance')
        self.food_distance.automf(3, variable_type='quant')

        # Food quantity: low, average, high
        self.food_quantity = ctrl.Antecedent(np.arange(0, max_count_of_flowers_in_one_place, 1), 'food_quantity')
        self.food_quantity.automf(3, variable_type='quant')

        self.dance_intensity = ctrl.Consequent(np.arange(0, 1, 0.1), 'dance_intensity')
        self.dance_intensity["low"] = fuzz.trimf(self.dance_intensity.universe, [0, 0, 1/2])
        self.dance_intensity["average"] = fuzz.trimf(self.dance_intensity.universe, [0, 1/2, 1])
        self.dance_intensity["high"] = fuzz.trimf(self.dance_intensity.universe, [1/2, 1, 1])

        self.rule1 = ctrl.Rule(self.food_distance['high'] & self.food_quantity['low'], self.dance_intensity["low"])
        self.rule2 = ctrl.Rule(self.food_distance['high'] & self.food_quantity['average'], self.dance_intensity["low"])
        self.rule3 = ctrl.Rule(self.food_distance['high'] & self.food_quantity['high'], self.dance_intensity["average"])
        self.rule4 = ctrl.Rule(self.food_distance['average'] & self.food_quantity['low'], self.dance_intensity["low"])
        self.rule5 = ctrl.Rule(self.food_distance['average'] & self.food_quantity['average'], self.dance_intensity["average"])
        self.rule6 = ctrl.Rule(self.food_distance['average'] & self.food_quantity['high'], self.dance_intensity["high"])
        self.rule7 = ctrl.Rule(self.food_distance['low'] & self.food_quantity['low'], self.dance_intensity["average"])
        self.rule8 = ctrl.Rule(self.food_distance['low'] & self.food_quantity['average'], self.dance_intensity["high"])
        self.rule9 = ctrl.Rule(self.food_distance['low'] & self.food_quantity['high'], self.dance_intensity["high"])

        self.dance_ctrl = ctrl.ControlSystem([self.rule1, self.rule2, self.rule3,
                                              self.rule4, self.rule5, self.rule6,
                                              self.rule7, self.rule8, self.rule9])
        self.dance_ctrl_sim = ctrl.ControlSystemSimulation(self.dance_ctrl)

    def set_dance_intensity(self, distance_from_hive, current_amount):
        self.dance_ctrl_sim.input['food_distance'] = distance_from_hive
        self.dance_ctrl_sim.input['food_quantity'] = current_amount

        self.dance_ctrl_sim.compute()

        return self.dance_ctrl_sim.output['dance_intensity']

