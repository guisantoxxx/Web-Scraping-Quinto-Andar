import unicodedata
import pandas as pd

def remove_accents(text):
    if isinstance(text, str):
        # Normaliza o texto para decompor os acentos
        nfkd_form = unicodedata.normalize('NFKD', text)
        # Remove os caracteres de acento (combining characters)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return text

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('quintoAndar.csv')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Aplica a remoção de acentos para todas as colunas que possuem dados textuais
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].apply(remove_accents)

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.lower()
    
df.dropna(inplace=True)

# Para cada coluna do tipo objeto (texto)
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.replace(r"[()\[\]{}]", "", regex=True)

print(df.head())       
print(df.columns)      

text_columns = ['Cidade', 'Estado', 'Regiao', 'Dia da Semana Extenso', 'Itens Disponivels', 'Itens Indisponíveis']

print(df)

