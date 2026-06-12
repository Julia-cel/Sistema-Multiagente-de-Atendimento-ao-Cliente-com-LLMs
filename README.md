# Sistema Multiagente de Atendimento ao Cliente com LLMs

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

🔗 **[Acessar o dashboard](https://sistema-multiagente-de-atendimento-ao-cliente-com-llms-sa6nzza.streamlit.app)**

---

## O projeto

Um pipeline com três agentes de IA que trabalham em sequência para lidar com solicitações de atendimento em e-commerce: o primeiro classifica a intenção do cliente, o segundo gera uma resposta direcionada, e o terceiro avalia automaticamente a qualidade dessa resposta — funcionando como um juiz independente.

Os resultados de 60 solicitações processadas ficam disponíveis em um dashboard interativo com métricas de desempenho do sistema.

---

## Resultados

| Métrica | Resultado |
|---|---|
| Acurácia do Classificador | **100%** |
| Taxa de Aprovação das Respostas | **96,7%** |
| Nota Média | **4,75 / 5** |

---

## Como foi construído

**Dataset de avaliação**
Criei uma base com 60 solicitações reais de e-commerce, distribuídas igualmente entre quatro categorias: cancelamento, rastreamento, reembolso e troca. Esse dataset foi o ponto de partida para todos os experimentos e para medir o desempenho do sistema de forma confiável.

**Prompt engineering**
Cada agente tem um prompt desenhado para sua função específica. No classificador, usei few-shot examples — mostrar exemplos de input e output esperado diretamente no prompt — o que aumentou a consistência das respostas. No agente especialista, as instruções de cada categoria são injetadas de forma isolada, evitando que o modelo misture contextos. A temperature foi ajustada para 0.3 no classificador (mais determinístico) e mantida mais alta no especialista (respostas menos repetitivas).

**Avaliação com LLM-as-judge**
O agente avaliador aplica o padrão LLM-as-judge: um modelo avalia a saída de outro com critérios definidos e retorna um JSON estruturado com nota, classificação correta/incorreta, status e feedback. Isso permitiu iterar sobre os prompts com base em dados reais — quando a nota caía, o prompt era ajustado e o experimento rodava novamente.

**Do experimento ao produto**
Depois de validar o desempenho na base de avaliação, o sistema foi colocado em produção no Streamlit Community Cloud, com as variáveis de ambiente gerenciadas de forma segura via Secrets. O dashboard agrega os resultados e apresenta as métricas de forma acessível.

---

## Stack

Python · LLaMA 3.3 70B (Groq API) · Streamlit · Pandas · Streamlit Cloud

---

## Estrutura

```
├── agentes.py        # os três agentes e a lógica de chamada à API
├── app.py            # dashboard com métricas e visualizações
├── evaluate.py       # processamento da base em lote
├── test_cases.csv    # dataset com 60 solicitações de e-commerce
└── requirements.txt
```

---

## Rodando localmente

```bash
git clone https://github.com/seu-usuario/vtex-llm-multiagent-support.git
cd vtex-llm-multiagent-support
pip install -r requirements.txt
```

Crie um `.env` com sua chave da [Groq](https://console.groq.com):
```
GROQ_API_KEY=sua_chave_aqui
```

```bash
python evaluate.py
streamlit run app.py
```

---

**Júlia** — Estudante de Ciência de Dados (Uninter)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)(https://www.linkedin.com/in/j%C3%BAlialobo-dataanalyst/)


