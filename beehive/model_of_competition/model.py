import numpy as np
import pandas as pd
import random

from beehive.constVariables import *

class ModelOfCompetition:
    def __init__(self, temperature, rainfall, forager_count, num_bee_families, qd1):
        self.num_bee_families = num_bee_families
        self.ALPHA = MOC_ALPHA
        self.BETA = MOC_BETA
        self.simulation_duration = len(temperature)
        self.QD1 = qd1
        self.QD2 = MOC_QD2
        self.forager_count = forager_count
        self.probability_of_finding = MOC_PROBABILITY_OF_FINDING

        self.nectar_foragers = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)
        self.pollen_foragers = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)
        self.environmental_conditions = np.zeros(self.simulation_duration, dtype=float)
        self.information_variable = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)
        self.nectar_mass = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)
        self.pollen_mass = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)
        self.daily_temperature = []
        self.daily_rainfall = []
        self.probability_of_competition = np.zeros((self.num_bee_families, self.simulation_duration), dtype=float)

        self.sum_U1 = np.zeros((4, self.num_bee_families), dtype=float)
        self.sum_U2 = np.zeros(self.num_bee_families, dtype=float)
        self.initialize_temperature(temperature)
        self.initialize_rainfall(rainfall)

    def initialize_temperature(self, data):
        self.daily_temperature = data

    def initialize_rainfall(self, data):
        self.daily_rainfall = data

    def initialize_information_variable(self, t):
        for k in range(self.simulation_duration):
            for i in range(self.num_bee_families):
                if k == 0:
                    self.information_variable[i, k] = 0.0
                    self.probability_of_competition[i][k] = 0.0
                else:
                    self.information_variable[i, k] = self.compute_information(i, k, t)

    def get_daily_temp(self, k):
        return self.daily_temperature[k]

    def get_daily_rainfall(self, k):
        return self.daily_rainfall[k]

    def get_temperature_weight_in_day(self, k):
        if self.get_daily_temp(k) <= 10.0:
            return 0
        elif 10 < self.get_daily_temp(k) <= 14:
            return 0.25 * (self.get_daily_temp(k) - 10)
        return 1

    def get_rainfall_weight_in_day(self, k):
        if self.get_daily_rainfall(k) == 0:
            return 1
        elif 0 < self.get_daily_rainfall(k) <= 10:
            return 1 - (0.1 * self.get_daily_rainfall(k))
        return 0

    def get_atmospheric_conditions_weight(self, k):
        return self.get_rainfall_weight_in_day(k) * self.get_temperature_weight_in_day(k)

    def get_count_of_nectar_bees(self, i, k):
        return self.forager_count

    def get_count_of_pollen_bees(self, i, k):
        return self.forager_count

    def get_number_of_flights_per_bee(self, k):
        return 10.0

    def get_nectar_mass_of_family_in_day(self, i, k):
        return self.ALPHA * self.get_number_of_flights_per_bee(k) * self.environmental_conditions[k] * self.nectar_foragers[i, k] * \
            self.information_variable[i, k]

    def get_pollen_mass_of_family_in_day(self, i, k):
        return self.BETA * self.get_number_of_flights_per_bee(k) * self.environmental_conditions[k] * self.pollen_foragers[i, k] * \
            self.information_variable[i, k]

    def RAND(self):
        return random.random()

    def compute_information(self, i, k, t):
        self.probability_of_competition[i][k] = self.RAND()
        if self.probability_of_competition[i][k] < self.probability_of_finding[t]:
            return 1.0
        else:
            return 0.0

    def simulation(self, additional_model_condition):
        if not additional_model_condition:
            for t in range(len(self.probability_of_finding)):
                self.initialize_information_variable(t)
                for k in range(self.simulation_duration):
                    self.update_foragers(t, k)
                    self.update_environmental_conditions(k)
                    self.update_information_variable(t, k)
                    self.update_forager_mass(t, k)
                    self.adjust_mass_values(t, k)

    def update_foragers(self, t, k):
        for i in range(self.num_bee_families):
            self.nectar_foragers[i, k] = self.get_count_of_nectar_bees(i, k)
            self.pollen_foragers[i, k] = self.get_count_of_pollen_bees(i, k)

    def update_environmental_conditions(self, k):
        self.environmental_conditions[k] = self.get_atmospheric_conditions_weight(k)

    def update_information_variable(self, t, k):
        if k >= 1:
            for j in range(self.num_bee_families):
                if self.information_variable[j, k - 1] != 1.0:
                    if self.probability_of_competition[j][k] <= self.probability_of_finding[t]:
                        self.information_variable[j, k] = 1.0
                    else:
                        self.information_variable[j, k] = 0.0

    def update_forager_mass(self, t, k):
        for i in range(self.num_bee_families):
            self.nectar_mass[i, k] = self.get_nectar_mass_of_family_in_day(i, k)
            self.pollen_mass[i, k] = self.get_pollen_mass_of_family_in_day(i, k)
            self.sum_U1[t][i] = self.sum_U1[t][i] + self.nectar_mass[i, k]
            self.sum_U2[i] = self.sum_U2[i] + self.pollen_mass[i, k]

    def adjust_mass_values(self, t, k):
        for i in range(self.num_bee_families):
            while self.sum_U1[t][i] > (self.QD1 * 3):
                self.sum_U1[t][i] = self.sum_U1[t][i] - (1 * (self.sum_U1[t][i] / self.num_bee_families))
            while self.sum_U2[i] > (self.QD2 * 3):
                self.sum_U2[i] = self.sum_U2[i] - (1 * (self.sum_U2[i] / self.num_bee_families))

    def create_df_for_neural_network(self):
        df = []

        temperature = []
        rainfall = []
        probability = []
        nectar = []

        for k in range(self.simulation_duration):
            temperature.append(self.daily_temperature[k])
            rainfall.append(self.daily_rainfall[k])

            for i in range(self.num_bee_families):
                probability.append(self.probability_of_competition[i][k])

        for t in range(len(self.probability_of_finding)):
            for i in range(self.num_bee_families):
                nectar.append(self.sum_U1[t][i])

        df.append({
            "temperature": temperature,
            "rainfall": rainfall,
            "probability": probability,
            "nectar": nectar
        })

        return pd.DataFrame(df)

    def get_foraged_nectar(self):
        nectar = []

        for t in range(len(self.probability_of_finding)):
            nectar.append(self.sum_U1[t][0])
        return sum(nectar)

    def create_csv_from_df(self, name, df):
        df.to_csv(name, encoding='utf-8')
