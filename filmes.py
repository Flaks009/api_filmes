from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)

@app.route('/filmes', methods=['GET'])

def filmes():
    return render_template('pesquisa.html', mensagem = 'Nome do Filme')

@app.route('/pesquisa_filmes_nome', methods = ['POST'])
def pesquisa_nome():
    api_key = 'ce4285e7'
    nome_filme = request.form['nome']
    url = "http://www.omdbapi.com/?apikey={}&s={}".format(api_key, nome_filme)
    retorno_string = requests.get(url).json()
    if retorno_string['Response'] == 'False':
        return render_template('pesquisa.html', mensagem = 'Erro, pesquise novamente')

    titulo = retorno_string['Search'][0]['Title']  
    id_filme = retorno_string['Search'][0]['imdbID']  
    url = "http://www.omdbapi.com/?apikey={}&i={}".format(api_key, id_filme)
    retorno_id = requests.get(url).json()
    diretor = retorno_id['Director']
    ano = retorno_id['Year']
    url_image = "http://img.omdbapi.com/?apikey={0}&i={1}".format(api_key, id_filme)

    if len(retorno_string['Search']) > 1:
        filmes = []
        for filme in range (len(retorno_string['Search'])):
            x = {
            'id' : retorno_string['Search'][filme]['imdbID'],
            'titulo' : retorno_string['Search'][filme]['Title']
            }
            filmes.append(x)            
        return render_template("filme.html", filme = titulo, imagem = url_image, diretor=diretor, ano = ano, filmes=filmes)

    return render_template("filme.html", filme = titulo, imagem = url_image, diretor=diretor, ano = ano)

@app.route('/pesquisa_filmes_id', methods = ['POST'])
def pesquisa_filmes_id():
    api_key = 'ce4285e7'
    id_filme = request.form['id_filme']
    url = "http://www.omdbapi.com/?apikey={}&i={}".format(api_key, id_filme)
    retorno_id = requests.get(url).json()
    titulo = retorno_id['Title']
    diretor = retorno_id['Director']
    ano = retorno_id['Year']
    url_image = "http://img.omdbapi.com/?apikey={0}&i={1}".format(api_key, id_filme)

    return render_template("filme.html", filme = titulo, diretor = diretor, ano = ano, imagem = url_image)



if __name__ == '__main__':
    app.run()