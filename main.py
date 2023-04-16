from beehive.hive import Hive

hive = Hive(num_bees=100, num_food_sources=3, world_size=50)
hive.simulate(num_iterations=100)
hive.plot()
