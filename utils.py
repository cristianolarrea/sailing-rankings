import pandas as pd
import requests

def rename_fleet(fleet: str):
    if fleet == 'medal':
        return 'MR'
    elif fleet == 'gold':
        return 'G'
    elif fleet == 'silver':
        return 'S'
    elif fleet == 'bronze':
        return 'B'
    else:
        return 'G'

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
    extracted_data['Flotilha'] = extracted_data['Flotilha'].apply(rename_fleet)

    extracted_data.to_excel(f'results/{reference["Nome Competição"]}_{reference["Classe Vela"]}.xlsx', index=False)
    
    return extracted_data