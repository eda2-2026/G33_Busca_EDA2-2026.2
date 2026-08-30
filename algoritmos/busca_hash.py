TAMANHO_TABELA = 1000
tabela_hash = []

fator_primo = 31

def normalizar_titulo(livro):
    return str(livro or "").strip().lower()
 

def funcao_hash(titulo):
    titulo = normalizar_titulo(titulo)
    valor_hash = 0

    for char in titulo:
        # ord(char) extrai o valor numérico (ASCII/Unicode) do caractere
        valor_hash = (valor_hash * fator_primo + ord(char)) % TAMANHO_TABELA

    return valor_hash

def construir_tabela_hash(livros):
    global tabela_hash

    tabela_hash = []

    for _ in range(TAMANHO_TABELA):
        tabela_hash.append([])

    for livro in livros:
        titulo = livro.get("titulo", "")

        indice = funcao_hash(titulo)

        tabela_hash[indice].append(livro)


def buscar_hash(titulo):
    titulo = normalizar_titulo(titulo)

    indice = funcao_hash(titulo)

    bucket = tabela_hash[indice]

    resultados = []

    for livro in bucket:
        titulo_livro = normalizar_titulo(
            livro.get("titulo", "")
        )

        if titulo_livro == titulo:
            resultados.append(livro)

    return resultados