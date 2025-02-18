import requests
from bs4 import BeautifulSoup
import pandas as pd

# Headers para simular um navegador
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Lista de URLs
urls_identifiers = [
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/transfers/wettbewerb/BRA1/plus/?saison_id=2023&s_w=w&leihe=1&intern=0", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023"},
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/transfers/wettbewerb/BRA1/plus/?saison_id=2022&s_w=w&leihe=1&intern=0", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022"},
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/transfers/wettbewerb/BRA1/plus/?saison_id=2021&s_w=w&leihe=1&intern=0", "identifier": "BRA1_2021", "camp":"BRA1", "ano":"2021"},
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-b/transfers/wettbewerb/BRA2/plus/?saison_id=2023&s_w=w&leihe=1&intern=0", "identifier": "BRA2_2023", "camp":"BRA2", "ano":"2023"},
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-b/transfers/wettbewerb/BRA2/plus/?saison_id=2022&s_w=w&leihe=1&intern=0", "identifier": "BRA2_2022", "camp":"BRA2", "ano":"2022"},
    {"url": "https://www.transfermarkt.com.br/campeonato-brasileiro-serie-b/transfers/wettbewerb/BRA2/plus/?saison_id=2021&s_w=w&leihe=1&intern=0", "identifier": "BRA2_2021", "camp":"BRA2", "ano":"2021"}
]
# Lista para armazenar os dados
dados_completos = []

# Loop pelas URLs
for item in urls_identifiers:
    url = item["url"]
    identifier = item["identifier"]
    camp = item["camp"]
    ano = item["ano"]
    print(identifier)
    # Fazer o request para a página
    objeto_response = requests.get(url, headers=headers)
    pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')

    # Encontrar a seção principal
    box = pagina_bs.find_all("div", {"class": "box"})
    for b in box:
        times = b.find_all("h2", {"class": "content-box-headline content-box-headline--inverted content-box-headline--logo"})
        times = [val.get_text(strip=True) for val in times]
        if times:
            # Encontrar as tabelas
            tables = b.find_all("div", {"class": "responsive-table"})
            for idx, table in enumerate(tables):
                tipo = 'Entrada' if idx % 2 == 0 else 'Saída'  # Alterna entre Entrada e Saída
                rows = table.find_all("tr")
                for row in rows:
                    #nome jogador
                    names = row.find_all("span", {"class": "hide-for-small"})
                    values = [val.get_text(strip=True) for val in names]
                    #id_jogador
                    links = [val.find("a") for val in names]
                    link = [val.get('href') for val in links]
                    values += [val.split('/')[-1] for val in link]
                    #destinos
                    destinos = row.find_all("td", {"class": "no-border-links verein-flagge-transfer-cell"})
                    values += [val.get_text(strip=True) for val in destinos]
                    #Quantia_Paga
                    quantias = row.find_all("td", {"class": ["rechts bg_gelb_20", "rechts ", "rechts bg_blau_20"]})
                    values += [val.text for val in quantias]

                    # Adicionar ao dataset
                    if values:
                        dados_completos.append([identifier]+[camp]+[ano]+ times + [tipo] + values)  # Adiciona o tipo ao final

# Criar o DataFrame com todos os dados empilhados
columns = ['identifier','camp','ano','Time', 'Status', 'Jogador',"ID_Jogador", 'Destino', 'Quantia_Paga']
df_final = pd.DataFrame(dados_completos, columns=columns)

# Exportar para CSV
df_final.to_csv('C:/Users/victo/OneDrive/Documentos/TCC/TCC Victor/01.Bases/TB_Transferencias_Empilhada.csv', index=False)

# Exibir os primeiros registros
print(df_final.head(11))

