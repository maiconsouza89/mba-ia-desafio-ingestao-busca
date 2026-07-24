# Desafio MBA Engenharia de Software com IA - Full Cycle

## Objetivo

Este projeto realiza:

1. Ingestao de um PDF em um banco vetorial (PostgreSQL + pgvector).
2. Busca semantica dos trechos relevantes.
3. Chat com agente para responder perguntas somente com base no contexto.

Implementacao do contexto da solucao:

- Orquestracao com LangChain.
- Uso de agente ReAct para fluxo de raciocinio e uso de ferramentas.
- Tool de busca vetorial para recuperar os trechos relevantes.
- Prompt Template para definir regras de resposta e formato de saida.

## Pre-requisitos

- Docker e Docker Compose instalados.
- Python 3.10+.
- Chave da OpenAI valida (`OPENAI_API_KEY`).

## 1) Subir o Docker (PostgreSQL + pgvector)

No diretorio raiz do projeto, execute:

```bash
docker compose up -d
```

Verifique se os containers estao saudaveis:

```bash
docker compose ps
```

## 2) Configurar ambiente Python e variaveis

Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Copie o arquivo de exemplo de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha os campos abaixo:

```env
OPENAI_API_KEY=<sua_chave_openai>
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=document_collection
PDF_PATH=../document.pdf
```

Observacao:
- `PDF_PATH` e resolvido a partir da pasta `src/`.
- Mantendo `PDF_PATH=../document.pdf`, o arquivo `document.pdf` deve estar na raiz do projeto.

## 3) Executar a ingestao do documento

Com o ambiente virtual ativo:

```bash
python src/ingest.py
```

Ao final, voce deve ver uma mensagem de sucesso indicando a quantidade de chunks ingeridos no PGVector.

## 4) Executar o chat

Com o ambiente virtual ativo:

```bash
python src/chat.py
```

O terminal exibira algo como:

```text
Chat com IA iniciado! Digite 'sair' para encerrar.
```

## 5) Validacao com perguntas esperadas

No chat, execute exatamente:

```text
Faca sua pergunta:

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhoes de reais.

---

Perguntas fora do contexto:

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Nao tenho informacoes necessarias para responder sua pergunta.
```

## Encerrar ambiente

Para encerrar o chat, digite:

```text
sair
```

Para derrubar os containers:

```bash
docker compose down
```