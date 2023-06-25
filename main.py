from amazon import main_amazon
from mercadoLivre import main_mercado_livre
from colorama import init
from colorama import  Style, Fore



def main():
    print(f"\n================================")
    print(f"Bem vindo ao Console de " +Fore.GREEN + "WebScraping"+  Style.RESET_ALL   +"\n\nAutor:" + Fore.RED + "GuilhermeFernandes" + Style.RESET_ALL)
    print(f"\n================================")
    menu()


def menu():
    print(f"\nAtualmente nossas opções são:\n1 - Amazon\n2 - Mercado Livre\n3 - Sair")
    print("digite numero ou escreva sua opçao:")
    opcao = input()
    if (opcao.lower() == "amazon" or opcao == "1"):
        main_amazon()
        reentrada()
    elif (opcao.lower() == "mercado livre" or opcao == "2"):
        main_mercado_livre()
        reentrada()
    elif (opcao == "3"):
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
    

main()