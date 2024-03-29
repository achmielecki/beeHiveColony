from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour
import numpy as np
from beehive.constVariables import *


class Onlooker(ArtificialBeeColonyBehaviour):
    def __init__(self, bee):
        super().__init__(bee)
        self.bee = bee

    def act(self):
        self.stay_around_hive()
        if self.is_around_hive() and self.are_there_any_dances():
            self.get_employed_at_best_food_source()
        else:
            if self.should_become_scout():
                self.become_scout()

    def are_there_any_dances(self):
        return self.bee.hive.get_current_dances()

    def get_employed_at_best_food_source(self):
        self.bee.my_food_source = self.choose_best_dance()
        self.bee.become_employed()

    def become_scout(self):
        self.bee.hive.current_scouts += 1
        self.bee.become_scout()

    def should_become_scout(self):
        return np.random.rand() < self.chance_of_becoming_scout()

    def chance_of_becoming_scout(self):
        if self.bee.hive.current_scouts >= self.bee.hive.max_scouts:
            return 0
        if self.bee.hive.world.is_it_dark():
            return 0
        return chance_of_becoming_scout

    def choose_best_dance(self):
        dances = self.bee.hive.get_current_dances()
        dance = list(sorted(dances, key=lambda it: it[2]))[-1]
        dance[0].ack_onlooker()
        return dance[1]
