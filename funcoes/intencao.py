class Intencao:
    """
    Classe que representa a intenção de busca de um produto.

    Atributos:
    produto (str): O nome do produto que o usuário deseja buscar.
    paginas (int): Quantidade de páginas a serem pesquisadas.
    confirmado (bool): Se a intenção foi confirmada pelo usuário.
    """
    
    def __init__(self, produto, paginas,loja, confirmado=False,):

        self.produto = produto
        self.paginas = paginas
        self.loja = loja
        self.confirmado = confirmado
        

    def __str__(self):
        return f'Produto: {self.produto}, Páginas: {self.paginas}'
   
   
   
    def buscar_intencao(self):
        produto = input("\nInsira o produto que você quer pesquisar:\n")
        
        confirmacao = input(f'Confirme o produto: {produto}\nS ou N: ').strip().lower()

        if confirmacao != 's':  
            print("Intenção não confirmada. Retornando aos dados originais.")
            return self 
        
     
        while True:
            try:
                paginas = int(input("\nInsira a quantidade de páginas para pesquisa (número): "))
                if paginas < 1:
                    print("Número de páginas não pode ser menor que 1. Tente novamente.")
                    continue  
                break 
            except ValueError:
                print("Entrada inválida. Insira um número válido para páginas.")
        
        if self.loja == "amazon":
            self.produto = produto.replace(' ', '+')
        elif self.loja == "ml":
            self.produto = produto.replace(' ', '-')
            multiplier = 51 * (paginas - 1)
            if (paginas > 1):
                self.produto += f'_Desde_{multiplier}_NoIndex_True'
            else:
                self.produto += f'_NoIndex_True#D[A:{self.produto.replace(' ', '%20')},on]'
        elif self.loja == "kbm":
            self.produto = produto.replace(' ', '-')   

        self.paginas = paginas
        self.confirmado = True

        return self

        
            