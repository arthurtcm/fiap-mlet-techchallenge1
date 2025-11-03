from src.adapters.base_adapter import BaseAdapter


class CategoriaService:
    def __init__(self):
        self.base_adapter = BaseAdapter()

    def listar_categorias(self):
        df = self.base_adapter.ler_base_categorias()
        categorias = df.to_dict(orient='records')

        return {"categories": categorias}