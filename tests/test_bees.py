from datetime import timedelta
from beehive.bee.bee import Bee
from beehive.world import World
from beehive.hive import Hive
from beehive.bee.roles import employed, scout, onlooker
import numpy as np


world = World(num_hives=1, num_bees_per_hive=300, num_food_sources=2500)
hive = Hive(world, 300, 1000, 1000)
bee = Bee(hive, 1000, 1000, world.get_time() - timedelta(seconds=(3110400 * np.random.rand())))


def test_role_assignment() -> None:
    assert bee.role is not None


def test_become_employed() -> None:
    bee.become_employed()
    assert isinstance(bee.role, employed.Employed)


def test_become_scout() -> None:
    bee.become_scout()
    assert isinstance(bee.role, scout.Scout)


def test_become_onlooker() -> None:
    bee.become_onlooker()
    assert isinstance(bee.role, onlooker.Onlooker)


def test_get_x() -> None:
    assert bee.get_x() == bee.x


def test_get_y() -> None:
    assert bee.get_y() == bee.y


def test_get_age() -> None:
    assert world.get_time() - bee.born_time == bee.get_age()
