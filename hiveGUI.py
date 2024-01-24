import pygame
from beehive.bee.artificialBeeColonyBehaviour import Role, bee_nectar_max_carry


class HiveGUI:
    def __init__(self, world):
        self.world = world
        self.width = 1400
        self.height = 1000
        self.simulation_dimension = 1000  # wymiary symulowanego świata to 1000x1000 px
        self.ratio = self.simulation_dimension / world.get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.grass_img = pygame.image.load('assets/grass.png')
        self.honeycomb_img = pygame.image.load('assets/honeycomb.png')
        self.bee_img_blue = pygame.image.load('assets/bee1_left_blue.png')
        self.bee_img_orange = pygame.image.load('assets/bee1_left_orange.png')
        self.bee_img_red = pygame.image.load('assets/bee1_left_red.png')
        self.hive_img = pygame.image.load('assets/bee_hive.png')
        self.bush_img = pygame.image.load('assets/bush.png')
        self.bush_flower_img = pygame.image.load('assets/bush_flowers.png')

        pygame.display.set_caption("Wizualne modelowanie ula pszczelego")
        pygame.display.set_icon(self.bee_img_orange)

        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 22)
        self.font_title = pygame.font.SysFont('Comic Sans MS', 22, bold=True)

    def run(self):
        running = True
        while running:
            self.world.simulate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((226, 177, 86))
            self.screen.blit(self.grass_img, (0, 0))
            self.draw_world()

            pygame.display.flip()

        pygame.quit()

    def draw_world(self):
        self.draw_food_sources(self.world.get_food_sources())
        self.draw_hives(self.world.get_hives())

        self.draw_side_panel(self.world.get_hives()[0], self.world)

    def draw_hives(self, hives):
        for hive in hives:
            self.draw_hive_bees(hive)
            hive_rect = self.hive_img.get_rect(center=(self.scale(hive.get_x()), self.scale(hive.get_y())))
            self.screen.blit(self.hive_img, hive_rect)

    def draw_hive_bees(self, hive):
        for bee in hive.get_bees():
            if self.scale(bee.get_x()) < 1000:
                if bee.behaviour.role == Role.scout:
                    bee_rect = self.bee_img_orange.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                    self.screen.blit(self.bee_img_orange, bee_rect)
                elif bee.behaviour.role == Role.employed_in_hive:
                    pass
                elif bee.behaviour.is_dancing:
                    pass
                else:
                    bee_rect = self.bee_img_blue.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                    self.screen.blit(self.bee_img_blue, bee_rect)

    def draw_food_sources(self, food_sources):
        for food_source in food_sources:
            if food_source.discovered:
                if food_source.current_amount >= bee_nectar_max_carry:
                    bush_rect = self.bush_flower_img.get_rect(
                        center=(self.scale(food_source.get_x()), self.scale(food_source.get_y())))
                    self.screen.blit(self.bush_flower_img, bush_rect)
                else:
                    bush_rect = self.bush_img.get_rect(
                        center=(self.scale(food_source.get_x()), self.scale(food_source.get_y())))
                    self.screen.blit(self.bush_img, bush_rect)

    def scale(self, x):
        return self.ratio * x

    def draw_side_panel(self, hive, world):
        time = world.get_time()
        temp = world.get_week_temps()
        rainfall = world.get_week_rainfall()

        # tło panelu bocznego
        self.screen.blit(self.honeycomb_img, (self.simulation_dimension, 0))

        # czas
        day_text = self.font.render('DZIEŃ ' + str(time.day), True, (0, 0, 0))
        self.screen.blit(day_text, (self.width - 380, 30))

        minutes = ('0' + str(time.minute)) if (time.minute < 10) else str(time.minute)
        time_text = self.font.render(str(time.hour) + ':' + minutes, True, (0, 0, 0))
        self.screen.blit(time_text, (self.width - 80, 30))

        # pogoda
        temperature_text = self.font.render('Temperatura: ' + str(temp[time.day]) + ' °C', True, (0, 0, 0))
        self.screen.blit(temperature_text, (self.width - 380, 80))

        humidity_text = self.font.render('Opady: ' + str(rainfall[time.day]) + ' mm', True, (0, 0, 0))
        self.screen.blit(humidity_text, (self.width - 380, 120))

        # prognoza pogody na cały tydzień
        statistics_text = self.font_title.render('PROGNOZA POGODY:', True, (0, 0, 0))
        self.screen.blit(statistics_text, (self.width - 380, 180))
        statistics_text = self.font.render('Dzień:', True, (0, 0, 0))
        self.screen.blit(statistics_text, (self.width - 380, 230))
        statistics_text = self.font.render('Temp. [°C]:', True, (0, 0, 0))
        self.screen.blit(statistics_text, (self.width - 380, 280))
        statistics_text = self.font.render('Opady [mm]:', True, (0, 0, 0))
        self.screen.blit(statistics_text, (self.width - 380, 330))
        for i in range(time.day, 7):
            day_text = self.font.render(str(i+1), True, (0, 0, 0))
            self.screen.blit(day_text, (self.width - 280 + (i * 40), 230))
            temp_text = self.font.render(str(temp[i]), True, (0, 0, 0))
            self.screen.blit(temp_text, (self.width - 280 + (i * 40), 280))
            rain_text = self.font.render(str(rainfall[i]), True, (0, 0, 0))
            self.screen.blit(rain_text, (self.width - 280 + (i * 40), 330))

        # ustawienia użytkownika
        # TODO

        # statystyki ula
        statistics_text = self.font_title.render('STATYSTYKI ULA:', True, (0, 0, 0))
        self.screen.blit(statistics_text, (self.width - 380, 400))

        food_text = self.font.render('Zebrany nektar: ' + str(round(hive.nectar_stored, 3)) + ' g', True, (0, 0, 0))
        self.screen.blit(food_text, (self.width - 380, 450))

        food_text = self.font.render('Prognoza zbiorów na dziś: ' + str(round(hive.nectar_goal, 3)) + ' g', True, (0, 0, 0))
        self.screen.blit(food_text, (self.width - 380, 500))

        bee_text = self.font.render('Pszczoły wylatujące z ula: ' + str(len(hive.bees)), True, (0, 0, 0))
        self.screen.blit(bee_text, (self.width - 380, 550))

        bee_text = self.font.render('Umarłe pszczoły: ' + str(hive.dead_bees), True, (0, 0, 0))
        self.screen.blit(bee_text, (self.width - 380, 600))

        # legenda
        legend_text = self.font_title.render('LEGENDA:', True, (0, 0, 0))
        self.screen.blit(legend_text, (self.width - 380, 680))

        scaled_hive_img = pygame.transform.scale(self.hive_img, (40, 40))
        hive_rect = scaled_hive_img.get_rect(midleft=(self.width - 380, 750))
        self.screen.blit(scaled_hive_img, hive_rect)
        legend_hive_text = self.font.render('- ul', True, (0, 0, 0))
        legend_hive_text_rect = legend_hive_text.get_rect(midleft=(self.width - 320, 750))
        self.screen.blit(legend_hive_text, legend_hive_text_rect)

        food_source_full_rect = self.bush_flower_img.get_rect(center=(self.width - 360, 800))
        self.screen.blit(self.bush_flower_img, food_source_full_rect)
        legend_food_source_full_text = self.font.render('- pełne źródło jedzenia', True, (0, 0, 0))
        legend_food_source_full_text_rect = legend_food_source_full_text.get_rect(midleft=(self.width - 320, 800))
        self.screen.blit(legend_food_source_full_text, legend_food_source_full_text_rect)

        food_source_empty_rect = self.bush_img.get_rect(center=(self.width - 360, 850))
        self.screen.blit(self.bush_img, food_source_empty_rect)
        legend_food_source_empty_text = self.font.render('- puste źródło jedzenia', True, (0, 0, 0))
        legend_food_source_empty_text_rect = legend_food_source_empty_text.get_rect(midleft=(self.width - 320, 850))
        self.screen.blit(legend_food_source_empty_text, legend_food_source_empty_text_rect)

        bee_scout_rect = self.bee_img_orange.get_rect(center=(self.width - 360, 900))
        self.screen.blit(self.bee_img_orange, bee_scout_rect)
        legend_bee_scout_text = self.font.render('- pszczoła zwiadowczyni', True, (0, 0, 0))
        legend_bee_scout_text_rect = legend_bee_scout_text.get_rect(midleft=(self.width - 320, 900))
        self.screen.blit(legend_bee_scout_text, legend_bee_scout_text_rect)

        bee_harvesting_rect = self.bee_img_blue.get_rect(center=(self.width - 360, 950))
        self.screen.blit(self.bee_img_blue, bee_harvesting_rect)
        legend_bee_harvesting_text = self.font.render('- pszczoła zbieraczka', True, (0, 0, 0))
        legend_bee_harvesting_text_rect = legend_bee_harvesting_text.get_rect(midleft=(self.width - 320, 950))
        self.screen.blit(legend_bee_harvesting_text, legend_bee_harvesting_text_rect)