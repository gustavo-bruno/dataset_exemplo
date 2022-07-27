import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from csv import writer

url = 'https://www.historicosblaze.com/br/blaze/doubles'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

numero = soup.find('div', class_= 'roulette-tile flex-column')
numero_str=str(numero)
lista_mensagem_numero = numero_str.split('<div class="number">')

if len(lista_mensagem_numero) > 1:
    lista_mensagem_numero_2 = lista_mensagem_numero[1].split('\n')
    numero_chamado = int(lista_mensagem_numero_2[1])
else:
    numero_chamado = 0

if (numero_chamado == 0):
    cor_chamada = "WITHE"
elif (numero_chamado == 1) or (numero_chamado == 2) or (numero_chamado == 3) or (numero_chamado == 4) or (
        numero_chamado == 5) or (numero_chamado == 6) or (numero_chamado == 7):
    cor_chamada = "RED"
else:
    cor_chamada = "BLACK"
cor = cor_chamada

lista_mensagem_dataEhora = numero_str.split("hr&gt")
lista_mensagem_dataEhora_2=lista_mensagem_dataEhora[3].split('\n')
data = lista_mensagem_dataEhora_2[1].split('às')
data_numero = data[0].strip()
hora = data[1].split(' ')
hora_numero = hora[1].strip()



x = 0
hora_inicial = hora_numero
banca = 300
saldo = banca
entrada = 2
cor_apostar = "0"
estrategia = 0
estrategia_completa = 0
count = 0

lista = []
lista.append(cor)

liberacao = 0
dados = 1

tabela =[]
df = pd.DataFrame(tabela, columns=['data','hora','cor_chamada','cor_apostar','estrategia','estrada','saldo','count_black','count_red'])
df.to_csv('historico.csv',index=False)


while x < 30000:
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    numero = soup.find('div', class_= 'roulette-tile flex-column')
    hora = soup.find('div', class_= 'time text-white-75')
    numero_str=str(numero)

    lista_mensagem_numero = numero_str.split('<div class="number">')

    if len(lista_mensagem_numero) > 1:
        lista_mensagem_numero_2 = lista_mensagem_numero[1].split('\n')
        numero_chamado = int(lista_mensagem_numero_2[1])
    else :
        numero_chamado = 0

    if (numero_chamado == 0):
        cor_chamada = "WITHE"
    elif (numero_chamado == 1) or (numero_chamado == 2) or (numero_chamado == 3) or (numero_chamado == 4) or (numero_chamado == 5) or (numero_chamado == 6) or (numero_chamado == 7):
        cor_chamada = "RED"
    else:
        cor_chamada = "BLACK"
    cor = cor_chamada


    lista_mensagem_dataEhora = numero_str.split("hr&gt")
    tamanho_dados = len(lista_mensagem_dataEhora)
    if tamanho_dados > 3:
        lista_mensagem_dataEhora_2=lista_mensagem_dataEhora[3].split('\n')
        data = lista_mensagem_dataEhora_2[1].split('às')
        data_numero = data[0].strip()
        hora = data[1].split(' ')
        hora_numero = hora[1].strip()
        minuto = hora_numero.split(":")
        minuto = minuto[1]
        dados = 1
    else:
        dados = 0

    if hora_numero != hora_inicial and dados == 1:
        tamanho_lista = len(lista)
        lista.append(cor)
        if tamanho_lista==20:
            count_Black = 0
            count_Red=0
            count_Withe =0
            for iten in lista:
                if iten == "BLACK":
                    count_Black +=1
                elif iten == "RED":
                    count_Red += 1
                else:
                    count_Withe += 1
            print("Quantidade de pretos:",count_Black,"Quantidade de vermelho:",count_Red,"Quantidade de Branco:",count_Withe)
            if count_Black>count_Red:
                apostar_red = 0
                apostar_Black = 1
            elif count_Red>count_Black:
                apostar_Black = 0
                apostar_red = 1
            else:
                apostar_Black = 0
                apostar_red = 0
                estrategia_completa = 0
            if apostar_Black == 1 and liberacao == 0:
                if estrategia ==0 or estrategia==3 or estrategia==4:
                    estrategia =1
                elif estrategia == 1:
                    estrategia =2
                elif estrategia == 2:
                    estrategia = 1
                liberacao = 1
            elif apostar_red == 1 and liberacao == 0:
                if estrategia ==0 or estrategia == 1 or estrategia== 2:
                    estrategia =3
                elif estrategia == 3:
                    estrategia = 4
                elif estrategia == 4:
                    estrategia = 3
                liberacao = 1
            lista.remove(lista[0])
        if estrategia_completa == 1:
            if cor_chamada == cor_apostar:
                saldo = saldo + entrada
                print("Win, saldo após win:",saldo)
                estrategia_completa = 0
                entrada = 2
                liberacao = 0
            else:
                saldo = saldo - entrada
                print("Loss, saldo após loss:",saldo)
                entrada = entrada*2
                estrategia_completa = 0
                liberacao = 0
            list_data = [data_numero,hora_numero,cor_chamada,cor_apostar,estrategia,entrada,saldo,count_Black,count_Red]
            with open('historico.csv','a',newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(list_data)
                f_object.close()
        elif estrategia == 4 :
            if cor == "RED":
                count += 1
            else:
                count = 0
            if count == 1:
                cor_apostar = "RED"
                count = 0
                estrategia_completa = 1
        elif estrategia == 1:
            if cor == "RED":
                count += 1
            else:
                count = 0
            if count == 1:
                cor_apostar = "BLACK"
                count = 0
                estrategia_completa = 1

        elif estrategia == 2:
            if cor == "BLACK":
                count += 1
            else:
                count = 0
            if count == 1:
                cor_apostar = "BLACK"
                count = 0
                estrategia_completa = 1
        elif estrategia == 3:
            if cor == "BLACK":
                count += 1
            else:
                count = 0
            if count == 1:
                cor_apostar = "RED"
                count = 0
                estrategia_completa = 1

        print("Numero chamado as:",hora_numero,",Cor chamada:",cor_chamada, ",Estrategia:",estrategia, ",Proxima esntrada de:", entrada)
        hora_inicial = hora_numero
        x = x+1
        time.sleep(10)
    time.sleep(1)