from beehive.world import World
from hiveGUI import HiveGUI

world = World(num_hives=1, num_bees_per_hive=1, num_food_sources=6)
gui = HiveGUI(world)
gui.run()
