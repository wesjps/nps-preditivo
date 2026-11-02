# NPS Preditivo: o que move a satisfação do cliente no e-commerce

Tech Challenge da **Fase 1** da pós-graduação **POSTECH Data Science + IA (FIAP)**.
Autor: **Wesley José Pinto Silveira**

---

## 1. Objetivo do projeto

Uma empresa de e-commerce cresceu rápido e passou a ver uma grande variação no **Net Promoter Score (NPS)** entre clientes com experiências aparentemente parecidas. Como o NPS só é coletado **no fim da jornada**, a empresa descobre a insatisfação tarde demais para agir.

Este projeto usa os dados operacionais de pedidos, logística e atendimento para responder:

- **Quais fatores operacionais realmente influenciam a satisfação do cliente?**
- **O que mais gera detratores e existe um "ponto de ruptura" na experiência?**
- **Que tipo de cliente tende a ter NPS mais alto ou mais baixo?**
- **Como a empresa pode agir de forma preventiva, antes da pesquisa de NPS?**

O foco é **entendimento do negócio, pensamento analítico e storytelling com dados**. O desafio opcional de modelo preditivo (etapa 4) **não foi implementado**. A apresentação traz apenas uma proposta conceitual de como um modelo poderia apoiar a empresa.

## 2. Principais resultados

| # | Achado | Evidência |
|---|---|---|
| 1 | **O atraso na entrega é o fator nº 1** | Cada dia de atraso tira ≈ 1 ponto da nota. NPS vai de −34 (sem atraso) a −100 (4+ dias) |
| 2 | **O 2º dia de atraso é o ponto de ruptura** | A partir dele os promotores somem (≤ 2%) e ~9 em cada 10 clientes viram detratores. 64% dos pedidos estão nessa situação |
| 3 | **Prazo longo não incomoda; atraso, sim** | Pedidos entregues em 2 ou em 14 dias têm o mesmo NPS (≈ −80) |
| 4 | **Atendimento e reclamações são o 2º bloco de fatores** | NPS −60 sem contato contra −94 com 3+ contatos; a partir de 2 reclamações a satisfação desaba |
| 5 | **Só a experiência sem atrito gera NPS positivo** | Sem atraso e sem contato: NPS +18, mas em só 2,6% dos pedidos |
| 6 | **O perfil do cliente quase não importa** | Região, idade, tempo de casa, valor, desconto e parcelas mudam o NPS em no máximo ~11 pontos |
| 7 | **Atacar o atraso tem alto retorno** | Simulação: limitar o atraso a 1 dia levaria o NPS de −80 para ≈ −65; atraso zero, para ≈ −50 |

## 3. Entregáveis

| Entregável | Arquivo |
|---|---|
| Etapas 1 e 2: entendimento do negócio e definição da target (PDF) | [`reports/01_entendimento_negocio_e_target.pdf`](reports/01_entendimento_negocio_e_target.pdf) |
| Tratamento e preparação dos dados | [`notebooks/01_tratamento_dados.ipynb`](notebooks/01_tratamento_dados.ipynb) |
| Etapa 3: análise exploratória (EDA) com foco em negócio | [`notebooks/02_analise_exploratoria.ipynb`](notebooks/02_analise_exploratoria.ipynb) |
| Apresentação para gestores (storytelling) | [`reports/apresentacao_nps_preditivo.pptx`](reports/apresentacao_nps_preditivo.pptx) |
| Roteiro do vídeo executivo | [`reports/roteiro_video.md`](reports/roteiro_video.md) |
| Vídeo executivo (até 5 min) | *link a ser incluído aqui* |

## 4. Descrição da base de dados

Arquivo: `data/raw/desafio_nps_fase_1.csv`. São **2.500 pedidos e 19 colunas**, sem valores ausentes e sem duplicados. Cada cliente aparece uma única vez.

| Grupo | Colunas | Descrição |
|---|---|---|
| Cliente | `customer_id`, `customer_age`, `customer_region`, `customer_tenure_months` | Identificador, idade, região (5 regiões do Brasil) e tempo de relacionamento em meses |
| Pedido | `order_id`, `order_value`, `items_quantity`, `discount_value`, `payment_installments`, `freight_value` | Valor, itens, desconto, parcelas e frete |
| Logística | `delivery_time_days`, `delivery_delay_days`, `delivery_attempts` | Tempo total de entrega, dias de atraso e tentativas de entrega |
| Atendimento | `customer_service_contacts`, `resolution_time_days`, `complaints_count` | Contatos com o SAC, tempo de resolução e reclamações |
| Resultado | `repeat_purchase_30d`, `csat_internal_score` | Recompra em 30 dias e score interno de satisfação |
| **Alvo** | **`nps_score`** | Nota de 0 a 10 coletada após a experiência de compra |

### Pontos de atenção encontrados nos dados
- **Nota com casas decimais:** 83% das notas não são inteiras, fora do padrão do NPS. A classificação usa *nota < 7 = detrator*, *7 a < 9 = neutro* e *≥ 9 = promotor*.
- **Vazamento de informação:** `repeat_purchase_30d` (100% dos promotores e 0% dos detratores recompraram) e `csat_internal_score` são consequência ou outra medida da satisfação. Por isso **não são usadas** para explicar ou antecipar o NPS.
- **Inconsistências de definição:** tempo de resolução > 0 para clientes sem contato (20% da base), atraso maior que o tempo total (5%), desconto maior que o valor do pedido (1%) e mais reclamações que contatos (97%). **Nenhuma linha foi removida.** Os casos foram marcados com *flags* e tratados onde importam (detalhes no notebook 01).

## 5. Metodologia

1. **Entendimento do negócio e da target** (PDF): problema, importância do NPS, áreas beneficiadas, impacto em recompra, boca a boca e market share, indicadores complementares, escolha da variável-alvo e riscos de uso.
2. **Tratamento dos dados** (notebook 01): verificações de qualidade, regras de consistência entre colunas, outliers (IQR), classificação das variáveis pelo momento da jornada (o que existe antes da pesquisa), criação da categoria NPS e de faixas em linguagem de negócio.
3. **Análise exploratória** (notebook 02), sempre comparando **NPS e % de detratores e promotores por grupo**:
   - impacto de atraso, prazo total, contatos, reclamações e tempo de resolução;
   - busca do ponto de ruptura e da combinação atraso × atendimento;
   - perfil do cliente (região, idade, tempo de casa, valor do pedido etc.);
   - ordenação dos fatores por *permutation importance* (floresta aleatória, com teste em 30% dos dados) e efeito unitário por regressão linear, **sem as variáveis com vazamento**. É uma ferramenta de apoio à EDA, não o modelo preditivo opcional;
   - simulação ilustrativa do ganho de NPS ao reduzir o atraso.
4. **Storytelling** (slides e roteiro de vídeo): contexto, pergunta, insights, fatores, recomendações, proposta de modelo e limitações, em linguagem para gestores.

## 6. Estrutura do repositório

```
.
├── data/
│   ├── raw/                  # base original (desafio_nps_fase_1.csv)
│   └── processed/            # base tratada gerada pelo notebook 01 (nps_tratado.csv)
├── notebooks/
│   ├── 01_tratamento_dados.ipynb
│   └── 02_analise_exploratoria.ipynb
├── src/
│   ├── nps_utils.py          # caminhos, regra de classificação, cálculo do NPS, estilo dos gráficos
│   └── diagrama_jornada.py   # gera o diagrama da jornada do cliente
├── reports/
│   ├── figures/              # gráficos gerados pelos notebooks
│   ├── 01_entendimento_negocio_e_target.pdf
│   ├── apresentacao_nps_preditivo.pptx
│   └── roteiro_video.md
├── models/                   # reservado: o modelo preditivo (desafio opcional) não foi implementado
├── requirements.txt
└── README.md
```

## 7. Como reproduzir os resultados

Pré-requisito: **Python 3.10 ou superior**.

```bash
# 1. Clonar o repositório
git clone <url-deste-repositorio>
cd <pasta-do-repositorio>

# 2. Criar e ativar um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Abrir os notebooks e executar em ordem
jupyter notebook
```

Ordem de execução:
1. `notebooks/01_tratamento_dados.ipynb` gera `data/processed/nps_tratado.csv`;
2. `notebooks/02_analise_exploratoria.ipynb` gera os gráficos em `reports/figures/`.

Opcional: `python src/diagrama_jornada.py` (a partir da raiz) regera o diagrama da jornada usado no PDF e nos slides.

Os notebooks já estão salvos **com as saídas**, então dá para ler a análise no próprio GitHub sem executar nada. Os resultados são determinísticos (`random_state=42`).

## 8. Limitações

- A análise mostra **associação**, não causa comprovada. As recomendações devem ser validadas com pilotos (testes A/B).
- A base parece **simulada** (nota decimal, relação perfeita entre recompra e NPS), então o tamanho dos efeitos deve ser lido com cautela.
- Não há **datas** nem **histórico por cliente**, o que impede análises de tendência e sazonalidade.
- Os fatores disponíveis explicam pouco mais da metade da variação das notas. Qualidade do produto, embalagem e expectativa não estão na base.
