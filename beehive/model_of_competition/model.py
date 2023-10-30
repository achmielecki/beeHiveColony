import numpy as np
import pandas as pd
import random


class ModelOfCompetition:
    def __init__(self, temperature, rainfall, forager_count, num_bee_families):
        self.num_bee_families = num_bee_families
        self.ALPHA = 0.015
        self.BETA = 0.015
        self.simulation_duration = len(temperature)
        self.QD1 = 10.0
        self.QD2 = 2.0
        self.forager_count = forager_count

        self.probability_of_finding = [0.25, 0.5, 0.750, 1.0]

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

    def TAU(self, k):
        return self.daily_temperature[k]

    def DELTA(self, k):
        return self.daily_rainfall[k]

    def PT(self, k):
        if self.TAU(k) <= 10.0:
            return 0
        elif 10 < self.TAU(k) <= 14:
            return 0.25 * (self.TAU(k) - 10)
        return 1

    def PD(self, k):
        if self.DELTA(k) == 0:
            return 1
        elif 0 < self.DELTA(k) <= 10:
            return 1 - (0.1 * self.DELTA(k))
        return 0

    def P(self, k):
        return self.PD(k) * self.PT(k)

    def W1(self, i, k):
        return 40.0

    def W2(self, i, k):
        return 10.0

    def L(self, k):
        return 10.0

    def U1(self, i, k):
        return self.ALPHA * self.L(k) * self.environmental_conditions[k] * self.nectar_foragers[i, k] * \
            self.information_variable[i, k]

    def U2(self, i, k):
        return self.BETA * self.L(k) * self.environmental_conditions[k] * self.pollen_foragers[i, k] * \
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
            self.nectar_foragers[i, k] = self.W1(i, k)
            self.pollen_foragers[i, k] = self.W2(i, k)

    def update_environmental_conditions(self, k):
        self.environmental_conditions[k] = self.P(k)

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
            self.nectar_mass[i, k] = self.U1(i, k)
            self.pollen_mass[i, k] = self.U2(i, k)
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
            for i in range(self.num_bee_families):
                nectar.append(self.sum_U1[t][i])
        return sum(nectar)

    def create_csv_from_df(self, name, df):
        df.to_csv(name, encoding='utf-8')
