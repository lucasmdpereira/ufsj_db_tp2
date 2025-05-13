import re
import unicodedata
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

def formatDate(dataString) -> str:
    numero, palavra = dataString.split()[:2]
    numero = 1 if numero in {"um", "uma"} else int(numero)

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

def extract_id_gmaps(url):
    padrao = r'!16s%2Fg%2F([a-zA-Z0-9_-]+)'
    match = re.search(padrao, url)
    return match.group(1) if match else None

def sanitize_search_string(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text.lower()

def prepares_string_for_search(text: str) -> str:
    text = sanitize_search_string(text)
    return text.replace(' ', '+')