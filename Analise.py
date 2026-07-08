import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec 
import os 
# Cores definidas como constantes no topo do script. Assim, se quiser mudar qualquer cor do relatório, muda em um lugar só.

AZUL = "#1F4E79"
AZUL_CLARO = "#2E75B6"
CINZA = "#D6DCE4"
VERDE = "#375623"
VERMELHO = "#C00000"

#  são as configurações globais do matplotlib — aplicam em todos os gráficos do script.

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"

    
})

# Lê o CSV e já converte a coluna "data" para o tipo datetime do pandas.

df = pd.read_csv("data/monitorias.csv", parse_dates=["data"])

# Aqui estou realizando uma validação antes de análisar os dados.

assert df["nota"].between(0, 100).all() 
assert df["operadores"].notna().all() 
assert df["problema_resolvido"].isin(["sim", "não"]).all() 

nota_media_geral = df["nota"].mean()
taxa_de_resolucao = (df["problema_resolvido"] == "sim").mean() * 100
duracao_media = df["duracao_seg"].mean() / 60

# Agrupa todas as linhas por operador e aplica funções diferentes para cada coluna ao mesmo tempo
# Media de notas, Quantidade de monitorias.

por_operador = (
    
    df.groupby("operadores")
    .agg(
        nota_media = ("nota", "mean"),
        total = ("id_monitoria", "count"),
        taxa_resolvido = ("problema_resolvido",
                          lambda x: (x == "sim").mean() * 100)
    )
    .round(1)
    .sort_values("nota_media", ascending= False)
    .reset_index()
    
)

# Extrai o nome do dia da coluna e garante que seja exibido pela ordem correta(Segunda a domingo)

df["dia_semana"] = df["data"].dt.day_name()

ORDEM_DIAS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

NOMES_PT = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo" ]

por_dia = (
    
    df.groupby("dia_semana")["nota"]
    .mean()
    .round(1)
    .reindex(ORDEM_DIAS)
    
)

por_dia.index = NOMES_PT

# Ordena da pior nota para melhor 

por_motivo = (
    df.groupby("motivo_contato")["nota"]
    .mean()
    .round(1)
    .sort_values()
)

# Define o tamanho do grafico 

fig = plt.figure(figsize=(14, 10))
fig.suptitle(
    "relatorio de qualidade - Monitorias de atendimento | Junho 2026",
    fontsize = 15, fontweight ="bold", color = AZUL, y= 0.98
)



gs= gridspec.GridSpec(3, 3, figure= fig, hspace=0.55, wspace=0.4)

ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis("off")

kpis = [
    ("Nota Média Geral",    f"{nota_media_geral:.1f}",   nota_media_geral >= 75),
    ("Taxa de Resolução",   f"{taxa_de_resolucao:.1f}%",    taxa_de_resolucao >= 70),
    ("Duração Média",       f"{duracao_media:.1f} min",  duracao_media <= 8),
    ("Total de Monitorias", str(len(df)),                True),
]

for i, (label, valor, dentro_da_meta) in enumerate(kpis):
    x   = 0.12 + i * 0.25
    cor = VERDE if dentro_da_meta else VERMELHO

    ax_kpi.text(x, 0.75, valor, transform=ax_kpi.transAxes,
                fontsize=22, fontweight="bold", color=cor, ha="center")
    ax_kpi.text(x, 0.2, label, transform=ax_kpi.transAxes,
                fontsize=9, color="gray", ha="center")
    
# Grafico 01

ax1 = fig.add_subplot(gs[1, :2])

cores_op = [
    AZUL if nota >= nota_media_geral else CINZA
    for nota in por_operador["nota_media"] 
    
]

bars = ax1.barh(
    por_operador["operadores"],
    por_operador["nota_media"],
    color= cores_op,
    height=0.6
    
)

# Grafico 01 - Nota média por operador

ax1.axvline(nota_media_geral, color=VERMELHO, linestyle= "--",
           linewidth=1, label= f'Média: {nota_media_geral:.1f}')
ax1.set_xlim(0, 105)
ax1.set_title("Nota Média por operador", fontsize=10, fontweight="bold", color= AZUL)
ax1.legend(fontsize=8)

for bar, val in zip(bars, por_operador["nota_media"]):
    ax1.text(val + 1, bar.get_y() + bar.get_height() /2,
            f"{val}", va="center", fontsize=8)
    
    
# Grfico 02 - Taxa de resolução por operador 

ax2 = fig.add_subplot(gs[1, 2])

cores_resolve = [
    AZUL_CLARO if t >= 70 else CINZA
    for t in por_operador["taxa_resolvido"]
    
]

ax2.barh(por_operador["operadores"], por_operador["taxa_resolvido"],
         color= cores_resolve, height=0.6)
ax2.axvline(70, color= VERMELHO, linestyle = "--", linewidth=1)
ax2.set_xlim(0, 110)
ax2.set_title("taxa de resolução %", fontsize=10, fontweight="bold", color= AZUL)

# Grafico 03 - Nota média por dia da semana 

ax3 = fig.add_subplot(gs[2, :2])

ax3.plot(por_dia.index, por_dia.values,
         marker="o", color= AZUL, linewidth=2, markersize=5)
ax3.fill_between(por_dia.index, por_dia.values, alpha=0.1, color= AZUL)
ax3.axhline(75, color= VERMELHO, linestyle= "--", linewidth= 1, label= "Meta 75")
ax3.set_title("Nota média por dia da semana", fontsize=10, fontweight ="bold", color= AZUL)
ax3.legend(fontsize=8)

# Grafico 04 - Nota por motivo do contato 

ax4 = fig.add_subplot(gs[2, 2])

cores_motivo = [
    AZUL if v >= nota_media_geral else CINZA
    for v in por_motivo.values
]

ax4.barh(por_motivo.index, por_motivo.values, color= cores_motivo, height= 0.6)
ax4.set_xlim(0, 105)
ax4.set_title("Nota por motivo", fontsize= 10, fontweight="bold", color= AZUL)
ax4.tick_params(axis="y", labelsize= 7)

# Salvando o relatorio 

os.makedirs("Relatorio", exist_ok=True)
plt.savefig("Relatorio/qualidade_monitoria.png", dpi= 150, bbox_inches="tight")
print("Relatorio salvo em: relatorio/relatorio_qualidade.png ")