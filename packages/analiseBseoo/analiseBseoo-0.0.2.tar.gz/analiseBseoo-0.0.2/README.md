# Analise SEO de uma página da internet

Esse pacote tem como objetivo ajudar a analisar o SEO de uma página hmtl, seu funcionamento ainda é limitado para paginas blogspot


### 📋 Pré-requisitos

Precisa do python 3.9 instalado

```
$ apt get-apt install python
```
Precisa baixar o ChromeDrive para executar os testes corretamente, escolha a versão correta para seu computador no link abaixo:

*[ChromeDrive](https://chromedriver.storage.googleapis.com/index.html?path=101.0.4951.41/)

Obs: Lembrando que esse executável terá que está na pasta em que você vai executar a análise

### 🔧 Instalação


Será instalado da seguinte maneira

```
pip install analiseBSeo
```

## 🛠️ Construído com

Ferramenta usada para coleta de dados da web:

* [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 
* [Selenium](https://selenium-python.readthedocs.io/installation.html#) 


## ⚙️ URL de teste e modo da ultilização

https://www.cataimagem.com/2019/03/moderninha-pro-ou-sumup-total-qual-devo.html

Exemplo para executar o pacote:
Para executar o pocote você precisa fazer um import analiseBSeo

Em seguinda pode fazer assim:

from analiseBseoo.classAnalise import Analise

A classe Analise recebe 2 parametros, a URL e a palavra chave oara usar na analise
teste = Analise('https://www.cataimagem.com/2019/03/moderninha-pro-ou-sumup-total-qual-devo.html', 'SumUp Total')

Em seguida chama a função para obter as informações do site
teste.capturaInformacoes()

Por ultimo, chame a função para ver os resultados
teste.resultados()

Usando no interpretador Python:

![Analise no interpretador](https://loucosporgeek.com.br/wp-content/uploads/2022/05/Screenshot_1.png)





## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Elievelton** - *Trabalho Inicial* - [Elievelton](https://github.com/elievelton)
* **Bruna** - *Desenvolvimento* - [Bruna](https://github.com/linkParaPerfil)




## 🎁 Obrigado pela sua visita

* Venha participar dete projeto também 📢 
* Obrigado pela sua visita🤓.


---
⌨️ com ❤️ por [Elievelton](https://github.com/elievelton) 😊