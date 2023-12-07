import numpy as np
import pandas as pd
import copy
import regex as re
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
    
    def elo_error(self, rating_a, rating_b, real_result):
        expected = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        return real_result - expected


    def error(self, data):
        """Calculates the error of the model

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
        """

        error = 0
        count = 0
        for i in range(len(data)):
            results = data[i][0]
            names = data[i][1]
            for j in range(len(results)):
                for k in range(j+1, len(results)):
                    r = results[j] < results[k]
                    error_update = self.elo_error(self.ratings[names[j]], self.ratings[names[k]], r)
                    error += abs(error_update)
                    count += 1

        # return error percentage
        return error/count

    def k_fold(self, data):
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
            self.fit(train)
            total_error += self.error(test)

        return total_error/len(data)


class Keeners(Models):
    def __init__(self, ratings=None, time_decay=False) -> None:
        self.ratings = ratings
        self.time_decay = time_decay

    def fit(self, data, time_decay=True, method='alpha'):
        """
        Calculates the ratings of each competitor using the Keener's method

        Args:
        data (pd.DataFrame): final dataframe with all the data
        time_decay (bool, optional): Whether to use time decay or not. Defaults to False. 
        method (str, optional): Method to use, either 'alpha' or 'beta'. Defaults to 'alpha'.       
        """
        self.time_decay = time_decay
        print(self.time_decay)

        # create dictionary to map competitor names to unique indices
        competitor_to_index = {competitor: idx for idx, competitor in enumerate(data['Nome Competidor'].unique())}

        # create matrix of size (n_players, n_players) with zeros
        n_players = len(competitor_to_index)
        matrix_alpha = np.zeros((n_players, n_players))
        matrix_beta = np.zeros((n_players, n_players))

        # iterate through competitions
        for competition in data['Nome Competição'].unique():
            year = int(data[data['Nome Competição'] == competition]['Ano'].values[0])

            # get data for this competition
            data_competition = data[data['Nome Competição'] == competition]
            data_competition = data_competition.drop_duplicates(subset='Nome Competidor', keep='first')

            # get list of competitors in this competition
            competitors = data_competition['Nome Competidor'].unique()
            # get number of competitors in this competition
            n_players = len(competitors)
            
            # iterate through competitors in this competition setting (i, j) = 1 if i beats j in this competition
            # get i and j from the dictionary
            for i in range(n_players):
                for j in range(n_players):
                    competitor_i = competitors[i]
                    competitor_j = competitors[j]
                    posicao_i = data_competition[(data_competition['Nome Competidor'] == competitor_i)]['Posição Geral'].values[0]
                    posicao_j = data_competition[(data_competition['Nome Competidor'] == competitor_j)]['Posição Geral'].values[0]
                    pontuacao_i = data_competition[(data_competition['Nome Competidor'] == competitor_i)]['Pontuação Total'].values[0]
                    pontuacao_j = data_competition[(data_competition['Nome Competidor'] == competitor_j)]['Pontuação Total'].values[0]

                    # get index of competitor i and j in the matrix
                    index_i = competitor_to_index[competitor_i]
                    index_j = competitor_to_index[competitor_j]

                    if posicao_i < posicao_j:
                        if self.time_decay:
                            if year >= 2021:
                                matrix_alpha[index_i][index_j] += 1
                                matrix_beta[index_i][index_j] += pontuacao_j/(pontuacao_i + pontuacao_j)
                            elif year >= 2016:
                                matrix_alpha[index_i][index_j] += 0.7
                                matrix_beta[index_i][index_j] += 0.7*(pontuacao_j/(pontuacao_i + pontuacao_j))
                            else:
                                matrix_alpha[index_i][index_j] += 0.3
                                matrix_beta[index_i][index_j] += 0.3*(pontuacao_j/(pontuacao_i + pontuacao_j))
                        else:
                            matrix_alpha[index_i][index_j] += 1
                            matrix_beta[index_i][index_j] += pontuacao_j/(pontuacao_i + pontuacao_j)
            
        if method == 'alpha':
            # add some perturbation to the matrix
            perturbed_W = matrix_alpha + 0.00001 * np.ones(matrix_alpha.shape)

            # get d vector, d=(W + W^T)1, where 1 is a vector of ones 
            d = np.dot(perturbed_W + perturbed_W.T, np.ones(perturbed_W.shape[0]))

            # perron frobeniun eigenvector of D^-1 W
            eigenvalues, eigenvectors = np.linalg.eig(np.dot(np.linalg.inv(np.diag(d)), perturbed_W))
            # absolute value of eigenvalues
            eigenvalues = np.abs(eigenvalues)
            idx = np.argmax(eigenvalues)
            eigenvector = eigenvectors[idx]

            # absolute value of eigenvector
            eigenvector = np.abs(eigenvector)

            # get rating dict with the name of the competitor and its rating
            self.ratings = {competitor: rating for competitor, rating in zip(competitor_to_index.keys(), eigenvector)}
        
        elif method == 'beta':
            matrix_beta = np.nan_to_num(matrix_beta)

            # add some perturbation to the matrix
            perturbed_S = matrix_beta + 0.0001*np.ones(matrix_beta.shape)

            d = np.dot(perturbed_S + perturbed_S.T, np.ones(perturbed_S.shape[0]))

            # create empty K matrix with same size as matrix_beta
            K = np.zeros(perturbed_S.shape)

            # for entry (i, j) in beta matrix, define h = ((i, j) + 1)/((i, j) + (j, i) + 2)
            for i in range(n_players):
                for j in range(n_players):
                    x = (perturbed_S[i][j] + 1)/(perturbed_S[i][j] + perturbed_S[j][i] + 2)
                    h = 1/2 + 1/2 * np.sign(x - 1/2) * np.sqrt(abs(2*x - 1))
                    K[i][j] = h

            # perron frobenius eigenvector of D^-1 K
            eigenvalues, eigenvectors = np.linalg.eig(np.dot(np.linalg.inv(np.diag(d)), K))
            idx = np.argmax(eigenvalues)
            eigenvector = eigenvectors[idx]

            # get rating dict with the name of the competitor and its rating
            self.ratings = {competitor: rating for competitor, rating in zip(competitor_to_index.keys(), eigenvector)}
    
    def keeners_error(self, rating_a, rating_b, real_result):
        winning_prob_a = 9.13*rating_a + 0.07
        winning_prob_b = 9.13*rating_b + 0.07

        prob = (winning_prob_b)/(winning_prob_a + winning_prob_b)
        return real_result - prob

    def error(self, data):
        """Calculates the error of the model

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
        """

        error = 0
        count = 0
        for i in range(len(data)):
            results = data[i][0]
            names = data[i][1]
            for j in range(len(results)):
                for k in range(j+1, len(results)):
                    r = results[j] < results[k]
                    if self.ratings.get(names[j]) is not None and self.ratings.get(names[k]) is not None:
                        error_update = self.keeners_error(self.ratings[names[j]], self.ratings[names[k]], r)
                        error += abs(error_update)
                        count += 1

        return error/count
        

    def k_fold(self, data, competitions, data_full):
        """ ESSE MÉTODO AINDA PODE MUDAR EU ACHO
        Calculates the error of the model using k-fold cross validation

        Args:
            data (list): List of tuples containing in position 0 the results of the matches and in position 1 the names of the players
                        both results and names are lists of the same length
                        Data represents one sailing class i.e. 49er, 470, etc.
                        Each tuple represents one competition i.e. 2020 Worlds, 2021 Euros, etc.
        """

        total_error = 0
        if self.time_decay:
            print("entrou no time decay do kfold")
            # test data should use 2020 onwards data
            # train data should use all data
            competitions_2020_onwards = []
            competitions_2020_onwards_idx = []
            for idx, competition in enumerate(competitions):
                year = int(re.findall(r'\d{4}', competition)[0])
                if year >= 2020:
                    competitions_2020_onwards.append(competition)
                    competitions_2020_onwards_idx.append(idx)

            for i in range(len(competitions_2020_onwards)):
                competition = competitions_2020_onwards[i]
                idx = competitions_2020_onwards_idx[i]
                # train data should use all data except this competition
                train = data_full[data_full['Nome Competição'] != competition]
                test = data[idx:idx+1]
                self.fit(train, time_decay=True, method='beta')
                total_error += self.error(test)
            print(total_error/len(competitions_2020_onwards))
            return total_error / len(competitions_2020_onwards)

        else:
            for i in range(len(data)):
                competition = competitions[i]
                # get from data_full the data for this competition
                train = data_full[data_full['Nome Competição'] != competition]
                test = data[i:i+1]
                self.fit(train, time_decay=False, method='beta')
                total_error += self.error(test)
            print(total_error/len(data))
            return total_error/len(data)

# # get error of keeners
# error = keeners.error(data_dict)
# print(error)


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