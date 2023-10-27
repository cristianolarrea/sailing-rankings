from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd

def is_data(css_class):
    return css_class=="odd summaryrow" or css_class=="even summaryrow"

def rename_fleet(fleet):
    if fleet == 'Gold':
        fleet = 'O'
    elif fleet == 'Silver':
        fleet = 'P'
    elif fleet == 'Bronze':
        fleet = 'B'
    return fleet

def rank_to_int(rank):
    # if rank has 'st', 'nd', 'rd' or 'th' in it, remove it
    if rank[-2:] in ['st', 'nd', 'rd', 'th']:
        rank = rank[:-2]
    return int(rank)

def add_columns(df, CAMPEONATO, ID_CAMPEONATO, CLASSE):
    """
    Recebe o dataframe, o nome do campeonato, o ID da competição e a classe.
    Retorna o dataframe com as colunas adicionadas.
    Also reorders the columns.
    """
    df['Nome Competição'] = [CAMPEONATO] * len(df)
    df['ID Competição'] = [ID_CAMPEONATO] * len(df)
    df['Classe Vela'] = [CLASSE] * len(df)
    df['Punição'] = [''] * len(df)
    
    column_order = ['Nome Competidor', 'ID Competição', 'Classe Vela', 'Pontuação Regata',
                    'Flotilha', 'Posição Geral', 'Punição', 'Pontuação Total', 
                    'Nett', 'Nome Competição']

    df = df[column_order]
    
    df.to_excel(f'results/{CAMPEONATO}_{CLASSE}.xlsx', index=False)
    
    return df

def extract_and_melt(URL, CAMPEONATO, ID_CAMPEONATO, CLASSE, COLUNAS):
    """
    Instancia o webdriver, acessa a URL, extrai os dados da tabela e transforma em um dataframe.
    O dataframe retornado passa por uma mudança de formato, de wide para long, usando a função melt.
    Retorna o dataframe com as colunas adicionadas.
    """
    options = Options()
    options.add_argument("--headless")
    
    PATH_TO_CHROMEDRIVER = 'chromedriver-mac-x64/chromedriver'
    
    driver = Chrome(PATH_TO_CHROMEDRIVER, options=options)
    driver.get(URL)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    
    data = []
    for row in soup.find_all(class_ = is_data):
        resultados = []
        for cell in row.find_all('td'):
            resultados.append(cell.text)
        data.append(resultados)
        
    # turn data into a pandas dataframe
    df = pd.DataFrame(data)
     
    # change column names
    df.columns = COLUNAS
    
    if CAMPEONATO.startswith('European Championship'):
        df.drop('Nat', axis=1, inplace=True)
        df.drop('Sail Number', axis=1, inplace=True)
        df.drop('Trophy', axis=1, inplace=True)
        
    elif CAMPEONATO.startswith('World Championship'):
        df.drop('Sail', axis=1, inplace=True)
        df.drop('ISAF ID', axis=1, inplace=True)
        df.drop('MNA', axis=1, inplace=True)
        
    COLUNAS = list(df.columns)
        
    # get last 2 and first 5 items in list colunas
    last_two = COLUNAS[-2:]
    first_three = COLUNAS[:3]
    id_vars = last_two + first_three
    
    # the rest are the columns that will be turned into rows
    value_vars = COLUNAS[3:-2]
    
    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars)
    
    # rename column 'variable' to 'Flotilha'
    df.rename(columns={'value': 'Pontuação Regata'}, inplace=True)
    df.drop('variable', axis=1, inplace=True)
    
    df['Posição Geral'] = df['Posição Geral'].apply(rank_to_int)
    df['Flotilha'] = df['Flotilha'].apply(rename_fleet)
    
    df = add_columns(df = df, 
                     CAMPEONATO = CAMPEONATO, 
                     ID_CAMPEONATO = ID_CAMPEONATO, 
                     CLASSE = CLASSE)
    
    return df