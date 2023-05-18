import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from colorama import init
from colorama import Fore, Back, Style


def get_amazon_url(search_term, page):
    template='https://www.amazon.com.br/s?k={}&ref=nb_sb_ss_sc_2_9'
    url = search_term.replace(' ', '+')
    
    if page > 0:
        url +=f"&page={page}" 
    print(f"\n\nPagina {page}\n\n")
    return template.format(url)



def amazon_extract(results):
    salvar = []
    preco =[]
    nome =[]
    link = []
    review =[]
    stars =[]
    count = 0
    record =[]
    nme = []
    prc =[]
    rting =[]
    rvwe =[]
    rl =[]

    for x in results:
        record.append(x)
    print(f'Quantidade de Produtos na Pagina{len(record)}')

    for i in record:
        tag = i.h2.a
        name =tag.text.strip()
        #Descrição e URL
        url= 'https://www.amazon.com.br'+tag.get('href') 
        #Preço
        try:
            price_parent = i.find('span', 'a-price')
            price =price_parent.find('span', 'a-offscreen').text
            price = price.replace('R$', '')
        except AttributeError:
            price = "Não encontrado"


        try:
            rating =i.i.text
        except AttributeError:
            rating = 'Classificação não encontrada'

        try:
            parent = i.find('div', {'class': 'a-row a-size-small'})
            review_count_parent = parent.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style'})
            review_count = review_count_parent.find('span', 'a-size-base s-underline-text').text 
            review_count = review_count.replace('(', '')
            review_count = review_count.replace(')', '')
        except AttributeError:
            review_count = 'Numero de reviews não encontrada'

        nme.append(name)
        prc.append(price)
        rting.append(rating)
        rvwe.append(review_count)
        rl.append(url)

    resultado = (nme, prc, rting, rvwe, rl)
    for x in resultado[0]:
        if resultado:
            salvar.append(resultado)
            nome.append(resultado[0][count])
            preco.append(resultado[1][count])
            review.append(resultado[2][count])
            stars.append(resultado[3][count])
            link.append(resultado[4][count])  
            count +=1
    ShowResults(nome, preco,review,stars, link, salvar)

    return nome, preco, review, stars, link, salvar

def ShowResults(nome, preco, review, stars, link, salvar):
    counter =0

    for d in nome:
        print(f"______________________________")
        print(f"|Numero do produto na pagina: {counter+1}") 
        print(f"            Nome: "+Fore.RED + f"{nome[counter]} " + Style.RESET_ALL + f"-- preco: R$ {preco[counter]}\n{link[counter]}  |")     
        counter += 1

def Save(nome, preco, review, stars, link, arquivo):
    writer = pd.ExcelWriter(f'{arquivo}.xlsx', engine='xlsxwriter')
    columns=['Nome do Produto', 'Preço $', 'Reviews', 'Ranqueamento', 'Url']
    df = pd.DataFrame(list(zip(nome, preco, review, stars, link)), columns=columns)
    df.to_excel(writer, sheet_name=f'PAG 0', startrow=0 , startcol=0)
    #print(df)
    print('Salvo com Sucesso!!')
    writer.close()



def main_amazon():
    texto =[]
    preco =[]
    nome =[]
    link = []
    review =[]
    stars =[]
    count = 0

    print("\nInsira O produto que você quer pesquisa na Amazon:\n")
    produto= input()

    print(f'Confirme o Produto: {produto}\n S ou N')
    confirmacao = input();

    if(confirmacao.lower() != 's'):
        return main_amazon()

    print("\nInsira a quantidade de Paginas para pesquisa:")
    pages = input()
    if(pages.isnumeric() == False):
        print("\nInsira numero Por favor! Retornando ao menu inicial.")
        return main_amazon()
    if(pages =="0"):
        print("\nInsira numero maior que zero Por favor! Retornando ao menu inicial.")
        return main_amazon()

    profile_path = r'C:\joseg\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\y1uqp5mi.default'
    options=Options()
    options.set_preference('profile', profile_path)
    driver = webdriver.Firefox(options=options)
    for page in range(1,(int(pages)+1)):
        url = get_amazon_url(produto.lower(), page)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results =  soup.find_all('div', {'data-component-type': 's-search-result'})
        texto = (amazon_extract(results))
        #nome, preco, review, stars, link
        count +=1
        xounter = 0
        for item in texto[0]:
            nome.append(texto[0][xounter])
            preco.append(texto[1][xounter])
            review.append(texto[2][xounter])
            stars.append(texto[3][xounter])
            link.append(texto[4][xounter])
            xounter +=1
    driver.quit()

    print(f'\n\n Deseja Salvar em EXCEL? S ou N')
    excel = input()
    if(excel.lower() != 's'):
        print(f'Obrigado por Usar!')
        return 
    print(f'\n\nDigite o um nove para o arquivo')
    arquivo = input()
    Save(nome, preco, review, stars, link, arquivo)





main_amazon()
