import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Para realizar a solicitação à página temos que informar ao site que somos um navegador
e é para isso que usamos a variável headers
"""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# Lista de URLs
urls_identifiers = [
    {"url": "https://www.transfermarkt.com.br/america-mineiro/leistungsdaten/verein/2863/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp": "BRA1", "ano": "2022", "time": "América Mineiro"},
    {"url": "https://www.transfermarkt.com.br/america-mineiro/leistungsdaten/verein/2863/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp": "BRA1", "ano": "2023", "time": "América Mineiro"},
    {"url": "https://www.transfermarkt.com.br/athletico-paranaense/leistungsdaten/verein/679/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp": "BRA1", "ano": "2022", "time": "Athletico Paranaense"},
    {"url": "https://www.transfermarkt.com.br/athletico-paranaense/leistungsdaten/verein/679/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Athletico Paranaense"},
    {"url": "https://www.transfermarkt.com.br/atletico-goianiense/leistungsdaten/verein/15172/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Atlético Goianiense"},
    {"url": "https://www.transfermarkt.com.br/atletico-mineiro/leistungsdaten/verein/330/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Atlético Mineiro"},
    {"url": "https://www.transfermarkt.com.br/atletico-mineiro/leistungsdaten/verein/330/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Atlético Mineiro"},
    {"url": "https://www.transfermarkt.com.br/avai-fc/leistungsdaten/verein/2035/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp": "BRA1", "ano": "2022", "time": "Avaí FC"},
    {"url": "https://www.transfermarkt.com.br/botafogo-fr/leistungsdaten/verein/537/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Botafogo FR"},
    {"url": "https://www.transfermarkt.com.br/botafogo-fr/leistungsdaten/verein/537/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Botafogo FR"},
    {"url": "https://www.transfermarkt.com.br/cr-flamengo/leistungsdaten/verein/614/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"CR Flamengo"},
    {"url": "https://www.transfermarkt.com.br/cr-flamengo/leistungsdaten/verein/614/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"CR Flamengo"},
    {"url": "https://www.transfermarkt.com.br/cr-vasco-da-gama/leistungsdaten/verein/978/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"CR Vasco da Gama"},
    {"url": "https://www.transfermarkt.com.br/ceara-sc/leistungsdaten/verein/2029/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Ceará SC"},
    {"url": "https://www.transfermarkt.com.br/coritiba-fc/leistungsdaten/verein/776/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Coritiba FC"},
    {"url": "https://www.transfermarkt.com.br/coritiba-fc/leistungsdaten/verein/776/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Coritiba FC"},
    {"url": "https://www.transfermarkt.com.br/cruzeiro-ec/leistungsdaten/verein/609/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Cruzeiro EC"},
    {"url": "https://www.transfermarkt.com.br/cuiaba-ec/leistungsdaten/verein/28022/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Cuiabá EC"},
    {"url": "https://www.transfermarkt.com.br/cuiaba-ec/leistungsdaten/verein/28022/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Cuiabá EC"},
    {"url": "https://www.transfermarkt.com.br/ec-bahia/leistungsdaten/verein/10010/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"EC Bahia"},
    {"url": "https://www.transfermarkt.com.br/ec-juventude/leistungsdaten/verein/10492/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"EC Juventude"},
    {"url": "https://www.transfermarkt.com.br/fluminense-fc/leistungsdaten/verein/2462/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Fluminense FC"},
    {"url": "https://www.transfermarkt.com.br/fluminense-fc/leistungsdaten/verein/2462/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Fluminense FC"},
    {"url": "https://www.transfermarkt.com.br/fortaleza-ec/leistungsdaten/verein/10870/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Fortaleza EC"},
    {"url": "https://www.transfermarkt.com.br/fortaleza-ec/leistungsdaten/verein/10870/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Fortaleza EC"},
    {"url": "https://www.transfermarkt.com.br/goias-ec/leistungsdaten/verein/3197/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Goiás EC"},
    {"url": "https://www.transfermarkt.com.br/goias-ec/leistungsdaten/verein/3197/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Goiás EC"},
    {"url": "https://www.transfermarkt.com.br/gremio-fbpa/leistungsdaten/verein/210/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Grêmio FBPA"},
    {"url": "https://www.transfermarkt.com.br/rb-bragantino/leistungsdaten/verein/8793/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"RB Bragantino"},
    {"url": "https://www.transfermarkt.com.br/rb-bragantino/leistungsdaten/verein/8793/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"RB Bragantino"},
    {"url": "https://www.transfermarkt.com.br/sc-corinthians/leistungsdaten/verein/199/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"SC Corinthians"},
    {"url": "https://www.transfermarkt.com.br/sc-corinthians/leistungsdaten/verein/199/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"SC Corinthians"},
    {"url": "https://www.transfermarkt.com.br/sc-internacional/leistungsdaten/verein/6600/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"SC Internacional"},
    {"url": "https://www.transfermarkt.com.br/sc-internacional/leistungsdaten/verein/6600/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"SC Internacional"},
    {"url": "https://www.transfermarkt.com.br/se-palmeiras/leistungsdaten/verein/1023/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"SE Palmeiras"},
    {"url": "https://www.transfermarkt.com.br/se-palmeiras/leistungsdaten/verein/1023/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"SE Palmeiras"},
    {"url": "https://www.transfermarkt.com.br/santos-fc/leistungsdaten/verein/221/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Santos FC"},
    {"url": "https://www.transfermarkt.com.br/santos-fc/leistungsdaten/verein/221/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Santos FC"},
    {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/leistungsdaten/verein/585/plus/1?reldata=BRA1%262022", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
    {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/leistungsdaten/verein/585/plus/1?reldata=BRA1%262021", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"São Paulo FC"}
]
# Lista para armazenar os dados
dados_completos = []
for item in urls_identifiers:
    url = item["url"]
    identifier = item["identifier"]
    camp = item["camp"]
    ano = item["ano"]
    time = item["time"]
    print(f"Processando: {item['identifier']} - {item['time']}")
# no objeto_response iremos realizar o download da página da web 
    objeto_response = requests.get(url, headers=headers)

    """
    Agora criaremos um objeto BeautifulSoup a partir do nosso objeto_response.
    O parâmetro 'html.parser' representa qual parser usaremos na criação do nosso objeto,
    um parser é um software responsável por realizar a conversão de uma entrada para uma estrutura de dados.
    """
    pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')

    tabela = pagina_bs.find_all("div",{"class":"responsive-table"})
    rows = tabela[0].find_all("tr",{"class":["odd","even"]})
    data = []
    for row in rows:
        # Nome Jogador
        names = row.find_all("span",{"class":"hide-for-small"})
        values = [val.get_text(strip=True) for val in names]
        values = [values[-1]]
        # Id jogador
        links = [val.find("a") for val in names]
        link = [val.get('href') for val in links]
        id_jogadores = [val.split('/')[-1] for val in link]
        values += [id_jogadores[-1]]
        # Estatisticas
        infos = row.find_all("td",{"class":"zentriert"})
        values += [val.get_text(strip=True) for val in infos]
        # Minutos Jogados
        minutes = row.find_all("td",{"class":"rechts"})
        values += [val.get_text(strip=True) for val in minutes]
        # Adicionar ao dataset
        if values:  # Ignorar linhas vazias   
            data.append(values+[identifier]+[camp]+[ano]+[time])  # Adiciona o tipo ao final
    dados_completos+=data
# Criar o DataFrame
columns = ['Jogador',"ID_Jogador",'Numero','Idade','Nacionalidade','No_plantel','Jogos','Gols','Assistencias','Cartoes_amarelos','Expulsoes_dois_amarelos','Expulsoes_vermelho_direto','Suplente_utilizado','Substituicoes','Pontos_por_jogo','Minutos_jogados','Identifier','Camp','Ano','Time']
df = pd.DataFrame(dados_completos, columns=columns)
df.to_csv('C:/Users/victo/OneDrive/Documentos/TCC/TCC Victor/01.Bases/TB_Empilhada_Estatisticas.csv', index=False)
print(df)
