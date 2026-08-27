from algoritmos.busca_hash import buscar_hash, construir_tabela_hash
from algoritmos.busca_interpolacao import busca_interpolacao
from openlibrary import normalizar_isbn


# Ativa a Busca por Interpolação na busca por ISBN (implemente busca_interpolacao.py)
USAR_INTERPOLACAO = True

# Ativa a Tabela Hash na busca por título (implemente busca_hash.py)
USAR_HASH = False

_catalogo = []


def configurar_catalogo(livros):
    global _catalogo
    _catalogo = livros if isinstance(livros, list) else []


def buscar_por_titulo(titulo):
    if USAR_HASH:
        construir_tabela_hash(_catalogo)
        return buscar_hash(titulo)
    return _buscar_por_titulo_linear(titulo)


def buscar_por_isbn(isbn):
    if USAR_INTERPOLACAO:
        # A busca por interpolação exige lista ordenada por ISBN numérico.
        # Livros sem ISBN ficam no início (string vazia < qualquer número).
        def _isbn_para_int(livro):
            raw = normalizar_isbn(livro.get("isbn")) or ""
            # ISBN-10 pode terminar em 'X' (valor 10); substitui por '0' só para ordenar
            return int(raw.replace("X", "0").replace("x", "0") or 0)

        catalogo_ordenado = sorted(_catalogo, key=_isbn_para_int)
        return busca_interpolacao(catalogo_ordenado, normalizar_isbn(isbn))
    return _buscar_por_isbn_linear(isbn)


def _buscar_por_titulo_linear(titulo):
    termo = str(titulo or "").strip().lower()
    if not termo:
        return []

    resultados = []
    for livro in _catalogo:
        titulo_livro = str(livro.get("titulo", "")).strip().lower()
        if termo in titulo_livro:
            resultados.append(livro)
    return resultados


def _buscar_por_isbn_linear(isbn):
    isbn_normalizado = normalizar_isbn(isbn)
    if not isbn_normalizado:
        return None

    for livro in _catalogo:
        if normalizar_isbn(livro.get("isbn")) == isbn_normalizado:
            return livro
    return None


__all__ = [
    "USAR_INTERPOLACAO",
    "USAR_HASH",
    "buscar_por_isbn",
    "buscar_por_titulo",
    "configurar_catalogo",
]
