import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from colorama import init
from colorama import Fore, Back, Style
from decouple import config


def get_mercado_livre_url(search_term, page):
    template = 'https://lista.mercadolivre.com.br/{}'
    url = search_term.replace(' ', '-')
    multiplier = 51 * (page - 1)
    if (page > 1):
        template += f'_Desde_{multiplier}_NoIndex_True'
        print(f"\n\nPagina {page}\n\n")
        return template.format(url)
    else:
        template += '#D[A:{}]'
        pos = search_term.replace(' ', '%20')
        print(f"\n\nPagina {page}\n\n")
        return template.format(url, pos)


def main_mercado_livre():
    texto = []
    preco = []
    nome = []
    link = []
    count = 0

    print("\nInsira O produto que você quer pesquisa no Mercado Livre:\n")
    produto = input()

    print(f'Confirme o Produto: {produto}\n S ou N')
    confirmacao = input()

    if (confirmacao.lower() != 's'):
        return main_mercado_livre()

    print("\nInsira a quantidade de Paginas para pesquisa:")
    pages = input()
    if (pages.isnumeric() == False):
        print("\nInsira numero Por favor! Retornando ao menu inicial.")
        return main_mercado_livre()
    if (pages == "0"):
        print("\nInsira numero maior que zero Por favor! Retornando ao menu inicial.")
        return main_mercado_livre()
    PATH = config("PROFILE_PATH")
    profile_path = PATH
    options = Options()
    options.set_preference('profile', profile_path)
    driver = webdriver.Firefox(options=options)
    for page in range(1, (int(pages)+1)):
        url = get_mercado_livre_url(produto.lower(), page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all(
            'div', {'class': 'ui-search-result__wrapper shops__result-wrapper'})
        texto = (mercado_livre_extract(results))
        # nome, preco, link
        count += 1
        xounter = 0
        for item in texto[0]:
            nome.append(texto[0][xounter])
            preco.append(texto[1][xounter])
            link.append(texto[2][xounter])
            xounter += 1
    driver.quit()

    print(f'\n\n Deseja Salvar em EXCEL? S ou N')
    excel = input()
    if (excel.lower() != 's'):
        print(f'Obrigado por Usar!')
        return
    print(f'\n\nDigite o um nove para o arquivo')
    arquivo = input()
    Save(nome, preco, link, arquivo)



def mercado_livre_extract(results):
    salvar = []
    preco = []
    nome = []
    link = []
    count = 0
    record = []
    nme = []
    prc = []
    rl = []

    for x in results:
        record.append(x)
    print(f'Quantidade de Produtos na Pagina {len(record)}')

    for i in record:
        tag = i.a
        name = tag.get('title')
        # Descrição e URL
        url = tag.get('href')
        # Preço
        try:
            price_parent = i.find(
                'div', 'ui-search-price__second-line shops__price-second-line')
            price = price_parent.find('span', 'price-tag-fraction').text 
            if(price_parent.find('span', 'price-tag-cents') != None):
                price +="." +price_parent.find('span', 'price-tag-cents').text
        except AttributeError:
            price = "Não encontrado"

        nme.append(name)
        prc.append(price)
        rl.append(url)

    resultado = (nme, prc, rl)
    for x in resultado[0]:
        if resultado:
            salvar.append(resultado)
            nome.append(resultado[0][count])
            preco.append(resultado[1][count])
            link.append(resultado[2][count])
            count += 1
    ShowResults(nome, preco, link)

    return nome, preco, link, salvar


def ShowResults(nome, preco, link,):
    counter = 0

    for d in nome:
        print(f"______________________________")
        print(f"|Numero do produto na pagina: {counter+1}")
        print(f"            Nome: "+Fore.RED +
              f"{nome[counter]} " + Style.RESET_ALL + f"-- preco: R$ {preco[counter]}\n{link[counter]}  |")
        counter += 1


def Save(nome, preco, link, arquivo):
    writer = pd.ExcelWriter(f'{arquivo}.xlsx', engine='xlsxwriter')
    columns = ['Nome do Produto', 'Preço $', 'Url']
    df = pd.DataFrame(list(zip(nome, preco, link)), columns=columns)
    df.to_excel(writer, sheet_name=f'PAG 0', startrow=0, startcol=0)
    print('Salvo com Sucesso!!')
    writer.close()
