import datetime

from beehive.world import World


def run():
    while world.time - start_simulation < stop_simulation:
        world.simulate()


# values for test
number_of_bees = 300
number_of_food = 2500
world_size = 2000

# initialize test world
world = World(num_hives=1, num_bees_per_hive=number_of_bees, num_food_sources=number_of_food, world_size=world_size)

# get start time of simulation
start_simulation = world.time

# set time of simulation
stop_simulation = datetime.timedelta(days=7)

run()
