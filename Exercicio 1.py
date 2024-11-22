from bs4 import BeautifulSoup
import pandas as pd

# carrega o arquivo 
with open('exemplo.html', 'r', encoding='utf-8') as file:
    documento = BeautifulSoup(file, 'html.parser')
                                            
articles = documento.find_all('article')

# extrai os dados
dados = []
for article in articles:
    if article.find('h3'):
        titulo = article.find('h3').get_text(strip=True)
    else:
        titulo = None

    if article.find('p'):
        conteudo = article.find('p').get_text(strip=True)
    else:
        conteudo = None
    
    dados.append({'Titulo': titulo, 'Conteudo': conteudo})


df = pd.DataFrame(dados)
print(df)
