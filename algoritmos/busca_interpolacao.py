def busca_interpolacao(livros, isbn):
    """
    Busca um livro pelo ISBN usando busca por interpolação.

    ATENÇÃO: `livros` deve estar ordenado por ISBN (numérico) em ordem crescente.
             Livros sem ISBN ficam no início da lista e são pulados pela busca.

    Parâmetros:
        livros (list[dict]): catálogo ordenado por ISBN numérico crescente.
        isbn   (str): ISBN normalizado (só dígitos) a ser buscado.

    Retorna:
        dict | None: o livro encontrado, ou None se não existir.

    Complexidade: O(log log n) em média para dados uniformemente distribuídos.
    """

    # Se o ISBN buscado for vazio, não há o que procurar
    if not isbn:
        return None

    def _isbn_int(s):
        """Converte string de ISBN para int, tratando 'X' do ISBN-10."""
        return int(s.replace("X", "0").replace("x", "0"))

    # Converte o ISBN buscado para inteiro — necessário para a fórmula matemática
    chave = _isbn_int(isbn)

    # Ponteiros de início e fim da janela de busca
    low = 0
    high = len(livros) - 1

    # Avança `low` para pular livros sem ISBN (ficam no início após a ordenação)
    while low <= high and not livros[low].get("isbn", ""):
        low += 1

    # --- Loop principal ---
    while low <= high:

        # Lê os ISBNs dos extremos da janela atual
        isbn_low_str = livros[low].get("isbn", "")
        isbn_high_str = livros[high].get("isbn", "")

        # Se os extremos não têm ISBN, a janela está na zona sem ISBN — encerra
        if not isbn_low_str or not isbn_high_str:
            return None

        # Converte os extremos para inteiro
        isbn_low = _isbn_int(isbn_low_str)
        isbn_high = _isbn_int(isbn_high_str)

        # Se a chave está fora do intervalo [isbn_low, isbn_high], não existe
        if chave < isbn_low or chave > isbn_high:
            return None

        # Evita divisão por zero: todos os ISBNs na janela são iguais
        if isbn_low == isbn_high:
            if isbn_low_str == isbn:
                return livros[low]
            return None

        # --- Fórmula de interpolação ---
        # Estima proporcionalmente onde o ISBN deve estar dentro da janela
        pos = low + int((chave - isbn_low) / (isbn_high - isbn_low) * (high - low))

        # Garante que pos ficou dentro dos limites (proteção contra arredondamento)
        if pos < low:
            pos = low
        if pos > high:
            pos = high

        # ISBN do elemento na posição estimada (como string e como int)
        isbn_pos_str = livros[pos].get("isbn", "")
        isbn_pos_int = _isbn_int(isbn_pos_str) if isbn_pos_str else -1

        # --- Comparação e movimentação dos ponteiros ---
        if isbn_pos_str == isbn:
            # Encontrou!
            return livros[pos]
        elif isbn_pos_int < chave:
            # Livro está à direita → descarta tudo até pos
            low = pos + 1
        else:
            # Livro está à esquerda → descarta tudo a partir de pos
            high = pos - 1

    # Saiu do loop sem encontrar: livro não existe no catálogo
    return None


__all__ = ["busca_interpolacao"]
