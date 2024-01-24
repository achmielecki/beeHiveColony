from beehive.bee.artificialBeeColonyBehaviour import ArtificialBeeColonyBehaviour


class Employed(ArtificialBeeColonyBehaviour):
    def __init__(self, bee):
        super().__init__(bee)
        self.bee = bee

    def act(self):
        if self.should_leave_nectar_in_hive():
            self.update_distance_to_hive()
            if not self.is_around_hive():
                self.go_to_hive()
            else:
                self.leave_food_in_hive()
            return
        if self.bee.my_food_source is None:
            self.bee.become_onlooker()
        else:
            if self.distance_to_your_food() > 0.05:
                self.go_to_your_food_source()
            else:
                self.harvest()
                if self.my_food_is_not_efficient_anymore():
                    self.abandon_my_food_source()

    def should_leave_nectar_in_hive(self):
        return self.bee.carried_nectar > self.max_carry * 0.8 or (self.bee.carried_nectar > 0 and self.bee.my_food_source is None)

    def leave_food_in_hive(self):
        self.bee.hive.leave_nectar(self.bee.carried_nectar)
        self.bee.carried_nectar = 0

    def go_to_your_food_source(self):
        self.go_towards_object(self.bee.my_food_source)

    def harvest(self):
        amount_that_can_be_harvested = min(self.max_carry / 4, self.max_carry - self.bee.carried_nectar)
        self.bee.carried_nectar = self.bee.my_food_source.extract_food(amount_that_can_be_harvested)

    def my_food_is_not_efficient_anymore(self):
        return self.bee.my_food_source.current_amount < self.max_carry

    def abandon_my_food_source(self):
        self.bee.my_food_source = None
