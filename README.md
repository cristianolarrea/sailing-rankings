# sailing-rankings

Esse repositório armazena todos os scripts e resultados do projeto Fields 2023 desenvolvido em parceria da FGV EMAp com a CBVela. O desenvolvimento do projeto é de autoria de:
* Ana Carolina Erthal
* Cristiano Larréa
* Felipe Lamarca
* Guilherme de Melo
* Paloma Borges

O objetivo do projeto era criar um modelo de ranking para os competidores de classes olímpicas da vela mundial. 

## Organização do repositório

[`data`](data): 

[`eda`](eda): pasta com o arquivo [`eda.ipynb`](eda/eda.ipynb), onde foi desenvolvida uma análise mais profunda dos dados coletados, com manipulações e visualizações a partir de perguntas e hipóteses definidas pelo grupo em contato com a equipe de negócios

[`general_cleaning`](general_cleaning): pasta contendo os notebooks utilizados para a limpeza dos dados brutos coletados via webscraping
  - [`fleetPoints.ipynb`](general_cleaning/fleetPoints.ipynb): pipeline de ajustes (1) da coluna de ID do campeonato de acordo com o nome do campeonato e (2) do formato da coluna com a pontuação das regatas, tratando todos os casos atípicos
  - [`cleaning_names`](general_cleaning/cleaning_names): subpasta com o pipeline de tratamento (via código e manual) dos nomes dos competidores
  - [`duplicates_fixer.ipynb`](general_cleaning/duplicates_fixer.ipynb):

[`mapping`](mapping): script auxiliar simples para indicar quais competições já haviam tido os dados extraídos em relação à lista de competições com dados mapeados em páginas da internet

[`rankings`](rankings): 

[`scrapers`](scrapers): pasta contendo mapeamentos de páginas com súmulas, scripts para realização da raspagem de dados e os dados resultantes do scraping
  - [`clusters`](scrapers/clusters): pasta com os scripts e mapeamentos
      - [`Clusters-Sumulas.xlsx`](scrapers/clusters/Clusters-Sumulas.xlsx): mapeamento de súmulas em diferentes clusters, com imagem do estilo da página HTML
      - [`Mapeamento.xlsx`](scrapers/clusters/Mapeamento.xlsx): mapeamento de competições mais antigas de 49er, 49erFX, Ilca 6 e Ilca 7, separadas por cluster
      - Arquivos `.ipynb` para a extração dos dados de cada um dos clusters, com indicação do cluster no nome do arquivo
      - [`utils.py`](scrapers/clusters/utils.py): arquivo com funções auxiliares para padronização dos dados extraídos
  - [`scraped-data`](scrapers/scraped-data): arquivos com todos os dados extraídos
  - [`source-data`](scrapers/source-data):

[`src`](src):

