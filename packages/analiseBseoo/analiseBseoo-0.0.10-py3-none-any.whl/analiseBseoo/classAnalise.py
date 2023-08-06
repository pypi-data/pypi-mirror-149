# -*- coding: utf-8 -*-
from audioop import reverse
from distutils.log import info
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup #Principal biblioteca
from collections import Counter
from selenium import webdriver



class Analise:
    '''
        Essa classe analise recebe 2 paramentros que são str:

            # A url que poderá ser digitada pelo usuario
            # A palavra chave que também poderá ser digitada pelo usuario

        Em seu init tem  a url, a palavra chave, uma lista de resultado que vai guarda os resultados das analise
        e o tamanho do texto  que está sendo analisado
    
    '''

    __slots__ = ['_url', '_palavra','_lista_de_resultados','_tamanho_texto','_tempo_de_carregamento']

    def __init__(self, url, palavra):
        """ Função inicializadora com os atributos necessários"""
        self._url = url
        self._palavra = palavra
        self._lista_de_resultados = []
        self._tamanho_texto = 0
        self._tempo_de_carregamento = 0.0

    @property
    def url(self):
        return self._url

    @property
    def palavra(self):
        return self._palavra

    def calcula_velocidade_de_carregamento(self):
        '''
            # Essa função é usada para carregamento da url solicida
            # precisa do chromedrive para simular a navegação    
            # O tempo é dado em milliseconds (ms), mas fazemos a conversão
            # para segundos para facilitar a visualização
            # Esse tempo é armazenado na variavel do init self._tempo_de_carregamento
        
        '''

        ''' Chrome web driver interface para simular o carregamento'''
        hyperlink = self._url
        driver = webdriver.Chrome()
        print("Aguarde, analisando o site...")
        driver.get(hyperlink)
        List_temp = []
        ''' Use a API Navigation Timing para calcular os tempos mais importantes '''   
        
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")
        
        ''' calcula a performance'''
        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        List_temp.append(backendPerformance_calc/1000)
        List_temp.append(frontendPerformance_calc/1000)
        self._tempo_de_carregamento = sum(List_temp)
        print(self._tempo_de_carregamento)
        #mostra o tempo de carregamento
        print( "O tempo de carregamento da sua página foi de: ")
        print("Back End: %s segundos" % backendPerformance_calc)
        print("Front End: %s segundos" % frontendPerformance_calc)
        
        driver.quit()

    def capturaInformacoes(self):
        '''
            # Essa função tem como principal objetivo baixar o hmrl da url digita 
            # Separar cada parte do html que será analisado e fazer algusn tratamnetos dos
            resultados coletado
        
        '''
        informacoes = [] # serve para guarda informações da pagina
        listadelista_info =[] # ultilizada para guarda dados do site em formato lista de lista 

        
        
        try:
            html = urlopen(self._url)
        except HTTPError as e:
            print(e)
        except URLError:
            print("Dominio digitado incorretamente")
        else:
            res = BeautifulSoup(html.read(),"html5lib") # captura o html inteiro e armazena em res
            self.calcula_velocidade_de_carregamento()

            titulo = res.find("h3", {"class": "post-title"})# {0}posição do vetor - pegando o título do texto body          
            informacoes.append(titulo.getText())
            
            titulo_da_pagina =res.find("title") #pega o titulo da pagina - {1} posicao do vettor
            informacoes.append(titulo_da_pagina.getText())

            texto = res.find("div", {"class": "post-body"}) # pegando o corpo do texto{2}
            informacoes.append(texto.getText())
            # faz o calculo para saber o tamnho do texto principal
            tam = texto.getText() 
            tam = tam.split()
            tam = Counter(tam)
            self._tamanho_texto = sum(tam.values())
            

            link = res.find("a") #pega os titulos dos links {3} posicao no vetor
            informacoes.append(link.getText())

            link_completo = res.findAll("a")# links completos com titulos {3}
            for tag in link_completo:                
                listadelista_info.append(tag.getText().replace("\n", ""))
            valor4 = self.tratamento_listaDeLista(listadelista_info)

            h2 = res.find("h2")# pega o primeiro H2 {4}
            informacoes.append(h2.getText())
            
            
            h2_completo = res.findAll("h2")# pega tudo que tiver em H2 que são os topicos do texto {4}
            for tag in h2_completo:                
                listadelista_info.append(tag.getText().replace("\n", ""))
            valor2 = self.tratamento_listaDeLista(listadelista_info)
            

            img = res.find("img") # {5} pega a primeira imagem
            listadelista_info =[] #zerando essa lista
            informacoes.append(img.getText())

            img_completo = res.findAll("img")# pega tudo que tiver imagem - {5} posição 5 no vetor
            for tag in img_completo:                
                listadelista_info.append(tag.getText().replace("\n", ""))
            valor3 = self.tratamento_listaDeLista(listadelista_info)

            listadelista_info =[] #zerando essa lista
            description = res.findAll("meta", {"property": "og:description"}) #{6} pegando a descrição da pagina
            for tag in description:                
                listadelista_info.append(tag.getText().replace("\n", ""))
            valor5 = self.tratamento_listaDeLista(listadelista_info)
            

            
            
            
            
            quantidades = []
            for elemento in informacoes:
                aux = self.repetir(elemento) # buscas as palavras que se repetem
                quantidades.append(aux)
            quantidades.append(valor5)

            for i in range(len(quantidades)):
                if i == 4:
                    quantidades[i]+=valor2
                elif i == 5:
                    quantidades[i]+=valor3
                elif i == 3:
                    quantidades[i]+=valor4
            quantidades.append(self._tempo_de_carregamento)

            self._lista_de_resultados = quantidades
                

            length = len(quantidades)
            valor = 0

            for x in range(length):
                valor = valor + quantidades[x]
                
            
            return valor
    
    def tratamento_listaDeLista(self, listadelista):
        '''
            É  um tratamento especial quando temos uma lista de lista
            Tivemos que fazer algumas analises separadas da lista principal
            Pois nesse caso temos uma lista de lista e na lista normal é uma 
            lista de string
        '''
        
        for i in range(len(listadelista)):
            listadelista[i] = listadelista[i].lower()            
            
        palavra_chave = self._palavra.lower()
        
        valor = listadelista.count(palavra_chave)
        return valor

                

    def repetir(self, elemento):
        '''
            Faz a analise de quantas vezes uma palavra se repete
            recebe uma lista e em cada posição temos uma parte do html já convertido só em texto
            que deverá ser analisado
        '''
        
        frase = elemento.lower() #converte todas a string para minus       
        palavra_chave = self._palavra.lower() #converte tod           
        repetidas = frase.count(palavra_chave) #conta os elemntos de uma lista
              
        return repetidas

    def resultados(self):
        '''
            Após os resultados coletados, pegamos essas informações e fazemos o tratamento
            delas aqui nessa função, passamos então dicas de melhorias em cada parte do html
            que foi analisado.

            Também é feito uma pontuação da página que vai de 0 a 100 
        
        
        '''
        resultado = self._lista_de_resultados
        pontuacao = 0

        print('*' * 100)
        print('*' * 100)
        print('------------------------------RECOMENDAÇÕES------------------------------')
        for i in range(8):

            if(resultado[i] == 0 and i == 0):
                
                print("[1] Seu título precisa melhorar, recomendamos inserir a palavra-chave [{}] no inicio do título.".format(self._palavra))
            elif (resultado[i] == 1 and i == 0):
                
                print("[1] Seu título está bom, pois apresenta a palavra chave nele.")
                pontuacao+=10
            elif (resultado[i] == 0 and i == 1):
                print("[2] O título da página está ruim, recomendamos inserir a palavra-chave [{}] no seu título.".format(self._palavra))
            elif (resultado[i] == 1 and i == 1):
                print("[2] O título de sua página está bom, pois contém a palvra chave inserido nele")
                pontuacao+=10
            elif (resultado[i] < 10 and i == 2 and self._tamanho_texto>1000):
                print("[4] Seu texto principal ta ruim, precisa aumentar a quantidade de palavras chaves ou sinônimos")
                print("[4] Mas o tamanho do seu texto está bom")
                pontuacao+=5
            elif (resultado[i] > 10 and i == 2 and self._tamanho_texto<1000):
                print("[4] Seu texto principal ta bom, ccontém uma densidade superior a 10 palavras chaves ou sinônimos")
                print("[4] Precisa melhorar o tamanho do seu texto, recomendamos textos acima de 1000 palavras")
                pontuacao+=5
            elif (resultado[i] > 10 and i == 2 and self._tamanho_texto>1000):
                print("[4] O texto preincipal está bom, sua densidade de palavra chave ou sinônimos está acima de 10")
                pontuacao+=15
            elif(resultado[i]== 0 and i ==3):
                print(" [5] Você não possui nenhum link com a palvra chave no alt")
                print("[5] Recomendamos inserir ao menos 1 link que contenha o alt com a palvra chave")
            elif(resultado[i]>= 1 and i ==3):
                print("[5] Seu site possui ao menos link com o alt com a palavra chave, isso é bom")
                pontuacao+=10
            elif(resultado[i]== 0 and i ==4):
                print("[6] Nenhuma H2 possui a palavra chave, recomendamos que o primeiro contenha")

            elif(resultado[i]== 0 and i ==6):
                print("[8] Sua descrição está ruim, recomendo que coloque ao menos uma palavra chave")
                

            elif(resultado[i]>=1 and i ==6):
                print("[8] Parabéns, a descrição da sua página está boa")
                pontuacao+=10
                

            elif(resultado[i]>=1 and i ==4):
                print("[6] Parabéns, o primeiro h2 do texto possui a palvra chave")
                pontuacao+=10
            elif(resultado[i]== 0 and i ==5):
                
                print("[7] Nenhuma imagem possui a palavra chave, recomendamos que ao menos uma tenha")
                
            elif(resultado[i]>= 1 and i ==5):
                print("[7] Parabéns, você possui ao menos uma imagem com a palavra chave")
                pontuacao+=15
            
            #verifica o tamanho do texto principal

            if(self._tamanho_texto>1000 and i==1):
                print("[3] Seu texto possui um tamanho bom, acima de 1000 palavras")
                pontuacao+=10
            elif(self._tamanho_texto<1000 and i==1):
                print("[3] O tamanho ideal para um texto é acima de 1000 palavras")
                print("[3] textos nesses tamanho tem prioridade nos ranqueamentos")

            # verifica o tempo de carregamento
            if(resultado[i]<3.0 and i==7):
                print("[9] Parabéns, seu site carrega em menos de 3 segundos")
                pontuacao+=15
                print('*' * 100)
                print('*' * 100)
            elif( resultado[i]>3.0 and resultado[i]<6.0 and i==7 ):
                print("[9] Site lento, seu site carrega em menos de {:.2f} segundos, precisa melhorar".format(resultado[i]))
                pontuacao+=5
                print('*' * 100)
                print('*' * 100)
            elif(resultado[i]>6.0 and i==7):
                print("[9] CARREGAMENTO EXTREMAMENTE LENTO, Seu site foi carregaado em {:.2f} segundos o recomendavel é abaido dos 3 segundos".format(resultado[i]))
                pontuacao+=3
                print('*' * 100)
                print('*' * 100)
            
            
        if(pontuacao>=70):
            # Imprime a borda superior
            print('#' * 60)
            print('#' * 60)
            print("Excelente, a pontuação da análise foi superior a {} pontos de um total de 100 pontos".format(pontuacao))
            print('#' * 60)
            print('#' * 60)
        elif(pontuacao<70 and pontuacao>50):
            print('#' * 60)
            print('#' * 60)
            print("O SEO esta regular, precisa de algumas melhorias, sua pontuação foi de:{} de um total de 100 pontos".format(pontuacao))
            print('#' * 60)
            print('#' * 60)
        elif(pontuacao<50):
            print('#' * 60)
            print('#' * 60)
            print("SEO desta página está ruim, sua pontuação foi de {} de um total de 100 pontos".format(pontuacao))
            print('#' * 60)
            print('#' * 60)

  
            
            





    
