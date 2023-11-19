from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour
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
        self.behaviour = ArtificialBeeColonyBehaviour(self)
        self.born_time = born_time

    def act(self):
        self.behaviour.act()

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_age(self):
        return self.hive.world.get_time() - self.born_time
