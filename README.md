# sailing-rankings

Esse repositório armazena todos os scripts e resultados do projeto Fields 2023 desenvolvido em parceria da FGV EMAp com a CBVela. O desenvolvimento do projeto é de autoria de:
* Ana Carolina Erthal
* Cristiano Larréa
* Felipe Lamarca
* Guilherme de Melo
* Paloma Borges

O objetivo do projeto era obter os dados das competições de vela mundiais em anos passados e construor um modelo de ranking para os competidores de classes olímpicas da vela mundial. 

## Modelos de Ranking
Os modelos de ranking gerados foram:
- Elo ranking
  - Variações do parâmetro k
- Keener's Method
  - Versões _alpha_ e _beta_
  - Versões com e sem _time decay_
 
Para maiores explicações, consultar o [relatório deste projeto](Relatório.pdf).

## Organização do repositório

Link para os dados consolidados ao final do projeto: [https://docs.google.com/spreadsheets/d/1MRJr7QwXIA8lJFOOH_DVyLKqe3rxYV4r/edit?usp=sharing&ouid=113213641367731055764&rtpof=true&sd=true](https://docs.google.com/spreadsheets/d/1MRJr7QwXIA8lJFOOH_DVyLKqe3rxYV4r/edit?usp=sharing&ouid=113213641367731055764&rtpof=true&sd=true)[^1].

[`data`](data): pasta contendo os dados gerais do projeto. 
  - [`final_data.xlsx`](data/final_data.xlsx): Banco de dados completo construído durante o projeto, completamente tratado e pronto para uso
  - [`banco_sem_processamento.xlsx`](data/banco_sem_processamento.xlsx): Banco de dados obtido após o fim do processo de coleta, antes do processamento e limpeza, para controle e versionamento. Não utilizar para análises ou elaboração de rankings
  - [`banco_campeonatos.xlsx`](data/banco_campeonatos.xlsx): Arquivo contendo campeonatos presentes no banco e ids.
  - [`mapped_competitions.xlsx`](data/mapped_competitions.xlsx): Arquivo contendo cada competição presente no banco (campeonato e ano) e o link para acessar os resultados originais

[`eda`](eda): pasta com o arquivo [`eda.ipynb`](eda/eda.ipynb), onde foi desenvolvida uma análise mais profunda dos dados coletados, com manipulações e visualizações a partir de perguntas e hipóteses definidas pelo grupo em contato com a equipe de negócios

[`general_cleaning`](general_cleaning): pasta contendo os notebooks utilizados para a limpeza dos dados brutos coletados via webscraping
  - [`fleetPoints.ipynb`](general_cleaning/fleetPoints.ipynb): pipeline de ajustes (1) da coluna de ID do campeonato de acordo com o nome do campeonato e (2) do formato da coluna com a pontuação das regatas, tratando todos os casos atípicos
  - [`cleaning_names`](general_cleaning/cleaning_names): subpasta com o pipeline de tratamento (via código e manual) dos nomes dos competidores
  - [`duplicates_fixer.ipynb`](general_cleaning/duplicates_fixer.ipynb):

[`mapping`](mapping): script auxiliar simples para indicar quais competições já haviam tido os dados extraídos em relação à lista de competições com dados mapeados em páginas da internet

[`rankings`](rankings): pasta contendo os arquivos `.csv` de ranking das classes 49er, 49erFX, Ilca 6, Ilca 7
  - [`rankings`](rankings/final_results): pasta com os resultados finais para uso geral
  - [`rankings`](rankings/trainsets): pasta com os arquivos de treino para cálculo de métricas de erro

[`scrapers`](scrapers): pasta contendo mapeamentos de páginas com súmulas, scripts para realização da raspagem de dados e os dados resultantes do scraping
  - [`clusters`](scrapers/clusters): pasta com os scripts e mapeamentos
      - [`Clusters-Sumulas.xlsx`](scrapers/clusters/Clusters-Sumulas.xlsx): mapeamento de súmulas em diferentes clusters, com imagem do estilo da página HTML
      - [`Mapeamento.xlsx`](scrapers/clusters/Mapeamento.xlsx): mapeamento de competições mais antigas de 49er, 49erFX, Ilca 6 e Ilca 7, separadas por cluster
      - Arquivos `.ipynb` para a extração dos dados de cada um dos clusters, com indicação do cluster no nome do arquivo
      - [`utils.py`](scrapers/clusters/utils.py): arquivo com funções auxiliares para padronização dos dados extraídos
  - [`scraped-data`](scrapers/scraped-data): arquivos com todos os dados extraídos
  - [`source-data`](scrapers/source-data):

[`src`](src): pasta contendo os scripts associados à elaboração dos métodos de ranking (modelos e métricas)
  - [`models.py`](src/models.py): arquivo `.py` contendo a funções para execução dos modelos, desde fits a métricas de erro.
  - [`using_models.py`](src/using_models.py): arquivo exemplificando a execução de ambos os modelos
  - [`using_keeners.py`](src/using_keeners.py): arquivo exemplificando a execução específica do Keeners
  - [`using_elo.py`](src/using_elo.py): arquivo exemplificando a execução específica do Elo
  - [`keeners.py`](src/keeners.py): arquivo utilizado durante a contrução do Keeners (somente para testes e estudo do modelo, não deve ser usado para gerar rankings)
  - [`generate-elo-ranking.py`](src/generate-elo-ranking.py): arquivo utilizado durante a contrução do Elo (somente para testes e estudo do modelo, não deve ser usado para gerar rankings)
  - [`prediction_error`](src/prediction_error): arquivo utilizado durante a elaboração da métrica de erro de predição (somente para testes e estudo, não deve ser usado para gerar rankings)


    [^1]: Link de leitor, sem possibilidade de edição. No início do próximo projeto do Field Project com a CBVela, sugere-se que o novo grupo entre em contato com algum integrante do grupo anterior para a transferência de propriedade do arquivo.

