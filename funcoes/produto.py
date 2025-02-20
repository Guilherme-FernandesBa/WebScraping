from colorama import Fore, Style

class Produto:
    def __init__(self):
        """
        Inicializa os atributos relacionados ao produto.
        """
        self.texto = []  # Lista que pode conter descrições ou outras informações relacionadas ao produto
        self.preco = []  # Lista de preços
        self.nome = []   # Lista de nomes de produtos
        self.link = []   # Lista de links para os produtos
        self.review = [] # Lista de reviews ou avaliações dos produtos
        self.stars = []  # Lista de estrelas ou classificação do produto
        self.count = 0    # Contador, por exemplo, para contar quantos produtos foram adicionados

    def adicionar_produto(self, nome, preco, review, stars, link):
        """
        Adiciona um produto à lista de produtos.
        
        Args:
        nome (str): Nome do produto
        preco (str): Preço do produto
        review (str): Comentários ou avaliações sobre o produto
        stars (float): Estrelas ou classificação do produto
        link (str): Link do produto
        """
        self.nome.append(nome)
        self.preco.append(preco)
        self.review.append(review)
        self.stars.append(stars)
        self.link.append(link)
        self.count += 1  # Incrementa o contador a cada novo produto

    def exibir_produtos(self):

        for i in range(self.count):
            print("-" * 30)
            print(f"|Numero do produto na pagina: {i+1}")
            print(f"Nome: "+Fore.RED + f"{self.nome[i]} " + Style.RESET_ALL + f"-- preco: R$ {self.preco[i]}\n{self.link[i]}  |")

            # Editar da forma como preferir
            # print(f"  Nome: {self.nome[i]}")
            # print(f"  Preço: {self.preco[i]}")
            # print(f"  Review: {self.review[i]}")
            # print(f"  Estrelas: {self.stars[i]}")
            # print(f"  Link: {self.link[i]}")
           




