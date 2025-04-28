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
            
    inicio = time.time()
    print ("Iniciando o crawler às: ", time.strftime("%H:%M:%S", time.localtime(inicio)))
    
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
                # scroll_to_the_end(driver, ".hfpxzc")
                
                num_elements = len(driver.find_elements(By.CSS_SELECTOR, ".hfpxzc"))
            
                print(url)
                print(f"Total de elementos encontrados: {num_elements}")
                print("Iniciando a coleta de dados...")
                
                services = []
                for i in range(num_elements):  
                    try:
                            element = driver.find_elements(By.CSS_SELECTOR, ".hfpxzc")[i]
                            element.click()
                    except ElementClickInterceptedException:
                        continue
                        
                    element = driver.find_elements(By.CSS_SELECTOR, ".hfpxzc")[i]
                    element.click()
                    time.sleep(5) # Espera o carregamento da página
                    
                    print(f"Elemento {i+1} de {num_elements}")

                    service = {}
                    # Coletor de dados do estabelecimento
                    try:
                        service["estabelecimento"] = getEstabelecimento(driver)
                    except Exception as e:
                        print(f"Erro ao pegar informações do estabelecimento: {e}")
                        service["estabelecimento"] = None
                        
                    # Coletor de dados de avaliações
                    try:
                        service["resumo_avaliacoes"] = getResumoAvaliacoes(driver)
                    except Exception as e:
                        print(f"Erro ao pegar resumo de avaliações: {e}")
                        service["resumo_avaliacoes"] = None
                        
                    # Abrir aba "Sobre"
                    try:
                        openTab(driver, "Sobre")
                    
                        service["tags"] = getTags(driver)
                    except Exception as e:
                        print(f"Erro ao pegar tags: {e}")
                        service["tags"] = None
                    
                    # Abrir aba "Avaliações"
                    try:
                        openTab(driver, "Avaliações")                        
                        service["comentarios_e_respostas"] = getComentarios(driver)
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

