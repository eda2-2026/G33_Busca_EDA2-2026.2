from algoritmos.busca_hash import buscar_hash, construir_tabela_hash
from algoritmos.busca_interpolacao import busca_interpolacao
from openlibrary import normalizar_isbn


USAR_ALGORITMOS_MANUAIS = False

_catalogo = []


def configurar_catalogo(livros):
    global _catalogo
    _catalogo = livros if isinstance(livros, list) else []


def buscar_por_titulo(titulo):
    if USAR_ALGORITMOS_MANUAIS:
        construir_tabela_hash(_catalogo)
        return buscar_hash(titulo)
    return _buscar_por_titulo_linear(titulo)


def buscar_por_isbn(isbn):
    if USAR_ALGORITMOS_MANUAIS:
        return busca_interpolacao(_catalogo, normalizar_isbn(isbn))
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
    "USAR_ALGORITMOS_MANUAIS",
    "buscar_por_isbn",
    "buscar_por_titulo",
    "configurar_catalogo",
]
