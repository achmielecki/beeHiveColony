import numpy as np

flower_max_nectar_carry = 0.007  # grams https://royalsocietypublishing.org/doi/10.1098/rstb.2021.0163
max_count_of_flowers_in_one_place = 30


class FoodSource:
    def __init__(
            self,
            x,
            y,
            max_amount=flower_max_nectar_carry * max_count_of_flowers_in_one_place * np.random.rand(),
            spawn_rate=0
    ):
        self.count_of_flowers = max_count_of_flowers_in_one_place * np.random.rand()
        self.spawn_rate = spawn_rate
        self.x = x
        self.y = y
        self.max_amount = flower_max_nectar_carry * self.count_of_flowers
        self.current_amount = np.random.rand() * self.max_amount
        self.discovered = False

    def spot(self):
        self.discovered = True

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
