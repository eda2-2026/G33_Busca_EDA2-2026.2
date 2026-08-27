def recomendar_livros(livro_base, catalogo, limite=5):
    if not livro_base or not isinstance(catalogo, list):
        return []

    sugestoes = []
    for candidato in catalogo:
        if _mesmo_livro(livro_base, candidato):
            continue

        pontos = _pontuar(livro_base, candidato)
        if pontos > 0:
            sugestoes.append((pontos, candidato))

    sugestoes.sort(key=lambda item: item[0], reverse=True)
    return [livro for _, livro in sugestoes[:limite]]


def _pontuar(livro_base, candidato):
    pontos = 0

    if _texto(livro_base.get("autor")) and _texto(livro_base.get("autor")) == _texto(candidato.get("autor")):
        pontos += 3

    subjects_base = {
        str(subject).strip().lower()
        for subject in livro_base.get("subjects", [])
        if subject
    }
    subjects_candidato = {
        str(subject).strip().lower()
        for subject in candidato.get("subjects", [])
        if subject
    }
    if subjects_base.intersection(subjects_candidato):
        pontos += 2

    ano_base = livro_base.get("ano")
    ano_candidato = candidato.get("ano")
    if isinstance(ano_base, int) and isinstance(ano_candidato, int) and abs(ano_base - ano_candidato) <= 10:
        pontos += 1

    return pontos


def _mesmo_livro(livro_base, candidato):
    isbn_base = _texto(livro_base.get("isbn"))
    isbn_candidato = _texto(candidato.get("isbn"))
    if isbn_base and isbn_base == isbn_candidato:
        return True
    return _texto(livro_base.get("titulo")) == _texto(candidato.get("titulo"))


def _texto(valor):
    return str(valor or "").strip().lower()


__all__ = ["recomendar_livros"]
