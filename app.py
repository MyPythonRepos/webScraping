import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template, request

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
app = Flask(__name__)
dic_categorias = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pccomponentes')
def pccomponentes():
    categorias = obtener_categorias()
    return render_template('categorias_pccomponentes.html', sitioWeb='PcComponentes', categorias=categorias)


@app.route('/lista_articulos/<categoria>')
def mostrar_articulos(categoria):
    url = dic_categorias[categoria]
    articulos = leer_articulos(url, categoria)
    return render_template('lista_articulos.html', articulos=articulos, categoria=categoria)


# Handlers de errores de la aplicación.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Utilidades
@app.context_processor
def utility_processor():
    def format_currency(value):
        return "{:,.2f} €".format(float(value))
    return dict(format_currency=format_currency)


def pedir_categoria():
    categoria = input("Tecla el nombre de la categoría a buscar y pulsa intro: ")
    url = "https://www.pccomponentes.com/" + categoria
    leer_articulos(url, categoria)


def obtener_categorias():
    url = "https://www.pccomponentes.com/"
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    for s in soup.findAll("a", class_="mkt-menu-level3"):
        title = s.get('title')
        href = s.get('href')
        if '/' in title:
            print(title)
            title = title.replace("/", " - ")
        dic_categorias[title] = href
    print(dic_categorias)
    lista_categorias = list(dic_categorias.keys())
    return lista_categorias


def leer_articulos(url,categoria):
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    dic = {}
    lista = []
    for s in soup.findAll("a"):
        print(s)
        if s.get('data-name') is not None:
            id = s.get('data-id')
            name = s.get('data-name')
            price = s.get('data-price')
            brand = s.get('data-brand')
            dic = dict(Id=id, Marca=brand, Nombre=name, Precio=price)
            if dic not in lista:
                lista.append(dic.copy())
    return lista


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run('0.0.0.0', 5002, debug=True)

