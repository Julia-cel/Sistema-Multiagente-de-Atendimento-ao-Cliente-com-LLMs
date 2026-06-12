import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================

st.set_page_config(
    page_title="Avaliação do Sistema Multiagente com LLMs",
    page_icon="🤖",
    layout="wide"
)

# ======================
# TÍTULO
# ======================

st.title("🤖 Dashboard de Avaliação do Sistema Multiagente com LLMs")

st.markdown("""
Este dashboard apresenta os resultados da avaliação de um sistema multiagente
baseado em LLMs para atendimento ao cliente em e-commerce.

O sistema utiliza três agentes especializados:

- **Classificador:** identifica a intenção do cliente;
- **Especialista:** gera respostas contextualizadas;
- **Avaliador (QA):** avalia a qualidade das respostas geradas.
""")

with st.expander("ℹ️ Como interpretar os resultados"):

    st.markdown("""
Cada resposta gerada pelo sistema recebeu uma **nota de 0 a 5**, atribuída por um agente avaliador responsável por analisar a qualidade do atendimento.

### Critério de aprovação
- **Nota ≥ 4:** resposta considerada **APROVADA**, indicando que atendeu adequadamente à solicitação do cliente.
- **Nota < 4:** resposta considerada **REPROVADA**, indicando oportunidades de melhoria.

### Métricas apresentadas

**Taxa de Aprovação:** percentual de respostas que receberam nota igual ou superior a 4.

**Acurácia do Classificador:** percentual de solicitações em que a categoria prevista pelo classificador correspondeu à categoria esperada no conjunto de testes.

**Nota Média das Respostas:** média das notas atribuídas pelo agente avaliador às respostas geradas pelo sistema.
""")

# ======================
# CARREGAR DADOS
# ======================

df = pd.read_csv("results.csv")

# ======================
# KPIs PRINCIPAIS
# ======================

accuracy = (
    (
        df["expected_category"]
        ==
        df["predicted_category"]
    ).mean()
    * 100
)

approval_rate = (
    (
        df["status"] == "APROVADO"
    ).mean()
    * 100
)

mean_score = df["nota_resolucao"].mean()

st.subheader("Indicadores Gerais")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Acurácia da Classificação",
    f"{accuracy:.1f}%"
)

col2.metric(
    "Taxa de Aprovação",
    f"{approval_rate:.1f}%"
)

col3.metric(
    "Nota Média das Respostas",
    f"{mean_score:.2f}/5"
)

# ======================
# DISTRIBUIÇÃO DAS CATEGORIAS
# ======================

st.subheader("Desempenho do Classificador por Categoria")

accuracy_categoria = (
    df.assign(
        acertou=lambda x:
        x["expected_category"] == x["predicted_category"]
    )
    .groupby("expected_category")["acertou"]
    .mean()
    .mul(100)
    .reset_index()
)

accuracy_categoria.columns = [
    "Categoria",
    "Acurácia (%)"
]

fig = px.bar(
    accuracy_categoria,
    x="Categoria",
    y="Acurácia (%)",
    text="Acurácia (%)"
)

fig.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ======================
# DISTRIBUIÇÃO DAS NOTAS
# ======================

st.subheader("Distribuição das Notas de Resolução")

fig = px.histogram(
    df,
    x="nota_resolucao",
    nbins=6,
    text_auto=True
)

fig.update_layout(
    xaxis_title="Nota",
    yaxis_title="Quantidade de Casos"
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ======================
# DESEMPENHO POR CATEGORIA
# ======================

st.subheader("Desempenho por Categoria")

desempenho = (
    df.groupby("expected_category")
    .agg(
        Nota_Média=("nota_resolucao", "mean"),
        Taxa_Aprovação=(
            "status",
            lambda x: (x == "APROVADO").mean() * 100
        )
    )
    .reset_index()
)

desempenho.columns = [
    "Categoria",
    "Nota Média",
    "Taxa de Aprovação (%)"
]

desempenho["Nota Média"] = (
    desempenho["Nota Média"]
    .round(2)
)

desempenho["Taxa de Aprovação (%)"] = (
    desempenho["Taxa de Aprovação (%)"]
    .round(1)
)

st.dataframe(
    desempenho,
    width="stretch"
)

# ======================
# NOTA MÉDIA POR CATEGORIA
# ======================

st.subheader("Nota Média por Categoria")

fig = px.bar(
    desempenho,
    x="Categoria",
    y="Nota Média",
    text_auto=".2f"
)

fig.update_layout(
    yaxis_range=[0, 5]
)

st.plotly_chart(
    fig,
    width="stretch"
)

# ======================
# CASOS QUE REQUEREM ATENÇÃO
# ======================

st.subheader("Casos que Requerem Atenção")

problem_cases = df[
    (
        df["status"] == "REPROVADO"
    )
    |
    (
        df["nota_resolucao"] < 4
    )
]

if len(problem_cases) > 0:

    st.write(
        f"Foram identificados **{len(problem_cases)} caso(s)** com potencial para melhorias."
    )

    st.dataframe(
        problem_cases[
            [
                "question",
                "expected_category",
                "predicted_category",
                "nota_resolucao",
                "status",
                "feedback"
            ]
        ],
        width="stretch"
    )

else:

    st.success(
        "Nenhum caso problemático foi identificado."
    )

# ======================
# DADOS COMPLETOS
# ======================

with st.expander("Visualizar base completa de resultados"):

    st.dataframe(
        df,
        width="stretch"
    )