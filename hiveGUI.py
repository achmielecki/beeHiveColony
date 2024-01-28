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
        self.honeycomb_bg_img = pygame.image.load('assets/honeycomb_with_bees_background.png')
        self.bee_img_blue = pygame.image.load('assets/bee1_left_blue.png')
        self.bee_img_orange = pygame.image.load('assets/bee1_left_orange.png')
        self.bee_img_red = pygame.image.load('assets/bee1_left_red.png')
        self.hive_img = pygame.image.load('assets/bee_hive.png')
        self.bush_img = pygame.image.load('assets/bush.png')
        self.bush_flower_img = pygame.image.load('assets/bush_flowers.png')

        self.chosen_temps = self.world.get_week_temps()
        self.chosen_rainfall = self.world.get_week_rainfall()

        pygame.display.set_caption("Wizualne modelowanie ula pszczelego")
        pygame.display.set_icon(self.bee_img_orange)

        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 22)
        self.font_title = pygame.font.SysFont('Comic Sans MS', 22, bold=True)

    def run(self):
        running = False

        while not running:
            for event in pygame.event.get():
                running = self.draw_start_screen(event)

                pygame.display.flip()

        while running:
            self.world.simulate()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

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
                if bee.role_tag == Role.scout:
                    bee_rect = self.bee_img_orange.get_rect(center=(self.scale(bee.get_x()), self.scale(bee.get_y())))
                    self.screen.blit(self.bee_img_orange, bee_rect)
                elif bee.role_tag == Role.employed_in_hive:
                    pass
                elif bee.is_dancing:
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
        temperature_text = self.font.render('Temperatura: ' + str(temp[time.day-1]) + ' °C', True, (0, 0, 0))
        self.screen.blit(temperature_text, (self.width - 380, 80))

        humidity_text = self.font.render('Opady: ' + str(rainfall[time.day-1]) + ' mm', True, (0, 0, 0))
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
            day_text_rect = day_text.get_rect(midtop=(self.width - 270 + (i * 40), 230))
            self.screen.blit(day_text, day_text_rect)
            temp_text = self.font.render(str(temp[i]), True, (0, 0, 0))
            temp_text_rect = temp_text.get_rect(midtop=(self.width - 270 + (i * 40), 280))
            self.screen.blit(temp_text, temp_text_rect)
            rain_text = self.font.render(str(rainfall[i]), True, (0, 0, 0))
            rain_text_rect = rain_text.get_rect(midtop=(self.width - 270 + (i * 40), 330))
            self.screen.blit(rain_text, rain_text_rect)

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

    def draw_start_screen(self, event):
        self.screen.blit(self.honeycomb_bg_img, (0, 0))

        title_text = self.font_title.render('USTAW POGODĘ NA TYDZIEŃ SYMULACJI', True, (0, 0, 0))
        title_text_rect = title_text.get_rect(center=(self.width / 2, 100))
        self.screen.blit(title_text, title_text_rect)

        instruction_text = self.font.render('Wybierz odpowiednie wartości za pomocą pokrętła myszy lub strzałek na '
                                            'ekranie.', True, (0, 0, 0))
        instruction_text_rect = instruction_text.get_rect(center=(self.width / 2, 150))
        self.screen.blit(instruction_text, instruction_text_rect)

        day_text = self.font_title.render('DZIEŃ:', True, (0, 0, 0))
        day_text_rect = day_text.get_rect(midright=(180, 250))
        self.screen.blit(day_text, day_text_rect)

        temp_text = self.font_title.render('Temperatura:', True, (0, 0, 0))
        temp_text_rect = temp_text.get_rect(midright=(180, 400))
        self.screen.blit(temp_text, temp_text_rect)

        temp_unit_text = self.font_title.render('°C', True, (0, 0, 0))
        temp_unit_text_rect = temp_unit_text.get_rect(midleft=(self.width - 180, 400))
        self.screen.blit(temp_unit_text, temp_unit_text_rect)

        rainfall_text = self.font_title.render('Opady:', True, (0, 0, 0))
        rainfall_text_rect = rainfall_text.get_rect(midright=(180, 625))
        self.screen.blit(rainfall_text, rainfall_text_rect)

        rainfall_unit_text = self.font_title.render('mm', True, (0, 0, 0))
        rainfall_unit_text_rect = rainfall_unit_text.get_rect(midleft=(self.width - 180, 625))
        self.screen.blit(rainfall_unit_text, rainfall_unit_text_rect)

        # pola wyboru wartości przez użytkownika
        for i in range(0, 7):
            day_number_text = self.font_title.render(str(i+1), True, (0, 0, 0))
            day_number_text_rect = day_number_text.get_rect(center=(250 + (i * 150), 250))
            self.screen.blit(day_number_text, day_number_text_rect)

            self.chosen_temps[i] = self.draw_number_input(250 + (i * 150), 325, self.chosen_temps[i], 1)
            self.chosen_rainfall[i] = self.draw_number_input(250 + (i * 150), 550, self.chosen_rainfall[i], 0.5, 0)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_width, button_height = (350, 80)  # wymiary przycisku
        button_x, button_y = (self.width / 2 - button_width / 2, self.height / 2 - button_height / 2 + 350)  # pozycja przycisku
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                self.world.set_week_temps(self.chosen_temps)
                self.world.set_week_rainfall(self.chosen_rainfall)
                return True  # Kliknięcie w przycisk ustawia running na True

        # Renderowanie przycisku
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            pygame.draw.rect(self.screen, (187, 135, 0), [button_x, button_y, button_width, button_height])
        else:
            pygame.draw.rect(self.screen, (230, 168, 0), [button_x, button_y, button_width, button_height])

        # Tekst na przycisku
        text = self.font_title.render("ROZPOCZNIJ SYMULACJĘ", True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
        self.screen.blit(text, text_rect)

    def draw_number_input(self, x, y, number, step, min_val=None):
        up_arrow_points = [[x, y], [x - 25, y + 25], [x + 25, y + 25]]
        down_arrow_points = [[x, y + 150], [x - 25, y + 125], [x + 25, y + 125]]

        def is_point_inside_triangle(point, vertices):
            def sign(p1, p2, p3):
                return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

            b1 = sign(point, vertices[0], vertices[1]) < 0.0
            b2 = sign(point, vertices[1], vertices[2]) < 0.0
            b3 = sign(point, vertices[2], vertices[0]) < 0.0

            return (b1 == b2) and (b2 == b3)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # obsługa kliknięcia myszy w strzałkę
        if is_point_inside_triangle((mouse_x, mouse_y), up_arrow_points):
            pygame.draw.polygon(self.screen, (187, 135, 0), up_arrow_points)
            if pygame.mouse.get_pressed()[0]:
                number += step
        else:
            pygame.draw.polygon(self.screen, "black", up_arrow_points)

        number_text = self.font_title.render(str(number), True, (0, 0, 0))
        number_rect = number_text.get_rect(center=(x, y + 75))
        self.screen.blit(number_text, number_rect)

        # obsługa kliknięcia myszy w strzałkę
        if is_point_inside_triangle((mouse_x, mouse_y), down_arrow_points) and (min_val is None or number > min_val):
            pygame.draw.polygon(self.screen, (187, 135, 0), down_arrow_points)
            if pygame.mouse.get_pressed()[0]:
                number -= step
        else:
            pygame.draw.polygon(self.screen, "black", down_arrow_points)

        # obsługa pokrętła myszy
        if (
                up_arrow_points[1][0] <= mouse_x <= up_arrow_points[2][0] and
                down_arrow_points[1][0] <= mouse_x <= down_arrow_points[2][0] and
                up_arrow_points[0][1] <= mouse_y <= down_arrow_points[0][1]
        ):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Ruch kółkiem myszy w górę
                    number += step
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and (min_val is None or number > min_val):  # Ruch kółkiem myszy w dół
                    number -= step

        # usunięcie zer po przecinku
        if int(number) == number:
            number = int(number)

        return number


