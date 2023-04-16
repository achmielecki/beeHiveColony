import numpy as np


class FoodSource:
    def __init__(self, max_amount = 1):
        self.x = np.random.rand()
        self.y = np.random.rand()
        self.max_amount = max_amount
        self.current_amount = max_amount
        self.fuzzy_inputs = {
            'food_distance': None,
            'food_amount': None,
        }

    def get_amount(self):
        return self.current_amount

    def update_amount(self, amount):
        self.current_amount -= amount
        if self.current_amount < 0:
            self.current_amount = 0

