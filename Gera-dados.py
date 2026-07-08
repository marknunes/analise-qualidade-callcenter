# IMportando bibliotecas

import pandas as pd                             # Pandas serve criar manipulas tabelas 
import numpy as np                              # Numpy serve para operações matematicas 
import random                                   # Gera valores aleatorios simples 
from datetime import datetime, timedelta        # Manipula datas 
import os                                       # Manipula o sistema

# Aqui estamos fixando os números aleatorios atrvez do parametro informado no metodo seed

random.seed(42)
np.random.seed(42) 

# Lista de agentes que simulam cadastro real em um call center 

OPERADORES = [
    
        'Carlos Lima',
        'Fernanda Sousa',
        'João Pedro',
        'Mariana costa',
        'Rafael Alves',
        'Tatiane Alves'
    
]

MOTIVOS = [
    
        'Dúvida sobre a fatura',
        'Cancelamento de cartão',
        'Desbloqueio',
        'Contestação de cobrança',
        'Alteração de limite'
]

# Essa é uma função que devolve uma nota para o operador sendo a média 82 e o desvio é 12
# a função random serve para arredondar os valores em números interos pois não existe nos NPS ou CSAT decimal 

def gerar_nota():
    return round(random.gauss(82, 12))

# Função para gerar os dados.

def gerar_dados(n=200):
    registros = []
    data_inicio = datetime(2026, 6, 1)
    
    for i in range(n):
        data = data_inicio + timedelta(days=random.randint(0, 29))
        nota = max (0, min(100, gerar_nota()))
        duracao = random.randint(90, 720) # Segundos
        resolvido = 'sim' if nota >= 70 else random.choice(['sim', 'não'])
        
        registros.append({
            'id_monitoria': i + 1,
            'data': data.strftime("%Y-%m-%d"),
            'operadores': random.choice(OPERADORES),
            "motivo_contato": random.choice(MOTIVOS),
            "nota": nota,
            "duracao_seg": duracao,
            "problema_resolvido": resolvido,
            "mes": data.strftime("%Y-%m")         
            
        })
        
        
    return pd.DataFrame(registros)

# Isso só roda se você executar gera_dados.py diretamente

if __name__ == "__main__":
    df = gerar_dados()
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/monitorias.csv", index= False, encoding="utf-8-sig")
    print(f"{len(df)} monitorias geradas em data/monitorias.csv")