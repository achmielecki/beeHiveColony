import numpy as np


class FoodSource:
    def __init__(self, x, y, max_amount=10, spawn_rate=0.03):
        self.spawn_rate = spawn_rate
        self.x = x
        self.y = y
        self.max_amount = max_amount
        self.current_amount = np.random.rand() * max_amount

    def get_pos(self):
        return self.x, self.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def simulate(self):
        self.current_amount += self.spawn_rate

    def extract_food(self, max):
        if self.current_amount > max:
            self.update_amount(max)
            return max
        else:
            self.update_amount(self.current_amount)
            return self.current_amount

    def get_amount(self):
        return self.current_amount

    def update_amount(self, amount):
        self.current_amount -= amount
        if self.current_amount < 0:
            self.current_amount = 0
