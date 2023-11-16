import numpy as np
import pandas as pd
import copy
from abc import ABC, abstractmethod

class Models(ABC):
    """
    Abstract class for models
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def fit(self, data):
        pass


    def cross_validation(self, data):
        """Calculates the error of the model using k-fold cross validation

        Args:
        """
        total_error = 0
        for i in range(len(data)):
            train = data.drop(i)
            test = data[i]
            self.fit(train)
            total_error += self.error(test)

        return total_error/len(data)

    @abstractmethod
    def error(self, data):
        pass

    @abstractmethod
    def k_fold(self, data):
        pass

def elo_calc(rating_a, rating_b, result, k=10):
    """Basic function to calculate elo change

    Args:
        rating_a (int): Rating of player A
        rating_b (int): Rating of player B
        result ([0, 0.5, 1]): Result of the match, 0 for player A win, 0.5 for draw, 1 for player B win
        k (int, optional): Hyperparam that defines elo rate of change. Defaults to 10.

    Returns:
        [int, int]: Change in rating for player A and player B
    """

    expected = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    change = k * (result - expected)
    return change, -change


class EloRating(Models):
    def __init__(self, ratings, k=10) -> None:
        self.k = k
        self.ratings = ratings

    def fit(self, data):
        """Fits the model to the data

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
        """
        for i in range(len(data)):
            ratings_copy = copy.deepcopy(self.ratings)
            results = data[i][0]
            names = data[i][1]
            for j in range(len(results)):
                for k in range(j+1, len(results)):
                    r = results[j] < results[k]
                    change = elo_calc(self.ratings[names[j]], self.ratings[names[k]], r, self.k)

                    ratings_copy[names[j]] += change[0]/len(results)
                    ratings_copy[names[k]] += change[1]/len(results)

            self.ratings = ratings_copy

    def error(self, data):
        """Calculates the error of the model

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
        """

        error = 0
        for i in range(len(data)):
            results = data[i][0]
            names = data[i][1]
            for j in range(len(results)):
                for k in range(j+1, len(results)):
                    r = results[j] < results[k]
                    change = elo_calc(self.ratings[names[j]], self.ratings[names[k]], r, self.k)

                    error += abs(change[0])
                    error += abs(change[1])

        return error/self.k * len(data)

    def k_fold(self, data, ratings):
        """ ESSE MÉTODO AINDA PODE MUDAR EU ACHO
        Calculates the error of the model using k-fold cross validation

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
            ratings (dict): Dictionary of ratings for each player
        """

        total_error = 0
        for i in range(len(data)):
            train = data[:i] + data[i+1:]
            test = data[i:i+1]
            self.ratings = ratings
            self.fit(train)
            total_error += self.error(test)

        return total_error/len(data)

# def glicko_calc(rating_a, rating_b, rd_a, rd_b, vol_a, vol_b, tau, result):
#     q_a = np.log(10)/400
#     q_b = np.log(10)/400
#     g_a = 1/np.sqrt(1 + 3*q_a**2*rd_a**2/np.pi**2)
#     g_b = 1/np.sqrt(1 + 3*q_b**2*rd_b**2/np.pi**2)
#     e_a = 1/(1 + 10**(-g_a*(rating_a - rating_b)/400))
#     e_b = 1/(1 + 10**(-g_b*(rating_b - rating_a)/400))
#     d = 1/(q_b**2*g_a**2*e_a*(1 - e_a) + q_a**2*g_b**2*e_b*(1 - e_b))
#     change_a = q_a/(1/rd_a**2 + g_b**2*e_a*(1 - e_a)*d)*(g_b*(result - e_a))
#     change_b = q_b/(1/rd_b**2 + g_a**2*e_b*(1 - e_b)*d)*(g_a*(1 - result - e_b))
#     change_rd_a = np.sqrt(1/(1/rd_a**2 + g_b**2*e_a*(1 - e_a)*d))
#     change_rd_b = np.sqrt(1/(1/rd_b**2 + g_a**2*e_b*(1 - e_b)*d))
#     change_vol_a = 1/(1/vol_a**2 + 1/change_rd_a**2)
#     change_vol_b = 1/(1/vol_b**2 + 1/change_rd_b**2)

#     return change_a,

# class GlickoRating(Models):
    # def __init__(self, ratings, rd, vol, tau=0.5) -> None:
    #     self.ratings = ratings
    #     self.rd = rd
    #     self.vol = vol
    #     self.tau = tau

    # def fit(self, data):
    #     for i in range(len(data)):
    #         ratings_copy = copy.deepcopy(self.ratings)
    #         rd_copy = copy.deepcopy(self.rd)
    #         vol_copy = copy.deepcopy(self.vol)
    #         results = data[i][0]
    #         names = data[i][1]
    #         for j in range(len(results)):
    #             for k in range(j+1, len(results)):
    #                 r = results[j] < results[k]
    #                 change = glicko_calc(self.ratings[names[j]], self.ratings[names[k]], self.rd[names[j]], self.rd[names[k]], self.vol[names[j]], self.vol[names[k]], self.tau, r)

    #                 ratings_copy[names[j]] += change[0]/len(results)
    #                 ratings_copy[names[k]] += change[1]/len(results)
    #                 rd_copy[names[j]] += change[2]/len(results)
    #                 rd_copy[names[k]] += change[3]/len(results)
    #                 vol_copy[names[j]] += change[4]/len(results)
    #                 vol_copy[names[k]] += change[5]/len(results)

    #         self.ratings = ratings_copy
    #         self.rd = rd_copy
    #         self.vol = vol_copy

    # def error(self, data):
    #     error = 0
    #     for i in range(len(data)):
    #         results = data[i][0]
    #         names = data[i][1]
    #         for j in range(len(results)):
    #             for k in range(j+1, len(results)):
    #                 r = results[j] < results[k]
    #                 change = glicko_calc(self.ratings[names[j]], self.ratings[names[k]], self.rd[names[j]], self.rd[names[k]], self.vol[names[j]], self.vol[names[k]], self.tau, r)

    #                 error += abs(change[0])
    #                 error += abs(change[1])
    #                 error += abs(change[2])
    #                 error += abs(change[3])
    #                 error += abs(change[4])
    #                 error += abs(change[5])

    #     return error/self.k * len(data)

    # def k_fold(self, data, ratings, rd, vol):
    #     total_error = 0
    #     for i in range(len(data)):
    #         train = data[:i] + data[i+1:]
    #         test = data[i:i+1]
    #         self.ratings = ratings
    #         self.rd = rd
    #         self.vol = vol
    #         self.fit(train)
    #         total_error += self.error(test)


    #     return total_error/len(data)