import sys

import requests
import pandas as pd
from bs4 import BeautifulSoup


def switch(tipo_ejecucion):
    if (tipo_ejecucion == 1): pedir_categoria()
    elif(tipo_ejecucion == 2): obtener_categorias()
    else: print("Valor incorrecto")


def mostrar_cabecera(titulo):
    tamanio_linea = len(titulo)
    linea = ''
    for i in range(0, tamanio_linea):
        linea = linea + '='
    print("\n"+linea)
    print(titulo)
    print(linea)


def pedir_categoria():
    categoria = input("Tecla el nombre de la categoría a buscar y pulsa intro: ")
    url = "https://www.pccomponentes.com/" + categoria
    leer_articulos(url, categoria)


def obtener_categorias():
    url = "https://www.pccomponentes.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dic_categorias = {}
    mostrar_cabecera("= Obtenemos categorías principales de artículos =")
    for s in soup.findAll("a", class_="mkt-menu-level3"):
        dic_categorias[s.get('title')] = s.get('href')
    print(dic_categorias)
    categorias = list(dic_categorias.keys())
    i = 0
    for item in categorias:
        i = i+1
        print(str(i) + " - " + str(item))
    index = int(input("Selecciona una categoría y pulsa intro:"))
    categoria = (categorias[index - 1])
    categoria_url = dic_categorias.get(categoria)
    leer_articulos(categoria_url, categoria )


def leer_articulos(url,categoria):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dic = {}
    lista = []
    for s in soup.findAll("a"):
        if s.get('data-name') is not None:
            id = s.get('data-id')
            name = s.get('data-name')
            price = s.get('data-price')
            brand = s.get('data-brand')
            dic = dict(Id=id, Marca=brand, Nombre=name, Precio=price)
            if dic not in lista:
                lista.append(dic.copy())
    titulo = "= Mostramos la lista de artículos dentro de la categoría: " + categoria + " ="
    mostrar_cabecera(titulo)
    if len(lista) == 0:
        print("No hay objetos en la lista")
    else:
        for elem in lista:
            print(elem.values())
        # TODO guardar archivo en el escritorio. Ver si es posible en función del SO
        file = categoria+'.csv'
        df = pd.DataFrame(lista, columns=['Id', 'Nombre', 'Precio'])
        df.to_csv(file, sep=';')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        print("1. Ejecución simplificada")
        print("2. Ejecución completa")
        print("3. Salir")
        tipo_ejecucion = int(input("Escoge un tipo de ejecucion del script: "))
        # TODO controlar error cuando no se introducen números
        if tipo_ejecucion == 3:
            break
        else:
            switch(tipo_ejecucion)
