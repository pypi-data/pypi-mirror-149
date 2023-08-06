from analiseBseoo import Analise

# Main feito apenas para coletar os inputs e
# recebe os dados para analise
# URL de teste - 'https://www.cataimagem.com/2019/03/moderninha-pro-ou-sumup-total-qual-devo.html'
# C:\Users\eliev\AppData\Local\Programs\Python\Python39\Lib\site-packages

url = input("Digite a url que você deseja analisar: ")
palavra = input('Digite a palavra que deseja buscar: ')


teste = Analise(url, palavra)
teste.capturaInformacoes()
teste.resultados()
