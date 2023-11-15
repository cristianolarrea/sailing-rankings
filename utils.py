from bs4 import BeautifulSoup
import requests
import pandas as pd

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

def rename_fleet1(fleet, classe):
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

def rename_fleet2(fleet, classe):
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

def rename_fleet3(fleet, classe):
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
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet1, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet1, args=('49erFX',))
    elif NOME_COMPETICAO == 'World Championship 2020':
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet2, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet2, args=('49erFX',))
    elif NOME_COMPETICAO == 'European Championship 2021':
        df_49er['Flotilha'] = df_49er['Flotilha'].apply(rename_fleet3, args=('49er',))
        df_49erFX['Flotilha'] = df_49erFX['Flotilha'].apply(rename_fleet3, args=('49erFX',))
        
    # drop rows where 'Pontuação Regata' is ''
    df_49er = df_49er[df_49er['Pontuação Regata'] != '']
    df_49erFX = df_49erFX[df_49erFX['Pontuação Regata'] != '']
    
    df_49er.to_excel(f'results/{NOME_COMPETICAO}_49er.xlsx', index=False)
    df_49erFX.to_excel(f'results/{NOME_COMPETICAO}_49erFX.xlsx', index=False)
    
    return df_49er, df_49erFX

def rename_fleet(fleet: str):
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
    extracted_data['Flotilha'] = extracted_data['Flotilha'].apply(rename_fleet)

    extracted_data.to_excel(f'results/{reference["Nome Competição"]}_{reference["Classe Vela"]}.xlsx', index=False)
    
    return extracted_data