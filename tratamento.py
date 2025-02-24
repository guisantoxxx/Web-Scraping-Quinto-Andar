import unicodedata
import pandas as pd

def remove_accents(text):
    """
    Remove acentos de uma string, se ela for do tipo str.
    """
    if isinstance(text, str):
        nfkd_form = unicodedata.normalize('NFKD', text)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return text

def trata_dados_csv(df, output_file):
    """
    Lê um arquivo CSV, realiza transformações nos dados e salva o resultado em outro CSV.
    
<<<<<<< HEAD
    Transformações realizadas:
      - Remove colunas cujo nome inicia com "Unnamed".
      - Remove acentos dos textos.
      - Converte textos para letras minúsculas.
      - Remove linhas com valores nulos.
      - Remove caracteres especiais: ( ) [ ] { }.
    """
    # Remove colunas "Unnamed"
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Aplica a remoção de acentos para colunas de texto
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(remove_accents)
    
    # Converte todos os textos para minúsculo
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.lower()
    
    # Remove linhas com valores nulos
    df.dropna(inplace=True)
    
    # Remove caracteres especiais: ( ) [ ] { }
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.replace(r"[()\[\]{}]", "", regex=True)
        
    # Remove anuncios repetidos que apenas alterando o preco
    cols_para_verificar = df.columns.difference(['Preco']).tolist()

    # Remover duplicatas, mantendo a primeira ocorrência
    df = df.drop_duplicates(subset=cols_para_verificar, keep='first')
    
    # Salva o DataFrame processado em um novo CSV
    df.to_csv(output_file, index=False)

