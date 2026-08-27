from pathlib import Path

from flask import Flask, render_template, request

from buscas import buscar_por_isbn, buscar_por_titulo, configurar_catalogo
from openlibrary import carregar_catalogo
from recomendacoes import recomendar_livros


BASE_DIR = Path(__file__).resolve().parent
CATALOGO_PATH = BASE_DIR / "catalogo.json"

app = Flask(__name__)
catalogo = carregar_catalogo(CATALOGO_PATH)
configurar_catalogo(catalogo)


def localizar_livro(identificador):
    livro = buscar_por_isbn(identificador)
    if livro:
        return livro

    for item in catalogo:
        if str(item.get("id", "")) == identificador:
            return item
    return None


@app.route("/")
def index():
    return render_template("index.html", total_livros=len(catalogo))


@app.route("/buscar/nome", methods=["POST"])
def buscar_nome():
    titulo = request.form.get("titulo", "")
    resultados = buscar_por_titulo(titulo)
    return render_template(
        "resultados.html",
        resultados=resultados,
        termo=titulo,
        tipo_busca="nome",
    )


@app.route("/buscar/isbn", methods=["POST"])
def buscar_isbn():
    isbn = request.form.get("isbn", "")
    livro = buscar_por_isbn(isbn)
    resultados = [livro] if livro else []
    return render_template(
        "resultados.html",
        resultados=resultados,
        termo=isbn,
        tipo_busca="ISBN",
    )


@app.route("/livro/<identificador>")
def detalhe_livro(identificador):
    livro = localizar_livro(identificador)
    if not livro:
        return render_template(
            "resultados.html",
            resultados=[],
            termo=identificador,
            tipo_busca="identificador",
        ), 404

    sugestoes = recomendar_livros(livro, catalogo, limite=5)
    return render_template("livro.html", livro=livro, sugestoes=sugestoes)


if __name__ == "__main__":
    app.run(debug=True)
