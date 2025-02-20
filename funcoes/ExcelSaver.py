import pandas as pd

class ExcelSaver:
    def __init__(self, produto):
   
        self.produto = produto

    def salvar(self, loja):

        print(f'\n\n Deseja Salvar em EXCEL? S ou N')
        excel = input()

        if (excel.lower() != 's'):
            print(f'Obrigado por Usar!')
            return
        
        print(f'\n\nDigite o um nove para o arquivo')
        arquivo = input()
        try:
          
            writer = pd.ExcelWriter(f'{arquivo}.xlsx', engine='xlsxwriter')
            if loja.lower() != 'amazon':
                columns = ['Nome do Produto', 'Preço $', 'Reviews', 'Ranqueamento', 'Url']

                df = pd.DataFrame(
                    list(zip(self.produto.nome, self.produto.preco, self.produto.review, 
                            self.produto.stars, self.produto.link)), columns=columns)

                df.to_excel(writer, sheet_name=f'PAG 0', startrow=0, startcol=0)

                print('Salvo com Sucesso!!')
            else:
                columns = ['Nome do Produto', 'Preço $', 'Reviews', 'Ranqueamento', 'Url']

                df = pd.DataFrame(
                    list(zip(self.produto.nome, self.produto.preco, self.produto.review, 
                            self.produto.stars, self.produto.link)), columns=columns)
                df.to_excel(writer, sheet_name=f'PAG 0', startrow=0, startcol=0)
                print('Salvo com Sucesso!!')

            
            writer.close()

        except Exception as e:
            print(f"Ocorreu um erro ao salvar o arquivo: {e}")

