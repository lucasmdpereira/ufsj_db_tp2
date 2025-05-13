import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from google_places_categories import google_places_categories
from cities import cities
from services import prepares_string_for_search
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import django

def extract_id_gmaps(url):
    padrao = r'!16s%2Fg%2F([a-zA-Z0-9_-]+)'
    match = re.search(padrao, url)
    return match.group(1) if match else None

class FakeRequest:
    def __init__(self, data):
        self.data = data

class Estabelecimento:
    def __init__(self, link_google, categoria, nome, endereco, telefone, website):
        self.link_google = extract_id_gmaps(link_google)
        self.categoria = categoria
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.website = website
    
    def printJson(self):
        data = {
            "link_google": self.link_google,
            "categoria": self.categoria,
            "nome": self.nome,
            "endereco": self.endereco,
            "telefone": self.telefone,
            "website": self.website
        }

        print(json.dumps(data, ensure_ascii=False, indent=4))
        return data

class Comentario:
    def __init__(self, data_review_id, qtd_estrelas, qtd_curtidas, data, texto, usuario_qtd_avaliacoes, usuario_qtd_fotos, usuario_is_local_guide, link_google):
        self.data_review_id = data_review_id
        self.qtd_estrelas = int(qtd_estrelas)
        self.qtd_curtidas = qtd_curtidas
        self.data = data
        self.texto = texto
        self.usuario_qtd_avaliacoes = usuario_qtd_avaliacoes
        self.usuario_qtd_fotos = usuario_qtd_fotos
        self.usuario_is_local_guide = usuario_is_local_guide
        self.link_google = extract_id_gmaps(link_google)

    def printJson(self):
        data = {
            "data_review_id": self.data_review_id,
            "qtd_estrelas": self.qtd_estrelas,
            "qtd_curtidas": self.qtd_curtidas,
            "data": self.data,
            "texto": self.texto,
            "usuario_qtd_avaliacoes": self.usuario_qtd_avaliacoes,
            "usuario_qtd_fotos": self.usuario_qtd_fotos,
            "usuario_is_local_guide": self.usuario_is_local_guide,
            "link_google": self.link_google
        }
        
        print(json.dumps(data, ensure_ascii=False, indent=4))
        return data

class Resposta:
    def __init__(self, data_review_id, data, texto):
        self.data_review_id = data_review_id
        self.data = data
        self.texto = texto    

    def printJson(self):
        data = {
            "data_review_id": self.data_review_id,
            "data": self.data,
            "texto": self.texto
        }
    
        print(json.dumps(data, ensure_ascii=False, indent=4))
        return data
                
class ResumoAvaliacoes:
    def __init__(self,link_google, qnt_avaliacoes, media_estrelas, estrelas_1, estrelas_2, estrelas_3, estrelas_4, estrelas_5):
        self.link_google = extract_id_gmaps(link_google)
        self.qnt_avaliacoes = qnt_avaliacoes
        self.media_estrelas = media_estrelas
        self.estrelas_1 = estrelas_1
        self.estrelas_2 = estrelas_2
        self.estrelas_3 = estrelas_3        
        self.estrelas_4 = estrelas_4
        self.estrelas_5 = estrelas_5

    def printJson(self):
        data = {
            "link_google": self.link_google,
            "qtd_avaliacoes": self.qnt_avaliacoes,
            "media_estrelas": self.media_estrelas,
            "estrelas_1": self.estrelas_1,
            "estrelas_2": self.estrelas_2,
            "estrelas_3": self.estrelas_3,        
            "estrelas_4": self.estrelas_4, 
            "estrelas_5": self.estrelas_5
        }

        print(json.dumps(data, ensure_ascii=False, indent=4))
        return data

class EstabelecimentoTags:
    def __init__ (self, link_google, tag):
        self.link_google = extract_id_gmaps(link_google)
        self.tag = tag

    def printJson(self):
        data = {
            "link_google": self.link_google,
            "tag": self.tag  # tags é um vetor de strings
        }
        print(json.dumps(data, ensure_ascii=False, indent=4))
        return data

def main() -> None:
    def openTab(driver: webdriver.Chrome, tab_name: str) -> None:
        print(f"Abrindo aba: {tab_name}...")
        tab = driver.find_element(By.XPATH, f'//button[.//div[contains(@class, "NlVald") and normalize-space()="{tab_name}"]]')
        tab.click()
        time.sleep(5)
    
    def getTags(driver: webdriver.Chrome) -> list[str]:
        # iNvpkb
        print("Pegando Tags...")
        
        service = []
        driver.find_element(By.CSS_SELECTOR, ".iP2t7d").click()
        # scroll_to_the_end(driver, ".iP2t7d") 
        tags = driver.find_elements(By.CSS_SELECTOR, ".iNvpkb")
        for tag in tags:
            service.append(tag.text.split('\n')[1])
        
        return service
            
    def getComentarios(driver: webdriver.Chrome) -> dict:
        print("Pegando comentários e respostas...")
        driver.find_element(By.CSS_SELECTOR, ".vyucnb").click()
        # scroll_to_the_end(driver, ".jJc9Ad")        
        comentarios = driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad")
        service = {
            "comentarios": [],
            "respostas": [],
        }
        
        print(f"Total de comentários encontrados: {len(comentarios)}.")        
        for comentario in comentarios:           
            user_info = comentario.find_elements(By.CSS_SELECTOR, ".RfnDt")
            if len(user_info) > 0:
                user_info= user_info[0].text.split(" · ")
            
            avaliacoes = 0
            fotos = 0
            local_guide = False
            for item in user_info:
                if "avaliações" in item or "avaliação" in item:
                    avaliacoes = int(re.search(r'\d+', item).group())
                if "foto" in item:
                    fotos = int(re.search(r'\d+', item).group())
                if "Local Guide" in item:
                    local_guide = True
            
            service["comentarios"].append(
                {
                    "data_review_id": comentario.find_element(By.CSS_SELECTOR, ".WEBjve").get_attribute("data-review-id"),
                    "estrelas": comentario.find_element(By.CSS_SELECTOR, ".kvMYJc").get_attribute("aria-label"),
                    "data": comentario.find_element(By.CSS_SELECTOR, ".rsqaWe").text,
                    "texto": (e := comentario.find_elements(By.CSS_SELECTOR, ".wiI7pd")) and e[0].text or None,
                    "nome": comentario.find_element(By.CSS_SELECTOR, ".d4r55").text,
                    "local_guide": local_guide,
                    "fotos": fotos,
                    "avaliacoes": avaliacoes,
                    "curtidas": (e := comentario.find_elements(By.CSS_SELECTOR, ".pkWtMe")) and int(e[0].text) or 0,
                }
            )
            
            resposta = comentario.find_elements(By.CSS_SELECTOR, ".DZSIDd")
            if len(resposta) > 0:
                service["respostas"].append({
                    "data_review_id": comentario.find_element(By.CSS_SELECTOR, ".WEBjve").get_attribute("data-review-id"),
                    "data": comentario.find_element(By.CSS_SELECTOR, ".DZSIDd").text,
                    "texto": comentario.find_elements(By.CSS_SELECTOR, ".wiI7pd")[-1].text,
                })
                
                # trata casos de comentários que não possuem texto, mas possuem resposta
                if service["comentarios"][-1]["texto"] == service["respostas"][-1]["texto"]:
                    service["comentarios"][-1]["texto"] = None
            
        return service

    def getResumoAvaliacoes(driver: webdriver.Chrome) -> dict:
        print("Pegando resumo de avaliações...")
        service = {}
        service['media'] = (e := driver.find_elements(By.CSS_SELECTOR, ".fontDisplayLarge")) and e[0].text or None
        service['avaliacoes'] = (e := driver.find_elements(By.CSS_SELECTOR, ".HHrUdb")) and e[0].text or None
        
        estrelas = (e := driver.find_elements(By.CSS_SELECTOR, ".BHOKXe")) or None
        if estrelas:
            service['5_estrela'] = estrelas[0].get_attribute('aria-label')
            service['4_estrela'] = estrelas[1].get_attribute('aria-label')
            service['3_estrela'] = estrelas[2].get_attribute('aria-label')
            service['2_estrela'] = estrelas[3].get_attribute('aria-label')
            service['1_estrela'] = estrelas[4].get_attribute('aria-label')
        return service
    
    def getEstabelecimento(driver: webdriver.Chrome) -> dict:
        print("Pegando informações do estabelecimento...")
        service = {}
        service['link'] = driver.current_url
        service['categoria'] = (e := driver.find_elements(By.CSS_SELECTOR, ".DkEaL")) and e[0].text or None
        service['nome'] = (e := driver.find_elements(By.CSS_SELECTOR, ".DUwDvf.lfPIob")) and e[0].text or None
        service['endereco'] = (e := driver.find_elements(By.XPATH, '//button[@data-item-id="address"]//div[contains(@class,"Io6YTe")]')) and e[0].text or None

        e = driver.find_elements(By.XPATH, '//button[@data-tooltip="Copiar número de telefone"]')
        telefone_aria_label = e[0].get_attribute('aria-label') if e else None
        service['telefone'] = ''.join(filter(str.isdigit, telefone_aria_label)) if telefone_aria_label else None
        service['website'] = (e := driver.find_elements(By.XPATH, '//a[@data-item-id="authority"]')) and e[0].get_attribute('href') or None
        return service
            
    def scroll_to_the_end(driver: webdriver.Chrome, css_class_elements) -> None:
        print("Scrolling...")
        while True:
            last_number_of_reviews = driver.find_elements(By.CSS_SELECTOR, css_class_elements)
            ActionChains(driver).send_keys(Keys.END).perform()
            time.sleep(2)  # Espera o carregamento da página
            new_number_of_reviews = driver.find_elements(By.CSS_SELECTOR, css_class_elements)
            
            if len(last_number_of_reviews) == len(new_number_of_reviews): 
                """
                    Se o número de elementos não mudou, significa que a página foi carregada completamente.
                    Retry para conferir se todos os elementos foram carregados, ou foi atraso na conexão
                """
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(10)  # Espera o carregamento da página
                new_number_of_reviews = driver.find_elements(By.CSS_SELECTOR, css_class_elements) 
                if len(last_number_of_reviews) == len(new_number_of_reviews):
                    break
        ActionChains(driver).send_keys(Keys.HOME).perform()
        print("Todas as entidades foram carregados.")
    
    def formatDate(dataString) -> str:
        numero, palavra = dataString.split()[:2]
        if numero == "um" or numero == "uma":
            numero = 1
        else:
            numero = int(numero)

        dataAtual = datetime.now()

        if numero == 1:
            if(palavra == "ano"):
                dataCalculada = dataAtual - relativedelta(years=1)
            elif(palavra == "mês"):
                dataCalculada = dataAtual - relativedelta(months=1)
            elif(palavra == "semana"):
                dataCalculada = dataAtual - relativedelta(weeks=1)
            elif(palavra == "dia"):
                dataCalculada = dataAtual - relativedelta(days=1)
            else:   
                dataCalculada = dataAtual
        elif palavra == "anos":
            dataCalculada = dataAtual - relativedelta(years=numero)
        elif palavra == "meses" :
            dataCalculada = dataAtual - relativedelta(months=numero)
        elif palavra == "semanas":
            dataCalculada = dataAtual - relativedelta(weeks=numero)
        elif palavra == "dias":
            dataCalculada = dataAtual - relativedelta(days=numero)
        
        else:
            dataCalculada = dataAtual
        
        return dataCalculada.strftime("%Y-%m-%d")
    
    def formatEstabelecimento(service) -> Estabelecimento:
        estabelecimento = Estabelecimento(
            link_google=service["estabelecimento"].get("link")[-255:],
            categoria=service["estabelecimento"].get("categoria"),
            nome=service["estabelecimento"].get("nome"),
            endereco=service["estabelecimento"].get("endereco"),
            telefone=service["estabelecimento"].get("telefone"),
            website=service["estabelecimento"].get("website"),
        )
        return estabelecimento
    
    def formatComentario(linkGoogle, comentario) -> Comentario:
        return Comentario(
            link_google= linkGoogle,
            data_review_id= comentario["data_review_id"],
            qtd_estrelas = int(comentario["estrelas"].split()[0]),
            data= formatDate(comentario["data"]),
            texto= comentario["texto"],
            usuario_is_local_guide= comentario["local_guide"],
            usuario_qtd_fotos= comentario["fotos"],
            usuario_qtd_avaliacoes= comentario["avaliacoes"],
            qtd_curtidas= comentario["curtidas"]
        )

    def formatResposta(resposta) -> Resposta:
            return Resposta(
                data_review_id= resposta["data_review_id"],
                data= formatDate(resposta["data"]),
                texto= resposta["texto"]
            )

    def formatResumoAvaliacoes(service) -> ResumoAvaliacoes:
        linkGoogle = service["estabelecimento"].get("link")[-255:]

        resumoAvaliacoes = ResumoAvaliacoes(
            link_google = linkGoogle,
            qnt_avaliacoes= int(service["resumo_avaliacoes"].get("avaliacoes").replace(".", "").split()[0]),
            media_estrelas= float(service["resumo_avaliacoes"].get("media").replace(",", ".")),
            estrelas_1= int(service["resumo_avaliacoes"].get("1_estrela").split(",")[1].split()[0]),
            estrelas_2= int(service["resumo_avaliacoes"].get("2_estrela").split(",")[1].split()[0]),
            estrelas_3= int(service["resumo_avaliacoes"].get("3_estrela").split(",")[1].split()[0]),       
            estrelas_4= int(service["resumo_avaliacoes"].get("4_estrela").split(",")[1].split()[0]),
            estrelas_5= int(service["resumo_avaliacoes"].get("5_estrela").split(",")[1].split()[0])
        )
        return resumoAvaliacoes

    def formatEstabelecimentoTags(service) -> Estabelecimento:
        tagsEstabelecimento = []
        for tag in service["tags"]:
            tagsEstabelecimento.append(tag)
        estabelecimentoTags = EstabelecimentoTags(
            link_google=service["estabelecimento"].get("link")[-255:],
            tag= tagsEstabelecimento
        )
        return estabelecimentoTags
    
    inicio = time.time()
    print ("Iniciando o crawler às: ", time.strftime("%H:%M:%S", time.localtime(inicio)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tp2.settings')
    django.setup()
    from v1.views.estabelecimento_views import EstabelecimentoView
    from v1.views.resumo_de_avaliacoes_views import ResumoDeAvaliacoesViewSet
    from v1.views.estabelecimento_tag_views import EstabelecimentoTagView
    from v1.views.comentario_views import ComentarioViewSet
    from v1.views.resposta_views import RespostaViewSet
    from v1.views.tag_views import TagViewSet
    
    for city in cities:
        print(f"Buscando em: {city}...")
        city = prepares_string_for_search(city)
        
        for (_, subcategories) in google_places_categories.items():
            for subcategory in subcategories:
                print("Inicializando o navegador...")
                options = webdriver.ChromeOptions()
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--headless")  # Sem abrir o chrome
                driver = webdriver.Chrome(options=options)
                
                print(f"Buscando subcategoria: {subcategory}...")
                url = f"https://www.google.com/maps/search/{subcategory}+in+{city}"     
                driver.get(url)
                driver.find_element(By.CSS_SELECTOR, ".JrN27d.SuV3fd.Zjt37e.TGiyyc").click()
                scroll_to_the_end(driver, ".hfpxzc")
                
                num_elements = len(driver.find_elements(By.CSS_SELECTOR, ".hfpxzc"))
            
                print(url)
                print(f"Total de elementos encontrados: {num_elements}")
                print("Iniciando a coleta de dados...")
                
                services = []
                for i in range(num_elements):
                    try:
                        element = driver.find_elements(By.CSS_SELECTOR, ".hfpxzc")[i]
                        element.click()
                        time.sleep(5) # Espera o carregamento da página
                    except ElementClickInterceptedException:
                        continue
                        

                    print(f"Elemento {i+1} de {num_elements}")

                    service = {}
                    # Coletor de dados do estabelecimento
                    try:
                        service["estabelecimento"] = getEstabelecimento(driver)
                        estabelecimento = formatEstabelecimento(service)
                        EstabelecimentoView().create(FakeRequest(estabelecimento.printJson()))
                    except Exception as e:
                        print(f"Erro ao pegar informações do estabelecimento: {e}")
                        service["estabelecimento"] = None
                        
                    # Coletor de dados de avaliações
                    try:
                        service["resumo_avaliacoes"] = getResumoAvaliacoes(driver)
                        resumo_avaliacoes = formatResumoAvaliacoes(service)
                        ResumoDeAvaliacoesViewSet().create(FakeRequest(resumo_avaliacoes.printJson()))
                    except Exception as e:
                        print(f"Erro ao pegar resumo de avaliações: {e}")
                        service["resumo_avaliacoes"] = None
                        
                    # Abrir aba "Sobre"
                    try:
                        openTab(driver, "Sobre")
                    
                        service["tags"] = getTags(driver)
                        tags = formatEstabelecimentoTags(service)
                        for tag in tags.tag:
                            try:
                                TagViewSet().create(FakeRequest({"tag": tag}))
                            except Exception as e:
                                print(f"Erro ao salvar tags: {e}")
                            try:
                                EstabelecimentoTagView().create(FakeRequest({"link_google": tags.link_google, "tag": tag}))
                            except Exception as e:
                                print(f"Erro ao salvar tags: {e}") 
                    except Exception as e:
                        print(f"Erro ao pegar tags: {e}")
                        service["tags"] = None
                    
                    # Abrir aba "Avaliações"
                    try:
                        openTab(driver, "Avaliações")                        
                        service["comentarios_e_respostas"] = getComentarios(driver)
                        linkGoogle = service["estabelecimento"].get("link")[-255:]
                        for comentario in service["comentarios_e_respostas"]["comentarios"]:
                            comentario = formatComentario(linkGoogle, comentario)
                            ComentarioViewSet().create(FakeRequest(comentario.printJson()))
                        for resposta in service["comentarios_e_respostas"]["respostas"]:
                            resposta = formatResposta(resposta)
                            RespostaViewSet().create(FakeRequest(resposta.printJson()))

                    except Exception as e:
                        print(f"Erro ao pegar comentários e respostas: {e}")
                        service["comentarios_e_respostas"] = None

                    services.append(service)
                    print(f"Tempo de execução: {time.time() - inicio:.4f} segundos.")
                    
                print(f"Tempo de execução: {time.time() - inicio:.4f} segundos.")
                
                print("Salvando informações em um arquivo JSON...")
                with open(f'{subcategory}_{city.replace('+', "_")}.json', 'w', encoding='utf-8') as f:
                    json.dump(
                        services,
                        f,
                        ensure_ascii=False,  # Preserva caracteres especiais (ç, á, etc.)
                        indent=4,           # Indentação de 4 espaços
                    )

                print("Arquivo salvo com sucesso!")
                driver.quit()
            print(f"Tempo de execução: {time.time() - inicio:.4f} segundos.")
        print(f"Tempo de execução: {time.time() - inicio:.4f} segundos.")
main()

