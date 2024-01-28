from beehive.bee.artificialBeeColonyBehaviour import Role
from beehive.bee.Roles.employed import Employed
from beehive.bee.Roles.scout import Scout
from beehive.bee.Roles.onlooker import Onlooker
from beehive.bee.Roles.inHive import InHive
import beehive.bee.Logic.goForFood as gff
import numpy as np
import uuid

dance_intensity_model = gff.GoForFood()


class Bee:
    def __init__(
            self,
            hive,
            x,
            y,
            born_time
    ):
        self.id = uuid.uuid4()
        self.hive = hive
        self.x = x
        self.y = y
        self.born_time = born_time
        self.role_tag, self.role = self.init_role()
        self.scout_steps = 0
        self.current_direction = 1  # angle in radians
        self.acked_onlookers = 0
        self.dance_intensity = dance_intensity_model
        self.carried_nectar = 0
        self.is_dancing = False
        self.spotted_food = None
        self.overall_food_quality = None
        self.distance_to_hive = None
        self.my_food_source = None

    def init_role(self):
        if np.random.rand() < 0.8:
            #return Role.onlooker, Onlooker(self)
            return Role.employed_in_hive, InHive(self)
        else:
            #return Role.scout, Scout(self)
            return Role.onlooker, Onlooker(self)

    def become_onlooker(self):
        self.role = Onlooker(self)
        self.role_tag = Role.onlooker

    def become_employed(self):
        self.role = Employed(self)
        self.role_tag = Role.employed

    def become_scout(self):
        self.role = Scout(self)
        self.role_tag = Role.scout

    def act(self):
        if self.role.is_too_old():
            self.role.die()
        self.role.act()

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_age(self):
        return self.hive.world.get_time() - self.born_time
