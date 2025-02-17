from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import datetime
from datetime import datetime
import calendar
import dateparser
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa sem abrir o navegador
chrome_options.add_argument("--disable-gpu")  # Evita alguns bugs gráficos no headless
chrome_options.add_argument("--window-size=1920x1080")  # Garante renderização correta

# Inicializa o WebDriver do Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def executar_scraping(url, estado, n_cliques):
    # trocar o link para trocar cidades, funiona para qualquer cidade
    # ideia: criar uma lista com links de diversas cidades e rodar o programa todo
    driver.get(url)
    main_window = driver.current_window_handle

    # Aguarda alguns segundos para carregar o JavaScript (ajuste conforme necessário)
    time.sleep(2)

    


    # Aumentar o range para aumentar o numero de imoveis
    for i in range(n_cliques):
        try:
            see_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "see-more"))
            )
             # Clica no botão
            see_more_button.click()
        except:
            print('Botão de visualizar mais não encontrado')
       

    cards = driver.find_elements(By.CLASS_NAME, "StyledLink_styledLink__P_6FN")
    
    precos = []
    num_quartos = []
    num_banheiros = []
    num_vagas = []
    m_quadrados = []
    tempos_publi = []
    itens_disponiveis = []
    itens_indisponiveis = []
    tipos_imoveis = []
    cidades = []
    regioes = []
    
    
    for i,card in enumerate(cards):
        href = card.get_attribute("href")
        
        html = requests.get(href).content
        soup = BeautifulSoup(html, 'html.parser')
        
        preco = soup.find('div', {'class': 'PriceTableSale_price__dexUu'})
        infos = soup.find_all('div', {'class': 'MuiBox-root mui-15au7ed'})
        spans = soup.find_all('span')
        tipo_imovel = soup.find_all('h1')

        
        # a lista de disponiveis fica no indice 0, e de indisponiveis no indice 1
        itens = soup.find_all('div', {'class': 'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-6 mui-1s50f5r'})
        
        # tratamento, pois nem todos imoveis possuem itens disponiveis
        # cria vetores aux para itens disponiveis e indisponiveis de cada umovel
        disponivel_aux = []
        indisponivel_aux = []
        
        try:
            itens_disponivels_pagina = itens[0].find_all('div', {'class': 'AmenitiesList_itemsWrapper__PLY3c'})
            
            for item in itens_disponivels_pagina:
                try:
                    disponivel_aux.append(item.text)
                except IndexError:
                        disponivel_aux.append(np.nan)
            itens_disponiveis.append(disponivel_aux)
        except IndexError:
            itens_disponiveis.append(np.nan)
            
        
        
        try:
            itens_indisponivels_pagina = itens[1].find_all('div', {'class': 'AmenitiesList_itemsWrapper__PLY3c'})
            
            for item in itens_indisponivels_pagina:
                try:
                    indisponivel_aux.append(item.text)
                except IndexError:
                    indisponivel_aux.append(np.nan)
            itens_indisponiveis.append(indisponivel_aux)
        except:
            itens_indisponiveis.append(np.nan)
        
        # o tipo do imovelsempre éo primeiro h1, então é valido fazer
        tipos_imoveis.append(tipo_imovel[0].text)
        
        # o período de publicação é sempre um span, e sempre esta no índice 106, então é possível fazer a seguinte operação
        tempos_publi.append(spans[106].text)
        
        # cidade e regiao sao sempre spans, na posição 100 e 101, entao é valido
        cidades.append(spans[100].text)
        regioes.append(spans[101].text)
        
        precos.append(preco.text)
        
        try:
            num_quartos.append(infos[0].text)
            m_quadrados.append(infos[1].text)
            num_vagas.append(infos[3].text)
            num_banheiros.append(infos[4].text)
        except IndexError:
            num_quartos.append(np.nan)
            m_quadrados.append(np.nan)
            num_vagas.append(np.nan)
            num_banheiros.append(np.nan)
        
    
    
    for i, tipo_imovel in enumerate(tipos_imoveis):
        tipo_imovel = str(tipo_imovel)
        tipos_imoveis[i] = tipo_imovel.split()[0] 
    
    for i, quarto in enumerate(num_quartos):
        quarto = str(quarto)
        num_quartos[i] = quarto.split()[0] 
        
    for i, tamanho in enumerate(m_quadrados):
        if isinstance(tamanho, str) and tamanho.strip():  
            m_quadrados[i] = tamanho.split()[0]
        else:
            m_quadrados[i] = str(tamanho).split()[0] 
    
    for i, vaga in enumerate(num_vagas):
        vaga = str(vaga)
        num_vagas[i] = vaga.split()[0]
        
        if num_vagas[i] == '-':
            num_vagas[i] = 0
            
    for i, banheiro in enumerate(num_banheiros):
        banheiro = str(banheiro)
        num_banheiros[i] = banheiro.split()[0]
        
    for i, preco in enumerate(precos):
        partes = preco.split('\xa0', 1)
        precos[i] = partes[1]
        
    # função que converte os  tempos de publicação em datas

    def converter_para_data(data_string):
        # Remover o prefixo 'Publicado há' para ficar com apenas a parte de tempo relativo
        data_string = data_string.replace('Publicado há', '').strip()

        # Usando o dateparser para analisar a string com a data relativa
        data_convertida = dateparser.parse(data_string, settings={'PREFER_DATES_FROM': 'past'})

        # Verificando se a conversão foi bem-sucedida
        if data_convertida:
            # Retorna a data no formato "dia/mês/ano"
            return data_convertida.strftime('%d/%m/%Y')
        else:
            # Caso não consiga converter, retorna uma mensagem de erro
            return "Data inválida"
        
    datas_completas = [converter_para_data(data) for data in tempos_publi]
        
    def extrair_informacoes(data_string):
    # Converte a string para o formato datetime
        try:
            data_convertida = datetime.strptime(data_string, '%d/%m/%Y')
        except:
            data_convertida = None
            
        if data_convertida is None:
            return {
                'Dia': None,
                'Mes': None,
                'Ano': None,
                'Dia da semana (número)': None,
                'Dia da semana (extenso)': None,
                'Semana do ano': None,
                'Quarter': None
            }
        
        # Extraindo as informações solicitadas
        dia = data_convertida.day
        mes = data_convertida.month
        ano = data_convertida.year
        dia_da_semana = data_convertida.weekday()  # Retorna 0 para segunda-feira até 6 para domingo
        dia_da_semana_extenso = [
            'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 
            'Sexta-feira', 'Sábado', 'Domingo'
        ][dia_da_semana]  # Nome do dia da semana em português
        semana_ano = data_convertida.isocalendar()[1]  # Número da semana do ano
        quarter = (mes - 1) // 3 + 1  # Determina o trimestre (Q1, Q2, Q3 ou Q4)

        # Retorna as informações como um dicionário
        return {
            'Dia': dia,
            'Mes': mes,
            'Ano': ano,
            'Dia da semana (número)': dia_da_semana,
            'Dia da semana (extenso)': dia_da_semana_extenso,
            'Semana do ano': semana_ano,
            'Quarter': f'Q{quarter}'
        }
        
    dia = []
    mes = []
    ano = []
    dia_da_semana = []
    dia_da_semana_extenso = []
    semana_do_ano = []
    quarter = []
    
    for data in datas_completas:
        informacoes = extrair_informacoes(data)
        
        # Acessando as chaves do dicionário para preencher as listas
        dia.append(informacoes['Dia'])
        mes.append(informacoes['Mes'])
        ano.append(informacoes['Ano'])
        dia_da_semana.append(informacoes['Dia da semana (número)'])
        dia_da_semana_extenso.append(informacoes['Dia da semana (extenso)'])
        semana_do_ano.append(informacoes['Semana do ano'])
        quarter.append(f'{informacoes["Quarter"]}')
    
    dados = pd.DataFrame({'Preco':precos})
    dados['Num Quartos'] = num_quartos
    dados['Num Banheiros'] =num_banheiros
    dados['Num Vagas'] = num_vagas
    dados['Tamanho'] = m_quadrados
    dados['Tipo'] = tipos_imoveis
    dados['Cidade'] = cidades
    dados['Regiao'] = regioes
    dados['Itens Disponivels'] = itens_disponiveis
    dados['Itens Indisponíveis'] = itens_indisponiveis
    dados['Data Completa'] = datas_completas
    dados['Dia'] = dia
    dados['Mes'] = mes
    dados['Ano'] = ano
    dados['Dia da Semana'] = dia_da_semana
    dados['Dia da Semana Extenso'] = dia_da_semana_extenso
    dados['Semana do Ano'] = semana_do_ano
    dados['Quarter'] = quarter
    dados['Estado'] = estado
    
    try:
        csv = pd.read_csv('quintoAndar.csv')
        
        result = pd.concat([csv, dados], ignore_index=True)
    
        result.to_csv('quintoAndar.csv', index=False)
    except:
        dados.to_csv('quintoAndar.csv')
        print("Arquivo não encontrado. Criando um novo arquivo CSV.")
    
    
