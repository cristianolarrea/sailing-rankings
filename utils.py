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

def add_columns(df, CAMPEONATO, ID_CAMPEONATO, CLASSE, FLOTILHA=None):
    """
    Recebe o dataframe, o nome do campeonato, o ID da competição e a classe.
    Retorna o dataframe com as colunas adicionadas.
    Also reorders the columns.
    """
    df['Nome Competição'] = [CAMPEONATO] * len(df)
    df['ID Competição'] = [ID_CAMPEONATO] * len(df)
    df['Classe Vela'] = [CLASSE] * len(df)
    df['Punição'] = [''] * len(df)
    
    if 'Flotilha' not in df.columns:
        if FLOTILHA != None:
            df['Flotilha'] = [FLOTILHA] * len(df)
        else:
            df['Flotilha'] = [''] * len(df)
    
    column_order = ['Nome Competidor', 'ID Competição', 'Classe Vela', 'Pontuação Regata',
                    'Flotilha', 'Posição Geral', 'Punição', 'Pontuação Total', 
                    'Nett', 'Nome Competição']

    df = df[column_order]
    
    return df

def extract_and_melt(URL, CAMPEONATO, ID_CAMPEONATO, CLASSE, COLUNAS, FLOTILHA=None, DIFFERENT_FIRST_TABLE=False, DIFFERENT_TABLE_COLUMNS=None):
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
    data2 = []
    
    for table in soup.find_all(class_ = 'summarytable'):
        
        if DIFFERENT_FIRST_TABLE:
            for row in table.find_all(class_ = is_data):
                resultados = []
                for cell in row.find_all('td'):
                    resultados.append(cell.text)
                data2.append(resultados)
            
            ### Applies full pipeline to the first table                
            df2 = pd.DataFrame(data2)

            df2.columns = DIFFERENT_TABLE_COLUMNS

            for column in df2.columns:
                if column.startswith('USELESS'):
                    df2.drop(column, axis=1, inplace=True)
                    
            DIFFERENT_TABLE_COLUMNS = list(df2.columns)
                    
            id_vars = DIFFERENT_TABLE_COLUMNS[0:2] + DIFFERENT_TABLE_COLUMNS[-1:]
            print(id_vars)
            value_vars = DIFFERENT_TABLE_COLUMNS[2:-1]
            print(value_vars)
            
            df2 = pd.melt(df2, id_vars=id_vars, value_vars=value_vars)
            
            df2.rename(columns={'value': 'Pontuação Regata'}, inplace=True)
            df2.drop('variable', axis=1, inplace=True)
            
            df2['Nett'] = df2['Pontuação Total']
            
            df2['Posição Geral'] = df2['Posição Geral'].apply(rank_to_int)
            
            df2 = add_columns(df = df2,
                                CAMPEONATO = CAMPEONATO,
                                ID_CAMPEONATO = ID_CAMPEONATO,
                                CLASSE = CLASSE,
                                FLOTILHA = 'MR')
            
            DIFFERENT_FIRST_TABLE = False
            
        else:
            ### applies standard pipeline to the rest of the tables
            for row in table.find_all(class_ = is_data):
                resultados = []
                for cell in row.find_all('td'):
                    resultados.append(cell.text)
                data.append(resultados)
    
    # turn data into a pandas dataframe
    df = pd.DataFrame(data)
     
    # change column names
    df.columns = COLUNAS
    
    for column in df.columns:
        # if column is not in column_order nor startswith Q or F, drop it
        if column.startswith('USELESS'):
            df.drop(column, axis=1, inplace=True)
        
    COLUNAS = list(df.columns)
        
    # get last 2 and first 5 items in list colunas
    if 'Flotilha' not in COLUNAS:
        last_two = COLUNAS[-2:]
        first_three = COLUNAS[:2]
        id_vars = last_two + first_three
        print(id_vars)
        
        # the rest are the columns that will be turned into rows
        value_vars = COLUNAS[2:-2]
        print(value_vars)
    else:
        last_two = COLUNAS[-2:]
        first_four = COLUNAS[:3]
        id_vars = last_two + first_four
        print(id_vars)
        
        # the rest are the columns that will be turned into rows
        value_vars = COLUNAS[3:-2]
        print(value_vars)
    
    df = pd.melt(df, id_vars=id_vars, value_vars=value_vars)
    
    # rename column 'variable' to 'Flotilha'
    df.rename(columns={'value': 'Pontuação Regata'}, inplace=True)
    df.drop('variable', axis=1, inplace=True)
    
    df['Posição Geral'] = df['Posição Geral'].apply(rank_to_int)
    
    try:
        df['Flotilha'] = df['Flotilha'].apply(rename_fleet)
    except:
        pass
    
    df = add_columns(df = df, 
                     CAMPEONATO = CAMPEONATO, 
                     ID_CAMPEONATO = ID_CAMPEONATO, 
                     CLASSE = CLASSE,
                     FLOTILHA = FLOTILHA)    

    # concat df and df2
    try:
        df = pd.concat([df, df2])
    except:
        pass
    
    df.to_excel(f'results/{CAMPEONATO}_{CLASSE}.xlsx', index=False)
    
    return df