from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import requests
import pandas as pd

#################################################
################### CLUSTER 8 ###################
#################################################

def iter_rows(table):
    data = []
    for row in table.find_all('tr'):
        resultados = []
        for cell in row.find_all('td'):
            if cell.find('strike'):
                cell.string = '(' + cell.string + ')'
            resultados.append(cell.get_text())
        data.append(resultados)
    return data

def rename_fleet1_cluster8(fleet, classe):
    """
    WORLD CHAMPIONSHIP 2019
    if classe == 49er
        Q17 -> MR
        else -> G
    elif classe == 49erFX
        Q17 -> MR
        Q16 -> O
        else -> G
    """
    if classe == '49er':
        if fleet == 'Q17':
            fleet = 'MR'
        else:
            fleet = 'G'
    elif classe == '49erFX':
        if fleet == 'Q17':
            fleet = 'MR'
        elif fleet == 'Q16':
            fleet = 'O'
        else:
            fleet = 'G'
    return fleet

def rename_fleet2_cluster8(fleet, classe):
    """
    WORLD CHAMPIONSHIP 2020
    if 49er
        Q13 -> MR
        Q12 -> O
        else -> G
    elif 49erFX
        Q12 -> MR
        else -> G
    """
    if classe == '49er':
        if fleet == 'Q13':
            fleet = 'MR'
        elif fleet == 'Q12':
            fleet = 'O'
        else:
            fleet = 'G'
    elif classe == '49erFX':
        if fleet == 'Q12':
            fleet = 'MR'
        else:
            fleet = 'G'
    return fleet

def rename_fleet3_cluster8(fleet, classe):
    """
    EUROPEAN CHAMPIONSHIP 2021
    if classe == 49er
        Q12, Q13, Q14, Q15 -> MR
        else -> G
    elif classe == 49erFX
        Q15 -> MR
        else -> G
    """
    if classe == '49er':
        if fleet in ['Q12', 'Q13', 'Q14', 'Q15']:
            fleet = 'MR'
        else:
            fleet = 'G'
    elif classe == '49erFX':
        if fleet == 'Q15':
            fleet = 'MR'
        else:
            fleet = 'G'
    return fleet


def cluster8(URL: str, PATH_TO_CHROMEDRIVER: str, NOME_COMPETICAO: str, ID_COMPETICAO: int, DRIVER):
    DRIVER.get(URL)
    html = DRIVER.page_source
    
    soup = BeautifulSoup(html, 'html.parser')
    
    result_49er = True
    for table in soup.find_all('table'):
        if result_49er == True:
            data_49er = iter_rows(table)
            result_49er = False
        else:
            data_49erFX = iter_rows(table)
            
    df_49er = pd.DataFrame(data_49er[1:])
    df_49erFX = pd.DataFrame(data_49erFX[1:])
    
    columns = ['Posição Geral', 'Sail Number', 'Nome Competidor', 'Nett', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 
              'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Pontuação Total']
    
    df_49er.columns = columns
    df_49erFX.columns = columns
    
    df_49er.drop('Sail Number', axis=1, inplace=True)
    df_49erFX.drop('Sail Number', axis=1, inplace=True)
    
    df_49er = pd.melt(df_49er, id_vars=['Posição Geral', 'Nome Competidor', 'Nett', 'Pontuação Total'],
                      value_vars=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8',
                                  'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17'])
    
    df_49erFX = pd.melt(df_49erFX, id_vars=['Posição Geral', 'Nome Competidor', 'Nett', 'Pontuação Total'],
                        value_vars=['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8',
                                    'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17'])
    
    df_49er.rename(columns={'variable': 'Flotilha', 'value': 'Pontuação Regata'}, inplace=True)
    df_49erFX.rename(columns={'variable': 'Flotilha', 'value': 'Pontuação Regata'}, inplace=True)
    
    df_49er['Nome Competição'] = [NOME_COMPETICAO] * len(df_49er)
    df_49erFX['Nome Competição'] = [NOME_COMPETICAO] * len(df_49erFX)
    
    df_49er['ID Competição'] = [ID_COMPETICAO] * len(df_49er)
    df_49erFX['ID Competição'] = [ID_COMPETICAO] * len(df_49erFX)
    
    df_49er['Classe Vela'] = ['49er'] * len(df_49er)
    df_49erFX['Classe Vela'] = ['49erFX'] * len(df_49erFX)
    
    df_49er['Punição'] = [''] * len(df_49er)
    df_49erFX['Punição'] = [''] * len(df_49erFX)
    
    column_order = ['Nome Competidor', 'ID Competição', 'Classe Vela',
                    'Pontuação Regata', 'Flotilha', 'Posição Geral', 
                    'Punição', 'Pontuação Total', 'Nett', 'Nome Competição']
    
    df_49er = df_49er[column_order]
    df_49erFX = df_49erFX[column_order]
    
    if NOME_COMPETICAO == 'World Championship 2019':
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet1_cluster8, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet1_cluster8, args=('49erFX',))
    elif NOME_COMPETICAO == 'World Championship 2020':
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet2_cluster8, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet2_cluster8, args=('49erFX',))
    elif NOME_COMPETICAO == 'European Championship 2021':
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet3_cluster8, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet3_cluster8, args=('49erFX',))
        
    # drop rows where 'Pontuação Regata' is ''
    df_49er = df_49er[df_49er['Pontuação Regata'] != '']
    df_49erFX = df_49erFX[df_49erFX['Pontuação Regata'] != '']
    
    df_49er.to_excel(f'scraped-data/{NOME_COMPETICAO}_49er.xlsx', index=False)
    df_49erFX.to_excel(f'scraped-data/{NOME_COMPETICAO}_49erFX.xlsx', index=False)
    
    return df_49er, df_49erFX

#################################################
################### CLUSTER 9 ###################
#################################################

def rename_fleet_cluster9(fleet: str):
    if fleet == 'medal':
        return 'MEDAL RACE'
    elif fleet == 'gold':
        return 'OURO'
    elif fleet == 'silver':
        return 'PRATA'
    elif fleet == 'bronze':
        return 'BRONZE'
    else:
        return 'GERAL'

def cluster9(reference: dict):
    """
    Recebe um URL com os dados a serem extraídos e
    um dicionário com o nome da classe, nome da competição e
    identificador da competição.
    """
    r = requests.get(reference['URL'])
    data = r.json()

    extracted_data = {
        'Nome Competidor': [],
        'ID Competição': [],
        'Classe Vela': [],
        'Pontuação Regata': [],
        'Descarte': [],
        'Flotilha': [],
        'Posição Geral': [],
        'Punição': [],
        'Pontuação Total': [],
        'Nett': [],
        'Nome Competição': [],
    }
    
    data = data['EntryResults']
    
    for velejador in data:
        regatas = velejador['EntryRaceResults']
        for regata in regatas:
            extracted_data['Nome Competidor'].append(velejador['Name'] + velejador['Crew'])
            extracted_data['ID Competição'].append(reference['ID Competição'])
            extracted_data['Classe Vela'].append(reference['Classe Vela'])
            
            if regata.get('Points') != None:
                extracted_data['Pontuação Regata'].append(regata['Points'])
            else:
                extracted_data['Pontuação Regata'].append('')
            
            if regata.get('PointsDiscarded') != None:
                extracted_data['Descarte'].append(1)
            else:  
                extracted_data['Descarte'].append(0)
            
            if regata.get('Fleet') != None:
                extracted_data['Flotilha'].append(regata['Fleet'])
            else:
                extracted_data['Flotilha'].append('')
                
            extracted_data['Posição Geral'].append(velejador['Rank'])
            
            if regata.get('RaceStatusCode') != None:
                extracted_data['Punição'].append(regata['RaceStatusCode'])
            else:
                extracted_data['Punição'].append('')
            
            extracted_data['Pontuação Total'].append(velejador['TotalPoints'])
            extracted_data['Nett'].append(velejador['NetPoints'])
            extracted_data['Nome Competição'].append(reference['Nome Competição'])
            
    extracted_data = pd.DataFrame(extracted_data)
    
    # drop rows where Pontuação Regata is ''
    extracted_data = extracted_data[extracted_data['Pontuação Regata'] != '']
    extracted_data = extracted_data.dropna(subset=['Pontuação Regata'])
    extracted_data['Flotilha'] = extracted_data['Flotilha'].apply(rename_fleet_cluster9)

    extracted_data.to_excel(f'scraped-data/{reference["Nome Competição"]}_{reference["Classe Vela"]}.xlsx', index=False)
    
    return extracted_data

#################################################
################### CLUSTER 2 ###################
#################################################

def is_data(css_class):
    return css_class=="odd summaryrow" or css_class=="even summaryrow"

def rename_fleet_cluster2(fleet):
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
        df['Flotilha'] = df['Flotilha'].apply(rename_fleet_cluster2)
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
    
    df.to_excel(f'scraped-data/{CAMPEONATO}_{CLASSE}.xlsx', index=False)
    
    return df