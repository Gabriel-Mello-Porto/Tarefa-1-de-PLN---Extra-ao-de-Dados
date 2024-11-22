from bs4 import BeautifulSoup
import pandas as pd
import requests


def extrair_dados(url, numero_professores):
    
    # retorna o conteudo da pagina
    pagina_curso = requests.get(url)
    pagina_principal_soup = BeautifulSoup(pagina_curso.text, 'html.parser')

    # listas para armazenar dados
    lista_professores_cdted = []
    lista_tipo_projeto = []
    lista_resumo_projeto = []

    div_professores = pagina_principal_soup.find('div', id="professores")
    base_link = 'https://institucional.ufpel.edu.br'

    for professor in range(0, numero_professores):

        # pega o href dos professores
        cdtec = div_professores.find_all('span', string='Centro de Desenvolvimento Tecnológico')[professor]
        nome_professor = cdtec.parent
        href_link = nome_professor.get('href')

        # pega os nomes dos professores que sao do cdtec
        nome_professor = str(nome_professor.find('span')).split('>')[-2].split('<')[0]
        lista_professores_cdted.append(nome_professor)

        # acessa o link do professor atual
        link_professor = base_link + href_link + '#projetos'
        pagina_professor = requests.get(link_professor)
        pagina_professor_soup = BeautifulSoup(pagina_professor.text, 'html.parser')

        # acessa a aba de projetos
        div_projetos = pagina_professor_soup.find('div', id="projetos")

        # pega cada <tr> que contem link para um projeto
        trs_com_links = []
        if div_projetos:
            trs = div_projetos.find_all('tr') 
            for tr in trs:
                if tr.find('a'): 
                    trs_com_links.append(tr)
                    lista_professores_cdted.append(nome_professor)
            lista_professores_cdted.pop()

        for tr in trs_com_links:
        
            # pega o link de cada <tr>
            href_link_projeto = tr.find('a')['href']  
            link_projeto = base_link + href_link_projeto 

            # acessa o projeto atual
            pagina_projeto = requests.get(link_projeto) 
            pagina_projeto_soup = BeautifulSoup(pagina_projeto.text, 'html.parser')
            
            # pega o tipo de projeto
            tipo_projeto = pagina_projeto_soup.find('div', class_='ficha-campo caps').get_text()
            lista_tipo_projeto.append(tipo_projeto)

            # pega o resumo do projeto
            div_ficha = pagina_projeto_soup.find('div', class_='ficha-dados cor-borda')
            resumo_projeto = div_ficha.find_all('div')[-1].get_text()
            lista_resumo_projeto.append(resumo_projeto)

    
    # organizaçao dos dados
    dados = pd.DataFrame({ 'Professor(a)': lista_professores_cdted, 'Tipo': lista_tipo_projeto, 'Resumo': lista_resumo_projeto})
    print(dados)
    dados.to_csv('eng_comp.xls', index=False)



url_eng_comp = 'https://institucional.ufpel.edu.br/cursos/cod/3910#professores'
extrair_dados(url_eng_comp, 34)

# sem necessidade de rodar ja que sao os mesmos professores ( mas funciona ;) )
#url_ciencia_comp = 'https://institucional.ufpel.edu.br/cursos/cod/3900#professores'
#extrair_dados(url_ciencia_comp, 34)
