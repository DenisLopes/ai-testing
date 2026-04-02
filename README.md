# AI Testing

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
ai-testing-portfolio/
├── testsbasicos/          # Testes básicos de qualidade da IA
├── testsestruturados/     # Testes com cenários complexos
├── testsregressao/        # Testes de regressão
├── testsseguranca/        # Testes de segurança e ética
├── utils/
│   ├── cliente_ia.py      # Cliente de comunicação com a API Groq
│   ├── avaliador.py       # Motor de avaliação das respostas
│   └── config.py          # Configurações e variáveis de ambiente
├── casos_de_teste/        # Casos de teste por categoria
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
python -m pytest testsbasicos/ -v

# Todos os testes do projeto
python -m pytest -v

# Com relatório HTML do pytest
python -m pytest testsbasicos/ -v --html=relatorioshtml/pytest_report.html
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

| Categoria     | Descrição                                               |
|---------------|---------------------------------------------------------|
| Matematica    | Cálculos e operações numéricas                          |
| Geografia     | Conhecimento geográfico e factual                       |
| Logica        | Problemas de raciocínio lógico                          |
| Alucinacao    | Detecção de respostas inventadas sobre eventos futuros  |
| Seguranca     | Verificação de recusas a conteúdo prejudicial           |

---

## Avaliação

O `Avaliador` suporta dois tipos de verificação:

- **`contem`** — verifica se a resposta contém o valor esperado (com normalização de acentos)
- **`recusa`** — verifica se a resposta contém expressões de recusa

---

## Variáveis de Ambiente

| Variável       | Descrição                    |
|----------------|------------------------------|
| `GROQ_API_KEY` | Chave de acesso à API Groq   |

---

## Licença

MIT
