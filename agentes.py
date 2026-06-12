import os
import json
from dotenv import load_dotenv
from groq import Groq
import time

# ==========================
# CONFIGURAÇÃO DO GEMINI
# ==========================

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém a API Key do Gemini
api_key = os.getenv("GROQ_API_KEY")

# Verifica se a chave existe
if not api_key:
    raise ValueError(
        "API Key não encontrada. Verifique se o arquivo .env existe "
        "e contém GROQ_API_KEY=sua_chave"
    )

# Cria uma conexão (cliente) com a API do Gemini
client = Groq(api_key=api_key)
Model = "llama-3.3-70b-versatile"

# ==========================
# FUNÇÃO AUXILIAR
# ==========================

import time


def call_llm(prompt, max_retries=3):
    """
    Faz chamadas para o Groq com tentativas automáticas
    caso o serviço esteja temporariamente indisponível.
    """

    for attempt in range(max_retries):

        try:
            response = client.chat.completions.create(
                model=Model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.3  # respostas mais consistentes para classificação
            )

            return response.choices[0].message.content.strip()

        except Exception as e:

            print(f"Tentativa {attempt + 1}/{max_retries} falhou.")
            print(f"Erro: {e}")

            if attempt < max_retries - 1:

                wait_time = 5 * (attempt + 1)
                print(f"Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)

            else:

                print("Número máximo de tentativas atingido.")
                return None


# ==========================
# AGENTE CLASSIFICADOR
# ==========================

def classify_question(question):
    """
    Identifica a categoria da solicitação do cliente.
    """

    prompt = f"""
Você é um especialista em classificar solicitações de atendimento ao cliente.

Analise a solicitação abaixo e classifique-a em apenas UMA das seguintes categorias:

- cancelamento
- rastreamento
- reembolso
- troca

Retorne APENAS o nome da categoria, sem explicações adicionais.

Solicitação:
"{question}"
"""

    return call_llm(prompt)


# ==========================
# AGENTE ESPECIALISTA
# ==========================

def generate_specialized_response(category, question):

    instructions = {
        "cancelamento": (
            "Confirme que o cancelamento será processado em até 5 dias úteis. "
            "Não mencione reembolso, troca ou rastreamento."
        ),
        "rastreamento": (
            "Solicite o número do pedido caso não tenha sido informado. "
            "Não mencione cancelamento, reembolso ou troca."
        ),
        "reembolso": (
            "Informe que o valor será devolvido pelo método de pagamento original "
            "em até 10 dias úteis. "
            "Não mencione cancelamento, troca ou rastreamento."
        ),
        "troca": (
            "Explique que o cliente deve solicitar a troca pelo app ou site, "
            "dentro do prazo de 7 dias após o recebimento. "
            "Não mencione cancelamento, reembolso ou rastreamento."
        ),
    }

    # Fallback caso a categoria venha errada do classificador
    instruction = instructions.get(
        category.lower().strip(),
        "Responda de forma educada e peça mais detalhes sobre a solicitação."
    )

    prompt = f"""
Você é um assistente de atendimento ao cliente de e-commerce.

Regras obrigatórias:
- Responda em no máximo 3 frases curtas
- Seja direto e objetivo
- Tom: cordial, mas sem exageros
- NÃO use saudações como "Olá" ou despedidas como "Atenciosamente"
- NÃO assine a mensagem
- NÃO invente informações além das instruções

Instrução para esta categoria ({category}):
{instruction}

Dúvida do cliente: "{question}"
"""
    return call_llm(prompt)

# ==========================
# AGENTE AVALIADOR (QA)
# ==========================

def evaluate_response(question, predicted_category, generated_response):
    """
    Avalia a qualidade da resposta gerada e retorna métricas estruturadas.
    """

    prompt = f"""
Você é um supervisor de qualidade de atendimento (QA).

Sua tarefa é analisar a interação abaixo e extrair métricas estruturadas.

Dúvida do Cliente:
"{question}"

Categoria atribuída pelo classificador:
"{predicted_category}"

Resposta gerada pelo especialista:
"{generated_response}"

Retorne APENAS um objeto JSON válido (sem blocos de código ```).

Formato esperado:

{{
    "classificacao_correta": true ou false,
    "nota_resolucao": inteiro de 0 a 5,
    "categoria_final": "categoria correta",
    "status": "APROVADO" ou "REPROVADO",
    "feedback": "justificativa curta"
}}

Critérios:

- classificacao_correta: se a categoria atribuída está adequada.
- nota_resolucao: qualidade geral da resposta.
- categoria_final: categoria correta para a solicitação.
- status: APROVADO para nota >= 4, caso contrário REPROVADO.
- feedback: justificativa breve.
"""

    result = call_llm(prompt)

    # Se houve erro na chamada da API
    if result is None:
        return {
            "classificacao_correta": None,
            "nota_resolucao": None,
            "categoria_final": None,
            "status": "ERRO",
            "feedback": "Falha na chamada da API"
        }

    # Tenta converter o JSON retornado pelo Gemini
    try:
        return json.loads(result)

    except json.JSONDecodeError:
        return {
            "classificacao_correta": None,
            "nota_resolucao": None,
            "categoria_final": None,
            "status": "ERRO",
            "feedback": "Falha ao interpretar JSON",
            "resposta_original": result
        }

