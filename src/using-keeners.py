from models import *
import pandas as pd

# read data and choose class
data = pd.read_excel('./data/final_data.xlsx')
data = data[data['Classe Vela'] == '49er']

for competition in data['Nome Competição']:
    data.loc[data['Nome Competição'] == competition, 'Ano'] = int(re.findall(r'\d{4}', competition)[0])

# split train/test 
train = data[~data['Nome Competição'].isin(['Trofeo S.A.R Princesa Sofia 2023', 'World Championship 2023'])]
data = train

keeners = Keeners()
keeners.fit(data, time_decay=False, method='alpha')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('./rankings/keenersalpha-49er-trainset.csv')


keeners = Keeners()
keeners.fit(data, time_decay=True, method='alpha')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('./rankings/keenersalphatime-49er-trainset.csv')


keeners = Keeners()
keeners.fit(data, time_decay=False, method='beta')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('./rankings/keenersbeta-49er-trainset.csv')


keeners = Keeners()
keeners.fit(data, time_decay=True, method='beta')
ratings = keeners.ratings

ratings = pd.DataFrame.from_dict(ratings, orient='index', columns=['Rating'])
ratings.to_csv('./rankings/keenersbetatime-49er-trainset.csv')