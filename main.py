from beehive.world import World
from hiveGUI import HiveGUI
from beehive.constVariables import debug_mode
import hiveGUIDebug

world = World(num_hives=1, num_bees_per_hive=300, num_food_sources=2500, world_size=2000)

if debug_mode is False:
    gui = HiveGUI(world)
else:
    gui = hiveGUIDebug.HiveGUI(world)
gui.run()
