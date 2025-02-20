from colorama import  Style, Fore
from funcoes.intencao import *
from funcoes.produto import *
from funcoes.driver import *
from funcoes.ExcelSaver import *



def main():
    print(f"\n================================")
    print(f"Bem vindo ao Console de " +Fore.GREEN + "WebScraping"+  Style.RESET_ALL   +"\n\nAutor:" + Fore.RED + "GuilhermeFernandes" + Style.RESET_ALL)
    print(f"\n================================")
    menu()


def menu():
    print(f"\nAtualmente nossas opções são:\n1 - Amazon\n2 - Mercado Livre\n3 - Kabum\n4 - Sair")
    print("digite numero ou escreva sua opçao:")
    opcao = input()
    if (opcao.lower() == "amazon" or opcao == "1"):
        main_buscar("amazon")
        reentrada()
    elif (opcao.lower() == "mercado livre" or opcao == "2"):
        main_buscar("ml")
        reentrada()
    elif (opcao.lower() == "kabum" or opcao == "3"):
        main_buscar("kbm")
        reentrada()
    elif (opcao == "4"):
        print("Até logo :)!")
        return
    else:
        print("Não entendi, por favor começar novamente\n\n\n\n\n")
        menu()


def reentrada():
    print(f"\n================================")
    print(f"\n\nQuer fazer outra pesquisa?")
    print("\n1 - Sim")
    print("\n2 - Não")
    print(f"\n================================")
    opcao = input()
    if (opcao == "1" or opcao.lower() == "sim" or opcao.lower() == "s"):
        menu()
    elif (opcao.lower() == "nao" or opcao.lower() == "não" or opcao.lower() == "n" or opcao == "2"):
        print("Até logo :)!")
        return
    else:
        print("Não te entendi :( Mas até logo :)!")
        return
    
def main_buscar(loja):
    produto = Produto()
    IntencaoCliente = Intencao("","", loja ,False)

    IntencaoCliente.buscar_intencao()

    if IntencaoCliente.confirmado == False:
        return 

    busca = Searcher(IntencaoCliente.produto.lower(), IntencaoCliente.paginas)
    busca.configurar_driver()
    busca.buscar_produto(loja, produto, busca)
    produto.exibir_produtos()
    save = ExcelSaver(produto)
    save.salvar(loja)


main()