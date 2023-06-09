import numpy as np


class FoodSource:
    def __init__(self, x, y, max_amount=10):
        self.x = x
        self.y = y
        self.max_amount = max_amount
        self.current_amount = np.random.rand() * max_amount

    def get_pos(self):
        return self.x, self.y

    def get_amount(self):
        return self.current_amount

    def update_amount(self, amount):
        self.current_amount -= amount
        if self.current_amount < 0:
            self.current_amount = 0
