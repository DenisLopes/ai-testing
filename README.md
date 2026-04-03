# AI Testing

![CI](https://github.com/DenisLopes/ai-testing/actions/workflows/ci.yml/badge.svg)

Os testes automatizados para avaliação de modelos de linguagem (LLMs), com foco em qualidade, segurança e detecção de alucinações.

## Visão Geral

Este projeto demonstra técnicas de QA aplicadas a sistemas de IA, cobrindo:

- **Testes básicos** — respostas corretas, precisão factual e cobertura de categorias
- **Testes estruturados** — cenários parametrizados com casos de borda
- **Testes de regressão** — garantia de consistência entre execuções
- **Testes de segurança** — detecção de recusas e comportamentos indesejados

### Modelo utilizado

`llama-3.3-70b-versatile` via API [Groq](https://groq.com)

---

## Estrutura do Projeto

```
ai-testing/
├── tests/
│   ├── basicos/           # Testes básicos de qualidade da IA
│   ├── estruturados/      # Testes com cenários complexos
│   ├── regressao/         # Testes de regressão
│   └── seguranca/         # Testes de segurança e ética
├── utils/
│   ├── cliente_ia.py      # Cliente de comunicação com a API Groq
│   ├── avaliador.py       # Motor de avaliação das respostas
│   └── config.py          # Configurações e variáveis de ambiente
├── casos_de_teste/
│   ├── basicos.json       # Casos básicos de qualidade
│   ├── estruturados.json  # Cenários complexos e casos de borda
│   ├── regressao.json     # Casos âncora para detectar regressões
│   └── seguranca.json     # Conteúdo prejudicial e prompt injection
├── scripts/
│   └── gerar_relatorio.py # Gerador de relatórios JSON e HTML
├── relatoriosjson/        # Relatórios em formato JSON
├── relatorioshtml/        # Relatórios em formato HTML
├── evidencias/            # Logs de execução e evidências
├── .env.example           # Modelo de variáveis de ambiente
└── README.md
```

---

## Pré-requisitos

- Python 3.10+
- Conta e API Key na [Groq](https://console.groq.com)

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/DenisLopes/ai-testing.git
cd ai-testing

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e insira sua GROQ_API_KEY
```

---

## Executando os Testes

```bash
# Todos os testes básicos
python -m pytest tests/basicos/ -v

# Todos os testes do projeto
python -m pytest tests/ -v

# Com relatório HTML do pytest
python -m pytest tests/ -v --html=relatorioshtml/pytest_report.html
```

---

## Gerando Relatório de Evidência

```bash
python scripts/gerar_relatorio.py
```

Gera automaticamente:
- `relatoriosjson/relatorio_YYYYMMDD_HHMMSS.json` — dados completos de cada caso
- `relatorioshtml/relatorio_YYYYMMDD_HHMMSS.html` — relatório visual navegável
- `evidencias/evidencia_YYYYMMDD_HHMMSS.txt` — log de execução em texto

---

## Categorias de Teste

| Categoria              | Suite         | Descrição                                              |
|------------------------|---------------|--------------------------------------------------------|
| Matematica             | Básicos       | Cálculos e operações numéricas                         |
| Geografia              | Básicos       | Conhecimento geográfico e factual                      |
| Logica                 | Básicos       | Problemas de raciocínio lógico                         |
| Alucinacao             | Básicos       | Detecção de respostas inventadas sobre eventos futuros |
| Matematica_Avancada    | Estruturados  | Cálculos complexos e casos de borda numérica           |
| Logica_Avancada        | Estruturados  | Raciocínio dedutivo e silogismos                       |
| Linguagem              | Estruturados  | Tradução e compreensão de texto                        |
| Ciencias / Historia    | Regressão     | Fatos estáveis para detectar regressões do modelo      |
| Conteudo_Prejudicial   | Segurança     | Recusa a instruções ilegais ou perigosas               |
| Prompt_Injection       | Segurança     | Resistência a manipulação de instruções                |
| Dados_Pessoais         | Segurança     | Recusa a expor dados pessoais de terceiros             |
| Alucinacao_Critica     | Segurança     | Não inventar descobertas científicas inexistentes      |

---

## Avaliação

O `Avaliador` suporta quatro tipos de verificação:

- **`contem`** — verifica se a resposta contém o valor esperado (com normalização de acentos)
- **`nao_contem`** — verifica se a resposta **não** contém o valor (útil para alucinações)
- **`exato`** — match exato após normalização
- **`recusa`** — verifica se a resposta contém expressões de recusa

---

## Variáveis de Ambiente

| Variável       | Descrição                    |
|----------------|------------------------------|
| `GROQ_API_KEY` | Chave de acesso à API Groq   |

---

## Licença

MIT
