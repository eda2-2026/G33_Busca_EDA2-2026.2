import json
from pathlib import Path

import requests


OPENLIBRARY_BASE_URL = "https://openlibrary.org"
HEADERS = {"User-Agent": "BibliotecaVirtualMVP/1.0 (projeto academico)"}
TIMEOUT = 10


def _get_json(url, params=None):
    try:
        resposta = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        resposta.raise_for_status()
        return resposta.json()
    except requests.RequestException:
        return None
    except ValueError:
        return None


def buscar_livros_por_titulo_api(titulo, limite=20):
    params = {
        "q": titulo,
        "limit": limite,
        "fields": "key,title,author_name,first_publish_year,isbn,cover_i,subject",
    }
    dados = _get_json(f"{OPENLIBRARY_BASE_URL}/search.json", params=params)
    if not dados:
        return []
    return dados.get("docs", [])


def buscar_edicao_por_isbn_api(isbn):
    isbn = normalizar_isbn(isbn)
    if not isbn:
        return None
    return _get_json(f"{OPENLIBRARY_BASE_URL}/isbn/{isbn}.json")


def buscar_detalhes_work(work_id):
    if not work_id:
        return None
    work_id = work_id.strip()
    if not work_id.startswith("/works/"):
        work_id = f"/works/{work_id}"
    return _get_json(f"{OPENLIBRARY_BASE_URL}{work_id}.json")


def montar_url_capa(isbn):
    isbn = normalizar_isbn(isbn)
    if not isbn:
        return ""
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"


def normalizar_isbn(isbn):
    return "".join(
        caractere
        for caractere in str(isbn or "")
        if caractere.isdigit() or caractere.upper() == "X"
    )


def carregar_catalogo(caminho="catalogo.json"):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return []
    return dados if isinstance(dados, list) else []


def salvar_catalogo(livros, caminho="catalogo.json"):
    caminho = Path(caminho)
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(livros, arquivo, ensure_ascii=False, indent=2)


def importar_catalogo(caminho="catalogo.json", limite_por_termo=25, limite_detalhes=60):
    termos = [
        "machado de assis",
        "jane austen",
        "george orwell",
        "clarice lispector",
        "jules verne",
        "agatha christie",
        "william shakespeare",
        "tolstoy",
    ]
    vistos = set()
    catalogo = []

    for termo in termos:
        for item in buscar_livros_por_titulo_api(termo, limite=limite_por_termo):
            livro = limpar_livro_api(item)
            if not livro:
                continue
            chave = livro.get("isbn") or livro.get("work_id") or livro.get("titulo", "").lower()
            if chave in vistos:
                continue
            vistos.add(chave)
            if len(catalogo) < limite_detalhes:
                livro = enriquecer_livro(livro)
            catalogo.append(livro)

    salvar_catalogo(catalogo, caminho)
    return catalogo


def limpar_livro_api(item):
    titulo = (item.get("title") or "").strip()
    if not titulo:
        return None

    isbns = item.get("isbn") or []
    isbn = normalizar_isbn(isbns[0]) if isbns else ""
    autores = item.get("author_name") or []
    subjects = item.get("subject") or []

    identificador = isbn or (item.get("key", "").strip("/").replace("/", "-"))

    return {
        "id": identificador,
        "titulo": titulo,
        "autor": autores[0] if autores else "",
        "isbn": isbn,
        "ano": item.get("first_publish_year"),
        "work_id": item.get("key", ""),
        "capa": montar_url_capa(isbn),
        "descricao": "",
        "subjects": subjects[:10] if isinstance(subjects, list) else [],
    }


def enriquecer_livro(livro):
    detalhes = buscar_detalhes_work(livro.get("work_id"))
    if not detalhes:
        return livro

    descricao = detalhes.get("description")
    if isinstance(descricao, dict):
        descricao = descricao.get("value", "")
    if isinstance(descricao, str) and descricao.strip():
        livro["descricao"] = descricao.strip()

    subjects = detalhes.get("subjects")
    if isinstance(subjects, list) and subjects:
        livro["subjects"] = subjects[:10]

    return livro


__all__ = [
    "buscar_detalhes_work",
    "buscar_edicao_por_isbn_api",
    "buscar_livros_por_titulo_api",
    "carregar_catalogo",
    "enriquecer_livro",
    "importar_catalogo",
    "limpar_livro_api",
    "montar_url_capa",
    "normalizar_isbn",
    "salvar_catalogo",
]
