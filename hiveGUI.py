import time
import pygame
from beehive.bee.artificialBeeColonyBehaviour import Role


class HiveGUI:
    def __init__(self, world):
        self.world = world
        self.width = 1000
        self.height = self.width
        self.ratio = self.width / world.get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BeeHiveColony")

    def run(self):
        running = True
        while running:
            time.sleep(0.1)
            self.world.simulate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.draw_world()

            pygame.display.flip()

        pygame.quit()

    def draw_world(self):
        self.draw_hives(self.world.get_hives())
        self.draw_food_sources(self.world.get_food_sources())

    def draw_hives(self, hives):
        for hive in hives:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.scale(hive.get_x()), self.scale(hive.get_y()), 5, 5))
            self.draw_hive_bees(hive)

    def draw_hive_bees(self, hive):
        for bee in hive.get_bees():
            if bee.behaviour.role == Role.scout:
                pygame.draw.circle(self.screen, (204, 102, 0), (self.scale(bee.get_x()), self.scale(bee.get_y())), 3)
            else:
                pygame.draw.circle(self.screen, (0, 0, 255), (self.scale(bee.get_x()), self.scale(bee.get_y())), 3)

    def draw_food_sources(self, food_sources):
        for food_source in food_sources:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             (self.scale(food_source.get_x()), self.scale(food_source.get_y()), 5, 5))

    def scale(self, x):
        return self.ratio * x
