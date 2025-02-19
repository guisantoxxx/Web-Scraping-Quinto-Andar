from execução_scraping import *
import pandas as pd
import random


links = ['https://www.quintoandar.com.br/comprar/imovel/belo-horizonte-mg-brasil', 'https://www.quintoandar.com.br/comprar/imovel/sao-paulo-sp-brasil',
         'https://www.quintoandar.com.br/comprar/imovel/guarulhos-sp-brasil', 'https://www.quintoandar.com.br/comprar/imovel/rio-de-janeiro-rj-brasil',
         'https://www.quintoandar.com.br/comprar/imovel/niteroi-rj-brasil', 'https://www.quintoandar.com.br/comprar/imovel/campinas-sp-brasil',
         'https://www.quintoandar.com.br/comprar/imovel/sao-bernardo-do-campo-sp-brasil', 'https://www.quintoandar.com.br/comprar/imovel/osasco-sp-brasil'
         , 'https://www.quintoandar.com.br/comprar/imovel/sao-goncalo-rj-brasil','https://www.quintoandar.com.br/comprar/imovel/duque-de-caxias-rj-brasil'
         , 'https://www.quintoandar.com.br/comprar/imovel/belford-roxo-rj-brasil']
estados = ['MG', 'SP', 'SP', 'RJ', 'RJ', 'SP', 'SP', 'SP', 'RJ', 'RJ', 'RJ']

for i in range(len(links)):
    executar_scraping(links[i], estados[i], 50)
    

df = pd.read_csv('quintoAndar.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.drop_duplicates()
df.to_csv('quintoAndar.csv')

driver.quit()