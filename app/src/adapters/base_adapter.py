import pandas as pd


class BaseAdapter:
    def ler_base_categorias(self):
        df = pd.read_csv('../bases/categorias.csv', sep=',')

        return df

    def ler_base_livros(self):
        df = pd.read_csv('../bases/base_livros.csv', sep=',')
        df['id'] = df.index

        return df