"""
Gera o diagrama da jornada do cliente usado no PDF e nos slides:
em que momento cada grupo de variáveis existe e onde o NPS é coletado.

Uso (a partir da raiz do projeto):
    python src/diagrama_jornada.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from nps_utils import COR_DESTAQUE, COR_NEUTRA, COR_TEXTO, COR_TEXTO_SECUNDARIO, CORES_CATEGORIA, salvar_figura

ETAPAS = [
    ("Compra", "valor, itens,\ndesconto, parcelas,\nfrete"),
    ("Entrega", "prazo, atraso,\ntentativas"),
    ("Atendimento", "contatos,\nreclamações,\ntempo de resolução"),
    ("Pesquisa NPS", "nps_score\n(alvo)"),
    ("Pós-compra", "recompra em 30 dias\n(consequência)"),
]


def gerar_diagrama():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.6)
    ax.axis("off")

    largura, altura, inicio_y = 1.9, 0.9, 1.9
    posicoes = [0.3 + i * 2.35 for i in range(len(ETAPAS))]

    # Faixa "dá para agir antes da pesquisa"
    ax.add_patch(FancyBboxPatch((0.15, 0.25), 6.95, 3.15, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor="#EEF4FC", edgecolor="none", zorder=0))
    ax.text(0.35, 3.15, "Sinais disponíveis ANTES da pesquisa: janela para agir", fontsize=10.5,
            fontweight="bold", color=CORES_CATEGORIA["Promotor"])

    for i, (x, (etapa, variaveis)) in enumerate(zip(posicoes, ETAPAS)):
        if etapa == "Pesquisa NPS":
            cor = COR_DESTAQUE
        elif etapa == "Pós-compra":
            cor = COR_NEUTRA
        else:
            cor = CORES_CATEGORIA["Promotor"]
        ax.add_patch(FancyBboxPatch((x, inicio_y), largura, altura, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=cor, edgecolor="none", zorder=2))
        ax.text(x + largura / 2, inicio_y + altura / 2, etapa, ha="center", va="center", fontsize=12,
                fontweight="bold", color="white", zorder=3)
        ax.text(x + largura / 2, inicio_y - 0.2, variaveis, ha="center", va="top", fontsize=9.5,
                color=COR_TEXTO_SECUNDARIO, zorder=3)
        if i < len(ETAPAS) - 1:
            ax.annotate("", xy=(posicoes[i + 1] - 0.05, inicio_y + altura / 2),
                        xytext=(x + largura + 0.05, inicio_y + altura / 2),
                        arrowprops=dict(arrowstyle="-|>", color=COR_TEXTO, lw=1.4), zorder=1)

    ax.text(0.3, 0.0, "Cadastro do cliente (idade, região, tempo de casa) existe desde antes da compra.  "
            "csat_internal_score é outra medida de satisfação, colhida junto ou depois do NPS.",
            fontsize=9, color=COR_TEXTO_SECUNDARIO)
    return fig


if __name__ == "__main__":
    figura = gerar_diagrama()
    caminho = salvar_figura(figura, "fig00_jornada_cliente.png")
    print(f"Diagrama salvo em {caminho}")
