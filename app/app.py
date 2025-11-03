from flask import Flask, request, jsonify
from flasgger import Swagger

from src.services.categorias_service import CategoriaService
from src.services.livros_service import LivroService

app = Flask(__name__)
app.config['SWAGGER'] = {'title': "TechChallenge1"}

swagger = Swagger(app)
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """
    Listar livros paginados
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Número da página
      - name: total_records
        in: query
        type: integer
        required: false
        default: 10
        description: Total de registros por página
    responses:
      200:
        description: Lista de livros paginada
        schema:
          type: array
          items:
            type: object
    """
    pagina = request.args.get('page', default=1, type=int)
    total_registros = request.args.get('total_records', default=10, type=int)

    response = LivroService().listar_livros(pagina, total_registros)
    return jsonify(response), 200

@app.route('/api/v1/books/search', methods=['GET'])
def search_books():
    """
    Buscar livros por categoria ou título (apenas um por vez)
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Número da página
      - name: total_records
        in: query
        type: integer
        required: false
        default: 10
        description: Total de registros por página
      - name: category
        in: query
        type: string
        required: false
        description: Categoria do livro (não pode ser usado junto com title)
      - name: title
        in: query
        type: string
        required: false
        description: Título do livro (não pode ser usado junto com category)
    responses:
      200:
        description: Lista de livros filtrada por categoria ou título
        schema:
          type: array
          items:
            type: object
      422:
        description: Erro de validação dos parâmetros de busca
    """
    pagina = request.args.get('page', default=1, type=int)
    total_registros = request.args.get('total_records', default=10, type=int)
    categoria = request.args.get('category', default=None, type=str)
    titulo = request.args.get('title', default=None, type=str)

    if categoria and titulo:
        return {"error_message": "Não é possível buscar por categoria e titulo ao mesmo tempo"}, 422
    if categoria == None and titulo == None:
        return {"error_message": "Pelo menos um parametro de busca deve ser preenchido. Parametros disponiveis {category, title}"}, 422

    if categoria:
        response = LivroService().listar_livro_por_categoria(categoria, pagina, total_registros)
    if titulo:
        if len(titulo) < 4:
            return {"error_message": "Titulo deve ter pelo menos 4 caracteres"}, 422
        response = LivroService().listar_livro_por_titulo(titulo, pagina, total_registros)

    return jsonify(response), 200

@app.route('/api/v1/books/<int:id_book>', methods=['GET'])
def get_book(id_book):
    """
    Buscar livro por ID
    ---
    parameters:
      - name: id_book
        in: path
        type: integer
        required: true
        description: ID do livro a ser buscado
    responses:
      200:
        description: Livro encontrado pelo ID
        schema:
          type: object
      404:
        description: Livro não encontrado
    """
    response = LivroService().listar_livro_por_id(id_book)

    return jsonify(response), 200

@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    """
    Listar categorias de livros
    ---
    responses:
      200:
        description: Lista de categorias disponíveis
        schema:
          type: array
          items:
            type: object
    """
    response = CategoriaService().listar_categorias()

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)