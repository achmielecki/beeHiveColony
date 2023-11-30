from beehive.bee.artificialBeeColonyBehaviour import Role
from beehive.bee.Roles.employed import Employed
from beehive.bee.Roles.scout import Scout
from beehive.bee.Roles.onlooker import Onlooker
import numpy as np
import uuid


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
        self.role = self.init_role()
        self.role_tag = None

    def init_role(self):
        if np.random.rand() < 0.8:
            self.role_tag = Role.scout
            return Scout(self)
        else:
            self.role_tag = Role.onlooker
            return Onlooker(self)

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
        self.role.act()

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_age(self):
        return self.hive.world.get_time() - self.born_time
