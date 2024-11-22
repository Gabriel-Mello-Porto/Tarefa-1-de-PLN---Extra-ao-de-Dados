from bs4 import BeautifulSoup
import pandas as pd
import requests


def extrair_dados(url):

    # retorna o conteudo da pagina
    conteudoDaPagina = requests.get(url)

    # torna o conteudo da pagina em um tipo BS
    pagina = BeautifulSoup(conteudoDaPagina.text, 'html.parser')

    # listas para salvar os dados
    lista_disciplinas = []
    lista_professores = []
    lista_turmas = []
    lista_vagas = []
    lista_alunos_matriculados = []

    print('\n\n')
    curriculo_versao_atual = pagina.find('div', class_='versao atual')
    num_semestres =  len(curriculo_versao_atual.find_all('table', class_='tabela-dados cor-borda'))

    for semestre in range(0, num_semestres):
        tabela_dados_atual = curriculo_versao_atual.find_all('table', class_='tabela-dados cor-borda')[semestre]
        total_tr = len(tabela_dados_atual.find_all('tr'))

        for tr_atual in range(1, total_tr, 3):
            disciplina_atual = tabela_dados_atual.find_all('tr')[tr_atual]

            # pega o nome da disciplina
            codigo_e_nome_disciplina = disciplina_atual.find('a')
            nome_disciplina = str(codigo_e_nome_disciplina).split('-')[-1].split('<')[0]          # pega o nome da disciplina
            nome_disciplina = nome_disciplina[1:]                                                 # remove o espaço extra do inicio da string
            lista_disciplinas.append(nome_disciplina)

            # pega o nome do professor
            nome_professor = disciplina_atual.find('span', class_='tabela-detalhe-info')
            nome_professor = str(nome_professor).split(':')[-1].split('<')[0]
            nome_professor = nome_professor[1:]
            lista_professores.append(nome_professor)

            # pega a turma"
            turma = disciplina_atual.find_all('td')[-3]
            lista_turmas.append(turma)

            # pega as vagas
            vagas = disciplina_atual.find_all('td')[-2]
            lista_vagas.append(vagas)

            # pega o numero de alunos matriculados
            num_alunos_matriculados = disciplina_atual.find_all('td')[-1]
            lista_alunos_matriculados.append(num_alunos_matriculados)
        
        
    # organizaçao dos dados
    dados = pd.DataFrame({ 'DISCIPLINAS': lista_disciplinas, 'PROFESSORES': lista_professores, 'TURMAS': lista_turmas, 'VAGAS': lista_vagas,'MATRICULADOS(AS)': lista_alunos_matriculados})
    print(dados)
    dados.to_csv('eng_comp.xls', index=False)



url_eng_comp = 'https://institucional.ufpel.edu.br/cursos/cod/3910'
extrair_dados(url_eng_comp)

url_ciencia_comp = 'https://institucional.ufpel.edu.br/cursos/cod/3900'
extrair_dados(url_ciencia_comp)

url_biotecnologia = 'https://institucional.ufpel.edu.br/cursos/cod/5700'
extrair_dados(url_biotecnologia)

url_eng_materiais = 'https://institucional.ufpel.edu.br/cursos/cod/6100'
extrair_dados(url_eng_materiais)

url_eng_hidrica = 'https://institucional.ufpel.edu.br/cursos/cod/6400'
extrair_dados(url_eng_hidrica)
  