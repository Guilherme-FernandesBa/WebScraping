from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from decouple import config

class Searcher:
    def __init__(self, produto, paginas):
        """
        Inicializa a classe Searcher com os parâmetros necessários.

        Args:
        produto (str): O produto que o usuário deseja pesquisar.
        paginas (int): O número de páginas de resultados a serem processadas.
        profile_path (str): O caminho do perfil do navegador.
        """
        self.produto = produto
        self.paginas = paginas
        self.profile_path = config("PROFILE_PATH")
        self.driver = None
        self.resultados  = None

    def configurar_driver(self):

        options = Options()
        options.set_preference('profile', self.profile_path)
        self.driver = webdriver.Firefox(options=options)

    def buscar_produto(self, loja, produto,busca):
      
        try:
            
            if not isinstance(self.paginas, int) or self.paginas < 1:
                raise ValueError("O número de páginas deve ser maior que 0.")

            
            for page in range(1, self.paginas + 1):
                url = self.get_url(self.produto.lower(), page, loja)
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                if(loja.lower() == "amazon"):
                    results = soup.find_all('div', {'data-component-type': 's-search-result'})
                elif(loja.lower() == "ml"):
                    results = soup.find_all('li', {'class': 'ui-search-layout__item'})
                elif(loja.lower() == "kbm"):
                    results = soup.find_all('div', {'class': 'p-[2px] rounded-4 group bg-white shadow-[0_0_1px_rgba(40,41,61,0.08),0_0.5px_2px_rgba(96,97,112,0.16)] hover:shadow-lg'})
                            
                self.resultados = results
                busca.extract(busca.resultados, produto, loja)
                
                

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            self.driver.quit()

    def get_url(self, produto, page, loja):
     
        if loja.lower() == 'amazon':
            return f'https://www.amazon.com.br/s?k={produto}&page={page}&ref=nb_sb_ss_sc_2_9'
        elif loja.lower() == 'ml':
             return f'https://lista.mercadolivre.com.br/{produto}'
        elif loja.lower() =="kbm":
             return f'https://www.kabum.com.br/busca/{produto}?page_number={page}&page_size=60&facet_filters=&sort=most_searched&variant=null'
   
    def extract(self, results, produto, loja):
        if(loja.lower() == 'amazon'):
            self.extract_amazon(results, produto)
        elif(loja.lower() == 'ml'):
            self.extract_mercado_livre(results, produto)
        elif loja.lower() =="kbm":
            self.extract_kabum(results, produto)
        return produto
    
    def extract_amazon(self, results, produto):
            for x in results:
                tag = x.find('a', class_='a-link-normal s-line-clamp-4 s-link-style a-text-normal')
                if tag:
                    name = tag.text.strip()
                    url = 'https://www.amazon.com.br'+tag.get('href')
                    price = "Não encontrado"
                    rating = 'Classificação não encontrada'
                    review_count = 'Número de reviews não encontrado'
                    try:
                        price_parent = x.find('span', 'a-price')
                        if price_parent:
                            price = price_parent.find('span', 'a-offscreen').text.strip()  
                            price = price.replace('R$', '').strip()  
                            price = price.replace('.', '') 
                            price = price.replace(',', '.') 
                            price = float(price)  
                    except AttributeError:
                            pass  
                    try:
                        rating = x.i.text
                    except AttributeError:
                        pass
                    try:
                        parent = x.find('div', {'class': 'a-row a-size-small'})
                        if parent:
                            review_count_parent = parent.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style'})
                            if review_count_parent:
                                review_count = review_count_parent.find('span', 'a-size-base s-underline-text').text.replace('(', '').replace(')', '')
                    except AttributeError:
                        pass
                    produto.adicionar_produto(name, price, review_count, rating, url)


    def extract_mercado_livre(self, results, produto):
         for x in results:
                tag = x.find('a', class_='poly-component__title')
                if tag:
                    name = tag.text.strip()
                    url = tag.get('href')
                    price = "Não encontrado"
                    rating = 'Classificação não encontrada'
                    review_count = 'Número de reviews não encontrado'
                    try:
                        price_parent = x.find('span', 'andes-money-amount__fraction')
                        if price_parent:
                            price_cents = x.find('span', 'andes-money-amount__cents andes-money-amount__cents--superscript-24')
                            if price_cents:
                                    price = price_parent.text.strip() +"." + price_cents.text.strip()
                            else:
                                price = price_parent.text.strip()
                    except AttributeError:
                            pass  
                    try:
                        rating = x.find('span', 'poly-reviews__rating').text.strip()
                    except AttributeError:
                        pass
                    try:
                        parent = x.find('span', {'class': 'poly-reviews__total'})
                        if parent:
                            review_count= parent.text.strip().replace("(", "").replace(")", "")
                    except AttributeError:
                        pass
                    produto.adicionar_produto(name, price, review_count, rating, url)
        

    def extract_kabum(self, results, produto):
        for x in results:
            tag = x.find('span', class_='nameCard')
            link = x.find('a', class_='productLink')
            if tag:
                name = tag.text.strip()
                url = 'https://www.kabum.com.br'+link.get('href')
                price = "Não encontrado"
                rating = 'Classificação não encontrada'
                review_count = 'Número de reviews não encontrado'
                try:
                    price_parent = x.find('span', 'priceCard')
                    if price_parent:
                        price = price_parent.text.strip()  
                        price = price.replace('R$', '').strip()  
                        price = price.replace('.', '') 
                        price = price.replace(',', '.') 
                        price = float(price)  
                except AttributeError:
                        pass  
                try:
                    rating = x.find('div', class_='sc-idOiZg iqaGdw ratingStarsContainer').get("aria-label")
                except AttributeError:
                    pass
                try:
                    parent = x.find('span', {'class': 'text-xxs text-black-600 leading-none pt-4'})
                    if parent:
                        review_count= parent.text.strip().replace("(", "").replace(")", "")
                except AttributeError:
                    pass
                produto.adicionar_produto(name, price, review_count, rating, url)