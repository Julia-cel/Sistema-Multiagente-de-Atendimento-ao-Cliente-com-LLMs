import pandas as pd
import time

from agentes import (
    classify_question,
    generate_specialized_response,
    evaluate_response
)

# ==========================
# CARREGAR CASOS DE TESTE
# ==========================

df = pd.read_csv("test_cases.csv")

results = []

print(f"Iniciando avaliação de {len(df)} casos...\n")

# ==========================
# EXECUTAR PIPELINE
# ==========================

for index, row in df.iterrows():

    question = row["question"]
    expected_category = row["expected_category"]

    print(f"Processando {index + 1}/{len(df)}")

    try:

        # Agente Classificador
        predicted_category = classify_question(question)

        # Agente Especialista
        generated_response = generate_specialized_response(
            predicted_category,
            question
        )

        # Agente Avaliador
        evaluation = evaluate_response(
            question,
            predicted_category,
            generated_response
        )

        results.append({
            "question": question,
            "expected_category": expected_category,
            "predicted_category": predicted_category,
            "generated_response": generated_response,
            "classificacao_correta_qa": evaluation.get("classificacao_correta"),
            "nota_resolucao": evaluation.get("nota_resolucao"),
            "categoria_final_qa": evaluation.get("categoria_final"),
            "status": evaluation.get("status"),
            "feedback": evaluation.get("feedback")
        })

    except Exception as e:

        print(f"Erro no caso {index + 1}: {e}")

        results.append({
            "question": question,
            "expected_category": expected_category,
            "predicted_category": None,
            "generated_response": None,
            "classificacao_correta_qa": None,
            "nota_resolucao": None,
            "categoria_final_qa": None,
            "status": "ERRO",
            "feedback": str(e)
        })

    # Evita sobrecarregar a API
    time.sleep(2)

# ==========================
# SALVAR RESULTADOS
# ==========================

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results.csv",
    index=False
)

print("\nAvaliação concluída!")
print("Arquivo salvo: results.csv")