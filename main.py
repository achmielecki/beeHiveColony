from beehive.world import World
from hiveGUI import HiveGUI

world = World(num_hives=3, num_bees_per_hive=10, num_food_sources=50)
gui = HiveGUI(world)
gui.run()
