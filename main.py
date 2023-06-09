from beehive.world import World

world = World(num_hives=1, num_bees_per_hive=1, num_food_sources=3)
world.simulate(num_iterations=100)
world.plot()
