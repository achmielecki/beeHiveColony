from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour


class InHive(ArtificialBeeColonyBehaviour):
    def __init__(self, bee):
        super().__init__(bee)
        self.bee = bee

    def act(self):
        # work in hive
        return
