from models import *
import pandas as pd

# read data and choose class

data = pd.read_excel('./data/final_data.xlsx')
data = data[data['Classe Vela'] == 'Ilca 6']

elo = EloRating(ratings={competitor: 1500 for competitor in data['Nome Competidor'].unique()}, k=40)

for competition in data['Nome Competição']:
    data.loc[data['Nome Competição'] == competition, 'Ano'] = int(re.findall(r'\d{4}', competition)[0])

# split dataset, using data['Nome Competição']== 'Trofeo S.A.R Princesa Sofia 2023', 'World Championship 2023' as test set
train = data[~data['Nome Competição'].isin(['Trofeo S.A.R Princesa Sofia 2023', 'World Championship 2023'])]
data = train

# get data in the format needed for error calculation
data_dict = []
grouped_data = data.groupby(["Ano","Nome Competição", "Nome Competidor", ]).agg({"Posição Geral": "min"}
    ).sort_values(by=["Ano", "Nome Competição", "Posição Geral"], ascending=True).reset_index()

for ano in grouped_data["Ano"].unique():
    for comp in grouped_data[grouped_data["Ano"] == ano]["Nome Competição"].unique():
        results = grouped_data[(grouped_data["Ano"] == ano) & (grouped_data["Nome Competição"] == comp)]["Posição Geral"].values
        names = grouped_data[(grouped_data["Ano"] == ano) & (grouped_data["Nome Competição"] == comp)]["Nome Competidor"].values
        data_dict.append([results, names])
        
elo.fit(data_dict)
ratings = elo.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('./rankings/elo40-ilca6-trainset.csv')