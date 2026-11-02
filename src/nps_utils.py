"""
Funções reutilizáveis do projeto NPS Preditivo (Tech Challenge - Fase 1).

Centraliza:
- caminhos do projeto;
- carga da base bruta e da base tratada;
- regra de classificação do NPS (detrator / neutro / promotor);
- cálculo do indicador NPS para qualquer agrupamento;
- paleta de cores e estilo padrão dos gráficos.
"""

from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
CAMINHO_BASE_BRUTA = RAIZ_PROJETO / "data" / "raw" / "desafio_nps_fase_1.csv"
CAMINHO_BASE_TRATADA = RAIZ_PROJETO / "data" / "processed" / "nps_tratado.csv"
PASTA_FIGURAS = RAIZ_PROJETO / "reports" / "figures"

# ---------------------------------------------------------------------------
# Regras de negócio do NPS
# ---------------------------------------------------------------------------
# Metodologia padrão do NPS (Bain & Company):
#   0 a 6  -> Detrator
#   7 e 8  -> Neutro
#   9 e 10 -> Promotor
# Nesta base a nota vem com casas decimais (ex.: 6.9). Usamos limites
# "abertos" para respeitar a escala original: nota < 7 é detrator,
# 7 <= nota < 9 é neutro e nota >= 9 é promotor.
LIMITE_NEUTRO = 7.0
LIMITE_PROMOTOR = 9.0
ORDEM_CATEGORIAS = ["Detrator", "Neutro", "Promotor"]

# Cores fixas por categoria, usadas em todos os gráficos e nos slides.
# Paleta divergente (vermelho <-> azul com cinza no meio): segura para
# daltonismo, ao contrário do par vermelho/verde. As categorias também
# recebem rótulo escrito, para que a cor nunca seja a única pista.
CORES_CATEGORIA = {
    "Detrator": "#C8463D",
    "Neutro": "#CFCCC4",
    "Promotor": "#2A78D6",
}
COR_DESTAQUE = "#C8463D"
COR_NEUTRA = "#9AA0A8"
COR_TEXTO = "#1F2933"
COR_TEXTO_SECUNDARIO = "#5B6470"


def classificar_nps(nota: float) -> str:
    """Converte a nota 0-10 em categoria de NPS."""
    if nota >= LIMITE_PROMOTOR:
        return "Promotor"
    if nota >= LIMITE_NEUTRO:
        return "Neutro"
    return "Detrator"


def calcular_nps(categorias: pd.Series) -> float:
    """NPS = % de promotores - % de detratores (varia de -100 a +100)."""
    total = len(categorias)
    if total == 0:
        return float("nan")
    pct_promotores = (categorias == "Promotor").sum() / total
    pct_detratores = (categorias == "Detrator").sum() / total
    return round((pct_promotores - pct_detratores) * 100, 1)


def resumo_nps_por(df: pd.DataFrame, coluna: str) -> pd.DataFrame:
    """
    Tabela gerencial por grupo: quantidade de pedidos, nota média,
    % de detratores, % de promotores e NPS.
    """
    resumo = (
        df.groupby(coluna, observed=True)
        .agg(
            pedidos=("nps_score", "size"),
            nota_media=("nps_score", "mean"),
            pct_detratores=("nps_categoria", lambda s: (s == "Detrator").mean() * 100),
            pct_promotores=("nps_categoria", lambda s: (s == "Promotor").mean() * 100),
        )
    )
    resumo["nps"] = resumo["pct_promotores"] - resumo["pct_detratores"]
    return resumo.round(1)


# ---------------------------------------------------------------------------
# Carga de dados
# ---------------------------------------------------------------------------
def carregar_base_bruta() -> pd.DataFrame:
    """Lê o CSV original, sem nenhuma transformação."""
    return pd.read_csv(CAMINHO_BASE_BRUTA)


def carregar_base_tratada() -> pd.DataFrame:
    """Lê a base gerada pelo notebook 01, preservando a ordem das faixas."""
    df = pd.read_csv(CAMINHO_BASE_TRATADA)
    colunas_ordenadas = {
        "nps_categoria": ORDEM_CATEGORIAS,
        "faixa_atraso": ["Sem atraso", "1 dia", "2 dias", "3 dias", "4+ dias"],
        "faixa_contatos": ["Nenhum", "1 contato", "2 contatos", "3+ contatos"],
        "faixa_reclamacoes": ["0-1", "2-3", "4-5", "6+"],
        "faixa_resolucao": ["0-2 dias", "3-5 dias", "6-8 dias", "9-11 dias"],
        "faixa_idade": ["18-24", "25-34", "35-44", "45-54", "55+"],
        "faixa_tempo_casa": ["Até 1 ano", "1-3 anos", "3-5 anos", "5+ anos"],
        "faixa_valor_pedido": ["Até R$150", "R$150-300", "R$300-500", "R$500-800", "Acima de R$800"],
    }
    for coluna, ordem in colunas_ordenadas.items():
        if coluna in df.columns:
            df[coluna] = pd.Categorical(df[coluna], categories=ordem, ordered=True)
    return df


# ---------------------------------------------------------------------------
# Estilo dos gráficos
# ---------------------------------------------------------------------------
def aplicar_estilo_graficos() -> None:
    """Estilo limpo, pensado para leitura por público não técnico."""
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.dpi": 110,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": "#C9CDD2",
            "axes.labelcolor": COR_TEXTO,
            "xtick.color": COR_TEXTO,
            "ytick.color": COR_TEXTO,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": "#ECEEF0",
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
        }
    )


def salvar_figura(fig, nome_arquivo: str) -> Path:
    """Salva a figura em reports/figures para reuso nos slides."""
    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_FIGURAS / nome_arquivo
    fig.savefig(caminho, facecolor="white")
    return caminho
