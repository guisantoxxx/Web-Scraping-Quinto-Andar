import unicodedata
import pandas as pd


#Função pra remover acentos
def remove_accents(text):
    if isinstance(text, str):
        # Normaliza o texto para decompor os acentos
        nfkd_form = unicodedata.normalize('NFKD', text)
        # Remove os caracteres de acento (combining characters)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return text

#Pegando o csv
df = pd.read_csv('quintoAndar.csv')

#Tirar as colunas "Unnamed"
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Aplica a remoção de acentos para todas as colunas que possuem dados textuais
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(remove_accents)

#Colocar tudo minúsculo
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.lower()
    
#Dropa nulos
df.dropna(inplace=True)

# Tirar caracteres especiais
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.replace(r"[()\[\]{}]", "", regex=True)

#print(df.head())       
#print(df.columns)      

print(df)

