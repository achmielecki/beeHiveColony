from beehive.world import World
from hiveGUI import HiveGUI

world = World(num_hives=1, num_bees_per_hive=300, num_food_sources=744, world_size=2000)
gui = HiveGUI(world)
gui.run()
