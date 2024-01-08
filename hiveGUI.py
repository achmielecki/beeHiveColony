import time
import pygame
from beehive.bee.artificialBeeColonyBehaviour import Role, bee_nectar_max_carry


class HiveGUI:
    def __init__(self, world):
        self.world = world
        self.width = 1000  # 1280
        self.height = 1000  # 720
        self.ratio = self.width / world.get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BeeHiveColony")
        # self.bee_img = pygame.image.load('assets/bee_left1.png')
        self.grass_img = pygame.image.load('assets/grass.png')
        self.bee_img_blue = pygame.image.load('assets/bee1_left_blue.png')
        self.bee_img_orange = pygame.image.load('assets/bee1_left_orange.png')
        self.bee_img_red = pygame.image.load('assets/bee1_left_red.png')
        self.hive_img = pygame.image.load('assets/bee_hive.png')
        self.bush_img = pygame.image.load('assets/bush.png')
        self.bush_flower_img = pygame.image.load('assets/bush_flowers.png')

    def run(self):
        running = True
        while running:
            self.world.simulate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # self.screen.fill((255, 255, 255))
            self.screen.blit(self.grass_img, (0, 0))
            self.draw_world()

            pygame.display.flip()

        pygame.quit()

    def draw_world(self):
        self.draw_food_sources(self.world.get_food_sources())
        self.draw_hives(self.world.get_hives())

    def draw_hives(self, hives):
        for hive in hives:
            self.draw_hive_bees(hive)
            # pygame.draw.rect(self.screen, (255, 0, 0), (self.scale(hive.get_x()), self.scale(hive.get_y()), 5, 5))
            hive_rect = self.hive_img.get_rect(center=(self.scale(hive.get_x()), self.scale(hive.get_y())))
            self.screen.blit(self.hive_img, hive_rect)

    def draw_hive_bees(self, hive):
        for bee in hive.get_bees():
            if bee.behaviour.role == Role.scout:
                # pygame.draw.circle(self.screen, (204, 102, 0), (self.scale(bee.get_x()), self.scale(bee.get_y())), 3)
                bee_rect = self.bee_img_orange.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                self.screen.blit(self.bee_img_orange, bee_rect)
            elif bee.behaviour.role == Role.employed_in_hive:
                pass
            elif bee.behaviour.is_dancing:
                # pygame.draw.circle(self.screen, (255, 0, 0), (self.scale(bee.get_x()), self.scale(bee.get_y())), 3)
                bee_rect = self.bee_img_red.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                self.screen.blit(self.bee_img_red, bee_rect)
            else:
                # pygame.draw.circle(self.screen, (0, 0, 255), (self.scale(bee.get_x()), self.scale(bee.get_y())), 3)
                bee_rect = self.bee_img_blue.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                self.screen.blit(self.bee_img_blue, bee_rect)

    def draw_food_sources(self, food_sources):
        for food_source in food_sources:
            if food_source.discovered:
                if food_source.current_amount >= bee_nectar_max_carry:
                    # pygame.draw.rect(self.screen, (0, 255, 0),
                    #                  (self.scale(food_source.get_x()), self.scale(food_source.get_y()), 5, 5))
                    bush_rect = self.bush_flower_img.get_rect(
                        center=(self.scale(food_source.get_x()), self.scale(food_source.get_y())))
                    self.screen.blit(self.bush_flower_img, bush_rect)
                else:
                    # pygame.draw.rect(self.screen, (255, 165, 0),
                    #                  (self.scale(food_source.get_x()), self.scale(food_source.get_y()), 5, 5))
                    bush_rect = self.bush_img.get_rect(
                        center=(self.scale(food_source.get_x()), self.scale(food_source.get_y())))
                    self.screen.blit(self.bush_img, bush_rect)

    def scale(self, x):
        return self.ratio * x
