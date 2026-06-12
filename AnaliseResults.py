import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

# ==========================
# CARREGAR RESULTADOS
# ==========================

df = pd.read_csv("results.csv")

print("=" * 50)
print("VISÃO GERAL")
print("=" * 50)

print(f"\nTotal de casos avaliados: {len(df)}")


# ==========================
# TAXA DE APROVAÇÃO
# ==========================

approval_rate = (
    (df["status"] == "APROVADO")
    .mean()
    * 100
)

print(f"\nTaxa de Aprovação: {approval_rate:.2f}%")


# ==========================
# NOTAS
# ==========================

print("\nEstatísticas das Notas:")

print(
    df["nota_resolucao"]
    .describe()
)


# ==========================
# ACCURACY CLASSIFICADOR
# ==========================

accuracy = (
    (
        df["expected_category"]
        ==
        df["predicted_category"]
    )
    .mean()
    * 100
)

print(
    f"\nAccuracy do Classificador: {accuracy:.2f}%"
)


# ==========================
# APROVAÇÃO POR CATEGORIA
# ==========================

approval_by_category = (
    df.groupby("expected_category")["status"]
    .apply(
        lambda x:
        (x == "APROVADO").mean() * 100
    )
)

print("\nTaxa de Aprovação por Categoria:")

print(
    approval_by_category
)


# ==========================
# NOTA MÉDIA POR CATEGORIA
# ==========================

mean_score = (
    df.groupby("expected_category")
    ["nota_resolucao"]
    .mean()
)

print("\nNota Média por Categoria:")

print(
    mean_score
)


# ==========================
# DISTRIBUIÇÃO CATEGORIAS
# ==========================

print(
    "\nDistribuição das Categorias Previstas:"
)

print(
    df["predicted_category"]
    .value_counts()
)


# ==========================
# MATRIZ DE CONFUSÃO
# ==========================

labels = [
    "cancelamento",
    "rastreamento",
    "reembolso",
    "troca"
]

cm = confusion_matrix(
    df["expected_category"],
    df["predicted_category"],
    labels=labels
)

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

print("\nMatriz de Confusão:")

print(cm_df)


# ==========================
# RELATÓRIO CLASSIFICAÇÃO
# ==========================

print(
    "\nClassification Report:"
)

print(
    classification_report(
        df["expected_category"],
        df["predicted_category"]
    )
)


# ==========================
# CASOS PROBLEMÁTICOS
# ==========================

problem_cases = df[
    (
        df["status"] == "REPROVADO"
    )
    |
    (
        df["nota_resolucao"] < 4
    )
]

print("\nCasos Problemáticos:")

print(
    problem_cases[
        [
            "question",
            "expected_category",
            "predicted_category",
            "nota_resolucao",
            "status",
            "feedback"
        ]
    ]
)