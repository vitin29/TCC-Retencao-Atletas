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
        {"url": "https://www.transfermarkt.com.br/atletico-mineiro/kader/verein/330/saison_id/2021/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/atletico-mineiro/kader/verein/330/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"Atlético Mineiro"},
        {"url": "https://www.transfermarkt.com.br/atletico-mineiro/kader/verein/330/saison_id/2021/plus/1", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"Atlético Mineiro"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2022/plus/1", "identifier": "BRA1_2023", "camp":"BRA1", "ano":"2023", "time":"São Paulo FC"},
        {"url": "https://www.transfermarkt.com.br/sao-paulo-fc/kader/verein/585/saison_id/2021/plus/1", "identifier": "BRA1_2022", "camp":"BRA1", "ano":"2022", "time":"São Paulo FC"},
]
# Lista para armazenar os dados
dados_completos = []

# Loop pelas URLs
for item in urls_identifiers:
    url = item["url"]
    identifier = item["identifier"]
    camp = item["camp"]
    ano = item["ano"]
    time = item["time"]
    print(identifier+" "+time)
    # no objeto_response iremos realizar o download da página da web 
    objeto_response = requests.get(url, headers=headers)

    """
    Agora criaremos um objeto BeautifulSoup a partir do nosso objeto_response.
    O parâmetro 'html.parser' representa qual parser usaremos na criação do nosso objeto,
    um parser é um software responsável por realizar a conversão de uma entrada para uma estrutura de dados.
    """
    pagina_bs = BeautifulSoup(objeto_response.content, 'html.parser')

    nomes_jogadores = []  # Lista para armazenar os nomes de todos os jogadores

    # O método find_all() retorna todas as tags <a> com a classe "hauptlink", mas dentro de <td> na tabela
    tags_jogadores = pagina_bs.find_all("td", {"class": "hauptlink"}) 

    # Agora extraímos somente os textos correspondentes aos nomes dos jogadores
    for tag_jogador in tags_jogadores:
        nomes_jogadores.append(tag_jogador.text.strip())  # Adiciona o nome, removendo espaços extras

    # Transformar o array em um DataFrame com colunas específicas
    columns = ['Nome Jogador', 'Valor Mercado']
    data_split = [nomes_jogadores[i:i+2] for i in range(0, len(nomes_jogadores), 2)]  # Quebra a lista em grupos de 3
    df1 = pd.DataFrame(data_split, columns=columns)

    pais_jogadores = [] # Lista ordenada dos nomes do país da liga de origem de todos os jogadores

    tags_ligas = pagina_bs.find_all("td",{"class": "zentriert"})
    # Agora iremos receber todas as células da tabela que não possuem classe

    for tag_liga in tags_ligas:
        # A função find irá encontrar a primeira imagem cuja classe é "flaggenrahmen" e possui um título
        imagem_pais = tag_liga.find("img", {"class": "flaggenrahmen"}, {"title":True})
        # A variável imagem_país será uma estrutura com todas as informações da imagem,
        # uma delas é o title que contem o nome do país da bandeira
        if(imagem_pais != None): # Testaremos se o método encontrou alguma correspondência
            pais_jogadores.append(imagem_pais['title'])

    # Criando um DataFrame a partir de nossos dados
    df2 = pd.DataFrame({"País de Origem":pais_jogadores})
    df = pd.concat([df1, df2], axis=1)


    posicao_time = []
    tags_posicao = pagina_bs.find_all("td",{"class":"posrela"})
    for tag_posicao in tags_posicao:
        texto_nome = tag_posicao.text
        posicao_time.append(texto_nome.strip())
    posicao_time

    data2 = [jogador.strip().split("\n\n\n\n\n") for jogador in posicao_time]
    df5 = pd.DataFrame(data2, columns=["Nome Jogador", "Posição"])
    df5

    df['Nome Jogador'] = df['Nome Jogador'].str.strip()
    df5['Nome Jogador'] = df5['Nome Jogador'].str.strip()


    df = pd.merge(df, df5, on='Nome Jogador', how='left')

    infos_time = []

    tags_infos = pagina_bs.find_all("td", {"class":"zentriert"})
    tags_infos[0].text
    for tag_info in tags_infos:
        texto_info = tag_info.text
        infos_time.append(texto_info)

    import numpy as np
    # Transformar o vetor em um array NumPy e reorganizá-lo para ter 8 colunas
    array = np.array(infos_time).reshape(-1, 8)

    # Criar o DataFrame a partir do array
    df6 = pd.DataFrame(array, columns=[f'Coluna_{i+1}' for i in range(8)])
    novos_nomes = ['Numero_da_Camisa', 'Data_de_Nascimento', 'Nacionalidade', 'Clube_Atual', 'Altura', 'Pe', 'No_time_desde','Anterior']

    df6.columns = novos_nomes
    df_chaves = []
    df_chaves = df_chaves.append([identifier],[camp],[ano],[time])
    df_chaves = pd.DataFrame(df_chaves)
    
    df0 = pd.concat([df,df6[["Numero_da_Camisa","Data_de_Nascimento","Altura","Pe","No_time_desde"]],df_chaves],axis=1)
# exportando os dados que obtemos
df0.to_csv('C:/Users/victo/OneDrive/Documentos/TCC/TCC Victor/01.Bases/TB_Empilhada_Jogadores.csv', index=False)
print(df0)