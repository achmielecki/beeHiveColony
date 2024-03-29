bee_max_speed = 8.2  # m/s
bee_min_speed = 4.9  # m/s
max_life_time = 36  # days
max_life_time_deviation = 48  # hours
bee_nectar_max_carry = 0.06  # grams https://ucanr.edu/blogs/blogcore/postdetail.cfm?postnum=43385
bee_sight_range = 5  # m
chance_of_becoming_scout = 0.001
flower_max_nectar_carry = 0.007
jiggle_effect_base_strength = 0.6
max_count_of_flowers_in_one_place = 30
world_size = 2000
daily_bee_spawn_rate = 50
flower_nectar_respawn_rate = 0.0005
forget_food_source_hours = 12
debug_mode = True

#### variables for model of competition

MOC_ALPHA = bee_nectar_max_carry * 0.6  # Masa nektaru przynoszona w jednym locie przez 1 pszczołe zbieraczke nektaru
MOC_BETA = 0.015  # Masa pyłku kwiatowego w jednym locie przez 1 pszczołe zbieraczke pyłku kwiatowego
MOC_QD2 = 2
MOC_PROBABILITY_OF_FINDING = [0.25, 0.5, 0.750, 1.0]
