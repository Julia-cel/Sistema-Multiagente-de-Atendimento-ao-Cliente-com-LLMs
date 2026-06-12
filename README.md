# Sistema Multiagente de Atendimento ao Cliente com LLMs

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=flat)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)

Pipeline de IA com três agentes especializados que classificam solicitações de e-commerce, geram respostas e avaliam automaticamente a qualidade do atendimento — com resultados visualizados em dashboard interativo.

🔗 **[Acessar o dashboard](https://sistema-multiagente-de-atendimento-ao-cliente-com-llms-sa6nzza.streamlit.app/)**

---

## Resultados

Avaliado em uma base com **60 solicitações reais de e-commerce**, distribuídas igualmente entre as quatro categorias do sistema:

| Métrica | Resultado |
|---|---|
| Acurácia do Classificador | **100%** |
| Taxa de Aprovação das Respostas | **98,3%** |
| Nota Média das Respostas | **4,73 / 5** |

---

## Arquitetura

O sistema é composto por três agentes independentes que operam em sequência. Cada agente tem uma responsabilidade única e isolada, o que permite auditar, ajustar ou substituir qualquer etapa sem impactar as demais.

```
Solicitação do cliente
        │
        ▼
┌─────────────────────┐
│  Agente Classificador│  Identifica a categoria: cancelamento │ rastreamento
│                     │                           reembolso   │ troca
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Agente Especialista │  Gera resposta direcionada à categoria,
│                     │  sem vazar informações de outras categorias
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Agente Avaliador   │  Avalia qualidade e retorna JSON estruturado
│  (QA)               │  com nota, status e feedback
└──────────┬──────────┘
           │
           ▼
    Dashboard Streamlit
```

---

## Decisões técnicas

**Separação de responsabilidades por agente**
Cada agente recebe apenas o prompt necessário para sua função. O agente especialista, por exemplo, só recebe as instruções da categoria identificada — isso evita que o modelo misture informações de cancelamento com reembolso, um problema comum em arquiteturas de prompt único.

**Prompt isolation no agente especialista**
As instruções de cada categoria são armazenadas em um dicionário e injetadas dinamicamente no prompt. O agente nunca vê as instruções das outras categorias, o que eliminou ambiguidades nas respostas geradas.

**temperature=0.3 no classificador**
Valores baixos de temperatura tornam o modelo mais determinístico. Para classificação, consistência importa mais que variabilidade — o mesmo input deve sempre retornar a mesma categoria.

**Saída estruturada em JSON no avaliador**
O agente avaliador retorna um JSON com campos definidos (`nota_resolucao`, `classificacao_correta`, `status`, `feedback`), o que permite agregar as métricas diretamente no dashboard sem pós-processamento manual.

**Groq como provedor de inferência**
O free tier do Groq oferece 14.400 requisições/dia com latência baixa, viabilizando o processamento de toda a base (60 registros × 3 chamadas = 180 requisições) em menos de 3 minutos com `time.sleep(2)` entre registros para respeitar o rate limit.

---

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11 |
| LLM | LLaMA 3.3 70B via Groq API |
| Dashboard | Streamlit |
| Processamento de dados | Pandas |
| Deploy | Streamlit Community Cloud |

---

## Estrutura do repositório

```
├── agentes.py          # Os três agentes e a função de chamada à API
├── app.py              # Dashboard com métricas e visualizações
├── evaluate.py         # Processamento em lote da base de dados
├── AnaliseResults.py   # Análise e agregação dos resultados
├── test_agents.py      # Testes dos agentes
├── test_cases.csv      # Base com 60 solicitações de e-commerce
└── requirements.txt
```

---

## Execução local

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
python evaluate.py   # processa a base e gera results.csv
streamlit run app.py # abre o dashboard
```

---

## Autora

**Júlia** — Estudante de Ciência de Dados 

[![LinkedIn](www.linkedin.com/in/júlialobo-dataanalyst)

