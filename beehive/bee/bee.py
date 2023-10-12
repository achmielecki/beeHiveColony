import numpy as np
from beehive.bee.beeFuzzyBehaviour import BeeFuzzyBehaviour
from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour


class Bee:
    def __init__(
            self,
            hive,
            x,
            y
    ):
        self.hive = hive
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.behaviour = ArtificialBeeColonyBehaviour(self)

    def act(self):
        self.behaviour.act()

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y
