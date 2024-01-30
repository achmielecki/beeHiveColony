from datetime import timedelta
from beehive.bee.bee import Bee
from beehive.world import World
from beehive.hive import Hive
from beehive.bee.roles import employed, scout, onlooker
import numpy as np


world = World(num_hives=1, num_bees_per_hive=300, num_food_sources=2500)
hive = Hive(world, 300, 1000, 1000)
bee = Bee(hive, 1000, 1000, world.get_time() - timedelta(seconds=(3110400 * np.random.rand())))
bee.become_scout()


def test_act_dance() -> None:
    bee.is_dancing = True

