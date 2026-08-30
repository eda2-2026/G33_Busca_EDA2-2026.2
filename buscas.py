from algoritmos.busca_hash import buscar_hash, construir_tabela_hash
from algoritmos.busca_interpolacao import busca_interpolacao
from openlibrary import normalizar_isbn


# Agora os dois algoritmos manuais estão ativos
USAR_INTERPOLACAO = True
USAR_HASH = True


_catalogo = []
_catalogo_ordenado_isbn = []


def _isbn_para_int(livro):
    """
    Converte o ISBN de um livro para inteiro,
    apenas para permitir a ordenação numérica.
    """
    raw = normalizar_isbn(livro.get("isbn")) or ""

    if not raw:
        return 0

    # ISBN-10 pode terminar em X.
    # Para manter a ordenação simples, substituímos X por 0.
    raw = raw.replace("X", "0").replace("x", "0")

    try:
        return int(raw)
    except ValueError:
        return 0


def configurar_catalogo(livros):
    global _catalogo
    global _catalogo_ordenado_isbn

    _catalogo = livros if isinstance(livros, list) else []

    # -------------------------
    # PREPARA A TABELA HASH
    # -------------------------

    if USAR_HASH:
        construir_tabela_hash(_catalogo)

    # -------------------------
    # PREPARA A INTERPOLAÇÃO
    # -------------------------

    if USAR_INTERPOLACAO:
        _catalogo_ordenado_isbn = sorted(
            _catalogo,
            key=_isbn_para_int
        )


def buscar_por_titulo(titulo):
    if USAR_HASH:
        return buscar_hash(titulo)

    return _buscar_por_titulo_linear(titulo)


def buscar_por_isbn(isbn):
    isbn_normalizado = normalizar_isbn(isbn)

    if not isbn_normalizado:
        return None

    if USAR_INTERPOLACAO:
        return busca_interpolacao(
            _catalogo_ordenado_isbn,
            isbn_normalizado
        )

    return _buscar_por_isbn_linear(isbn)


# =========================================================
# BUSCAS LINEARES
# Mantidas apenas como fallback / comparação
# =========================================================

def _buscar_por_titulo_linear(titulo):
    termo = str(titulo or "").strip().lower()

    if not termo:
        return []

    resultados = []

    for livro in _catalogo:
        titulo_livro = str(
            livro.get("titulo", "")
        ).strip().lower()

        if termo in titulo_livro:
            resultados.append(livro)

    return resultados


def _buscar_por_isbn_linear(isbn):
    isbn_normalizado = normalizar_isbn(isbn)

    if not isbn_normalizado:
        return None

    for livro in _catalogo:
        isbn_livro = normalizar_isbn(
            livro.get("isbn")
        )

        if isbn_livro == isbn_normalizado:
            return livro

    return None


__all__ = [
    "USAR_INTERPOLACAO",
    "USAR_HASH",
    "buscar_por_isbn",
    "buscar_por_titulo",
    "configurar_catalogo",
]