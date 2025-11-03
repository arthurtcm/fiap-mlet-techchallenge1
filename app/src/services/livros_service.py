from src.adapters.base_adapter import BaseAdapter


class LivroService:
    def __init__(self):
        self.base_adapter = BaseAdapter()

    def listar_livros(self, pagina, total_registros):
        if pagina < 1 or total_registros < 1:
            return []

        df = self.base_adapter.ler_base_livros()

        primeiro_registro = (pagina - 1) * total_registros
        ultimo_registro = primeiro_registro + total_registros

        df_pagina = df.iloc[primeiro_registro:ultimo_registro]
        livros = df_pagina.to_dict(orient='records')

        info = {
            "total_registros_retornados": len(livros),
            "pagina_atual": pagina,
            "total_registros": df.__len__()
        }
        return {"books": livros, "info": info}

    def listar_livro_por_categoria(self, categoria, pagina, total_registros):
        if pagina < 1 or total_registros < 1:
            return []

        df = self.base_adapter.ler_base_livros()

        primeiro_registro = (pagina - 1) * total_registros
        ultimo_registro = primeiro_registro + total_registros

        df_categoria = df[(df['categoria'] == categoria)]

        df_pagina = df_categoria.iloc[primeiro_registro:ultimo_registro]
        livros = df_pagina.to_dict(orient='records')

        info = {
            "total_registros_retornados": len(livros),
            "pagina_atual": pagina,
            "total_registros": df_categoria.__len__()
        }
        return {"books": livros, "info": info}

    def listar_livro_por_titulo(self, titulo, pagina, total_registros):
        if pagina < 1 or total_registros < 1:
            return []

        df = self.base_adapter.ler_base_livros()

        primeiro_registro = (pagina - 1) * total_registros
        ultimo_registro = primeiro_registro + total_registros

        df_titulo = df[df['titulo'].str.contains(titulo, case=False, na=False)]

        df_pagina = df_titulo.iloc[primeiro_registro:ultimo_registro]
        livros = df_pagina.to_dict(orient='records')

        info = {
            "total_registros_retornados": len(livros),
            "pagina_atual": pagina,
            "total_registros": df.__len__()
        }
        return {"books": livros, "info": info}

    def listar_livro_por_id(self, id):
        df = self.base_adapter.ler_base_livros()

        df_id = df[df['id'] == id]
        livros = df_id.to_dict(orient='records')

        return {"books": livros}