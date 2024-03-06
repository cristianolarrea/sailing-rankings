from models import *
import pandas as pd

# read data and choose class
data = pd.read_excel('../data/final_data.xlsx')
data = data[data['Classe Vela'] == '49erFX']

for competition in data['Nome Competição']:
    data.loc[data['Nome Competição'] == competition, 'Ano'] = int(re.findall(r'\d{4}', competition)[0])

# split train/test if needed
#train = data[~data['Nome Competição'].isin(['Trofeo S.A.R Princesa Sofia 2023', 'World Championship 2023'])]
#data = train

keeners = Keeners()
keeners.fit(data, time_decay=False, method='alpha')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('../rankings/keeners_alpha_49erFX.csv')

keeners = Keeners()
keeners.fit(data, time_decay=True, method='alpha')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('../rankings/keeners_alpha_time_49erFX.csv')


keeners = Keeners()
keeners.fit(data, time_decay=False, method='beta')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('../rankings/keeners_beta_49erFX.csv')


keeners = Keeners()
keeners.fit(data, time_decay=True, method='beta')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('../rankings/keeners_beta_time_49erFX.csv')