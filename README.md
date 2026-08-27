# Biblioteca Virtual

MVP de Biblioteca Virtual Web em Python, Flask, HTML, CSS, Requests e JSON.

O sistema usa a Open Library apenas para alimentar o `catalogo.json`. As buscas feitas pelo usuário acontecem localmente no catálogo.

## Como executar

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Depois:

```bash
pip install -r requirements.txt
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

## Gerar ou atualizar o catálogo

```bash
python -c "from openlibrary import importar_catalogo; importar_catalogo()"
```

## Busca atual

- Nome: busca linear provisória
- ISBN: busca linear provisória

## Reservado para implementação manual

- `algoritmos/busca_hash.py`
- `algoritmos/busca_interpolacao.py`

Esses arquivos possuem apenas interfaces e `TODOs`. A Tabela Hash e a Busca por Interpolação devem ser implementadas manualmente depois.
