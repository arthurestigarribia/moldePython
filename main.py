#-* coding: utf8 -*#-

from usuario import *
from usuariodao import *
from flask import *
import md5
import os
import sys

app = Flask(__name__)
app.secret_key = "chave_secreta"

udao = UsuarioDAO()

def getUsuario(email):
    l = udao.lista()

    for i in range(0, len(l)):
        if l[i].email == email:
            return l[i]
    
    return None

def verificaLogin(email, senha):
    return (getUsuario(email) and md5.new(senha).hexdigest() == getUsuario(email).senha) == True

@app.before_request
def antesDaRota():
	if not(request.path == '/login' or request.path == '/login' or request.path == '/fazLogin' or request.path == '/fazCadastro') and 'id' not in session:
		return redirect('/login')

@app.route('/')
def paginaInicial():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"

    return render_template("index.html", acao=acao, textologin=textologin, erro=None)

@app.route('/login')
def paginaLogin():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']

        redirect('/')
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"
    
        return render_template("login.html", acao=acao, textologin=textologin, erro=None)

@app.route('/fazLogin', methods = ['POST'])
def fazLogin():
    email = request.form['email']
    senha = request.form['senha']

    if verificaLogin(email, senha):
        session['nome'] = getUsuario(email).nome
        session['email'] = email
        session['id'] = getUsuario(email).id
    
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/fazCadastro', methods = ['POST'])
def fazCadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    if getUsuario(email) == None:
        u = Usuario(0, nome, email, senha)
        udao.adiciona(u)

        session['nome'] = nome
        session['email'] = email
        session['id'] = getUsuario(email).id

        return redirect('/')
    else:
        return redirect('/login')

@app.route('/fazLogout')
def fazLogout():
    if 'id' in session:
        session.pop('nome', None)
        session.pop('email', None)

        session.pop('id', None)

        return redirect('/')
    else:
        return redirect('/login')

@app.route('/exclui')
def exclui():
    if 'id' in session:
        udao = UsuarioDAO()

        session.pop('nome', None)
        session.pop('email', None)

        udao.remove(session['id'])

        session.pop('id', None)
    
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/edicao')
def paginaEdicao():
    if 'id' in session:
        acao = "/edicao"
        textologin = session['nome']

        return render_template("edicao.html", nome=session['nome'], email=session['email'], acao=acao, textologin=textologin, erro=None)
    else:
        acao = "/login"
        textologin = "Entrar ou cadastrar"

        return redirect('/login')

@app.route('/fazEdicao', methods = ['POST'])
def fazEdicao():
    if 'id' in session:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if getUsuario(email) == None:
            u = Usuario(0, nome, email, senha)
            udao.edita(u, session['id'])

            session['nome'] = nome
            session['email'] = email
        
            return redirect('/')
        else:
            return redirect('/edicao')
    else:
        return redirect('/login')

@app.errorhandler(404)
def erro(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	# para arrumar os acentos (principalmente no windows)
	reload(sys)
	sys.setdefaultencoding('UTF-8')
	app.run()