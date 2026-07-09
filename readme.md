# Análise de qualidade de atendimento 

pipeline python que processa dados de monitoria de call center e gera
um dashborad automatizado com os principais indicadores de qualidade .

## Contexto de negocio 

Em operações de atendimento, monitores de qualidade escutam ligações 
gravadas e avaliam os operadores seguindo criterios internos de 
qualidade - abordagem, solução, conformidade com script e experiência 
do cliente. Este projeto automatiza a consolidação dessas avaliações 
e gera um dashboard para apoiar a tomada de decisão dos supervisores.

## Metricas geradas 

- Nota média por operador vs Média geral
- Taxa de resolução no primeiro contato 
- Duração média de atendimento 
- Nota média por dia da semana 
- Nota média por motivo do contato 

## Tecnologias 

- Python 3.14
- Pandas
- Metplotlib

## Como rodar 

'''bash
pip instal -r requirements. txt 
python gera-dados.py
python analise.py
'''

## Decisões técnicas 
** Desctribuição gaussiana por operador** cada operador tem uma média
de nota individual simulando níveis reais de experiências destintos.

** Principios de storytelling com dados(Cole Nussbaumer Knafic)
cores destacam desvio de meta, não decoram. Cada elemento visual 
existe por um motivo de negócio.

<img width="1839" height="1370" alt="qualidade_monitoria" src="https://github.com/user-attachments/assets/010702ac-db23-414a-b543-25e4a674b571" />
