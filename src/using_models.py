from models import *

# read data and choose class

data = pd.read_excel('./data/final_data.xlsx')
data = data[data['Classe Vela'] == 'Ilca 6']


# add column with year of competition
for competition in data['Nome Competição']:
    data.loc[data['Nome Competição'] == competition, 'Ano'] = int(re.findall(r'\d{4}', competition)[0])


# use keeners to get ratings
keeners = Keeners()
# keeners.fit(data, time_decay=True, method='alpha')
# ratings = keeners.ratings
# print(ratings)


# use elo to get ratings
# elo = EloRating(ratings={competitor: 1500 for competitor in data['Nome Competidor'].unique()}, k=40)


##############################################
##############################################
# GET data_dict FOR:
# 1. fit elo
# 2. get error of elo and keeners

# get data in the format needed for error calculation
data_dict = []
competitions = []
grouped_data = data.groupby(["Ano","Nome Competição", "Nome Competidor", ]).agg({"Posição Geral": "min"}
    ).sort_values(by=["Ano", "Nome Competição", "Posição Geral"], ascending=True).reset_index()

for ano in grouped_data["Ano"].unique():
    for comp in grouped_data[grouped_data["Ano"] == ano]["Nome Competição"].unique():
        # get name of competition
        competitions.append(comp)
        results = grouped_data[(grouped_data["Ano"] == ano) & (grouped_data["Nome Competição"] == comp)]["Posição Geral"].values
        names = grouped_data[(grouped_data["Ano"] == ano) & (grouped_data["Nome Competição"] == comp)]["Nome Competidor"].values
        data_dict.append([results, names])

##############################################
##############################################


# # fit elo
# elo.fit(data_dict)
# ratings = elo.ratings
# print(ratings)

# # get error of elo
# error = elo.error(data_dict)
# print(error)

# # get k-folds error of elo
# kfold_error = elo.k_fold(data_dict)
# print(kfold_error)

# get k-folds error of keeners
kfold_error = keeners.k_fold(data_dict, competitions, data)
print(kfold_error)

# ilca 6 alpha no time decay